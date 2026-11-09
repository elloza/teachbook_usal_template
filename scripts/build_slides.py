#!/usr/bin/env python3
"""Construye las diapositivas Slidev dentro del sitio HTML del TeachBook."""

from __future__ import annotations

import argparse
import html
import json
import os
import platform
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

from build_cache import BUILD_ROOT, CACHE_ROOT, build_lock, file_hash, fingerprint, remove_build_tree, tree_hashes
from project_options import PROJECT_ROOT, SLIDEV_CLI, SLIDES_DIR, node_runtime, slides_enabled

BOOK_DIR = PROJECT_ROOT / "book"
HTML_DIR = BUILD_ROOT / "html"
SLIDE_CACHE_DIR = CACHE_ROOT / "slidev"
DEFAULT_SLIDEV_JOBS = 2
IGNORED_SLIDE_DIRS = {"node_modules", "dist", ".slidev", ".vite", ".cache"}


@dataclass(frozen=True)
class Deck:
    lang: str
    position: str
    book_file: str
    source: Path
    url: str
    title: str
    section_files: tuple[str, ...] = ()


def normalize_site_base(value: str | None) -> str:
    base = (value or "/").strip() or "/"
    if not base.startswith("/"):
        base = "/" + base
    if not base.endswith("/"):
        base += "/"
    return base


def deck_base(site_base: str, deck_url: str) -> str:
    deck_dir = deck_url.rsplit("/", 1)[0] + "/"
    return normalize_site_base(site_base).rstrip("/") + "/" + deck_dir


def detect_languages() -> list[str]:
    languages = sorted(
        path.stem.replace("_config_", "", 1)
        for path in BOOK_DIR.glob("_config_*.yml")
    )
    if languages:
        return languages
    if (BOOK_DIR / "_config.yml").is_file():
        return ["default"]
    raise SystemExit("ERROR: no se han encontrado configuraciones del libro.")


def load_toc(lang: str) -> dict:
    toc_name = "_toc.yml" if lang == "default" else f"_toc_{lang}.yml"
    toc_path = BOOK_DIR / toc_name
    if not toc_path.is_file():
        raise SystemExit(f"ERROR: falta {toc_path.relative_to(PROJECT_ROOT)}.")
    with toc_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def html_page_for_book_file(book_file: str) -> str:
    return f"{book_file}.html".replace("\\", "/")


def slide_source_for_book_file(book_file: str) -> Path:
    path = Path(book_file)
    if path.is_absolute() or path.drive or ".." in path.parts:
        raise ValueError(f"Ruta de capítulo no válida para Slidev: {book_file}")
    return SLIDES_DIR / path / "slides.md"


def slide_url_for_book_file(book_file: str) -> str:
    return f"slides/{book_file}/index.html".replace("\\", "/")


def candidate_content_paths(book_file: str) -> list[Path]:
    raw = BOOK_DIR / book_file
    if raw.suffix:
        return [raw]
    return [raw.with_suffix(".md"), raw.with_suffix(".ipynb")]


def strip_title(line: str) -> str:
    title = line.lstrip("#").strip()
    title = re.sub(r"\{[^}]*\}$", "", title).strip()
    title = re.sub(r"`([^`]*)`", r"\1", title)
    title = re.sub(r"\*\*([^*]*)\*\*", r"\1", title)
    title = re.sub(r"\*([^*]*)\*", r"\1", title)
    return title or "Diapositivas"


def title_from_source(book_file: str) -> str:
    for candidate in candidate_content_paths(book_file):
        if not candidate.is_file():
            continue
        if candidate.suffix.lower() == ".ipynb":
            try:
                data = json.loads(candidate.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            for cell in data.get("cells", []):
                if cell.get("cell_type") != "markdown":
                    continue
                source = cell.get("source", [])
                lines = source if isinstance(source, list) else str(source).splitlines()
                for line in lines:
                    if line.lstrip().startswith("#"):
                        return strip_title(line)
        else:
            try:
                lines = candidate.read_text(encoding="utf-8").splitlines()
            except UnicodeDecodeError:
                continue
            for line in lines:
                if line.lstrip().startswith("#"):
                    return strip_title(line)
    return Path(book_file).name.replace("_", " ").replace("-", " ").title()


def collect_decks() -> list[Deck]:
    decks: list[Deck] = []
    for lang in detect_languages():
        toc = load_toc(lang)
        root_file = toc.get("root")
        if root_file:
            decks.append(
                Deck(
                    lang=lang,
                    position="root",
                    book_file=root_file,
                    source=slide_source_for_book_file(root_file),
                    url=slide_url_for_book_file(root_file),
                    title=title_from_source(root_file),
                )
            )

        for part_index, part in enumerate(toc.get("parts", []) or []):
            for chapter_index, chapter in enumerate(part.get("chapters", []) or []):
                chapter_file = chapter.get("file")
                if not chapter_file:
                    continue
                section_files = tuple(
                    section.get("file")
                    for section in chapter.get("sections", []) or []
                    if section.get("file")
                )
                decks.append(
                    Deck(
                        lang=lang,
                        position=f"p{part_index}/c{chapter_index}",
                        book_file=chapter_file,
                        source=slide_source_for_book_file(chapter_file),
                        url=slide_url_for_book_file(chapter_file),
                        title=title_from_source(chapter_file),
                        section_files=section_files,
                    )
                )
    return decks


def validate_decks(decks: list[Deck]) -> None:
    if not decks or len({deck.book_file for deck in decks}) != len(decks):
        raise SystemExit("ERROR: el TOC debe definir capítulos con rutas únicas para las diapositivas.")
    missing = [deck for deck in decks if not deck.source.is_file()]
    if missing:
        print("ERROR: faltan diapositivas Slidev.")
        for deck in missing:
            print(
                "  - "
                f"{deck.source.relative_to(PROJECT_ROOT)} "
                f"({deck.lang}, {deck.position})"
            )
        print("Ejecuta: python scripts/sync_slide_templates.py")
        raise SystemExit(1)


def ensure_temporary_deck_style(deck_source: Path) -> Path | None:
    """Make shared Slidev styles visible when compiling a nested deck."""
    deck_dir = deck_source.parent
    deck_style = deck_dir / "style.css"
    if deck_style.exists():
        return None
    shared_style = SLIDES_DIR / "styles" / "teachbook.css"
    relative_style = os.path.relpath(shared_style, deck_dir).replace("\\", "/")
    deck_style.write_text(f'@import "{relative_style}";\n', encoding="utf-8", newline="\n")
    return deck_style


def count_slides(deck_source: Path) -> int:
    """Count top-level Slidev slide separators in a deck source."""
    lines = deck_source.read_text(encoding="utf-8").splitlines()
    separator_count = 0
    in_fence = False
    fence_marker = ""
    first_content_line = ""

    for line in lines:
        stripped = line.strip()
        if stripped and not first_content_line:
            first_content_line = stripped

        fence_match = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_match:
            marker = fence_match.group(1)
            if in_fence and marker.startswith(fence_marker[0]) and len(marker) >= len(fence_marker):
                in_fence = False
                fence_marker = ""
            elif not in_fence:
                in_fence = True
                fence_marker = marker
            continue

        if not in_fence and stripped == "---":
            separator_count += 1

    if separator_count == 0:
        return 1
    if first_content_line == "---":
        return max(1, separator_count - 1)
    return separator_count + 1


def write_clean_slide_entrypoints(deck: Deck, out_dir: Path) -> int:
    """Create GitHub Pages-safe clean URLs like /slides/.../4."""
    index_path = out_dir / "index.html"
    index_html = index_path.read_text(encoding="utf-8")
    slide_count = count_slides(deck.source)
    for slide_number in range(1, slide_count + 1):
        slide_dir = out_dir / str(slide_number)
        slide_dir.mkdir(parents=True, exist_ok=True)
        (slide_dir / "index.html").write_text(index_html, encoding="utf-8", newline="\n")
    return slide_count


def build_deck(deck: Deck, base: str, out_dir: Path, node: str) -> None:
    cmd = [
        node,
        str(SLIDEV_CLI),
        "build",
        str(deck.source.resolve()),
        "--base",
        base,
        "--out",
        str(out_dir.resolve()),
        "--without-notes",
    ]
    temporary_style = ensure_temporary_deck_style(deck.source)
    try:
        result = subprocess.run(
            cmd,
            cwd=SLIDES_DIR,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
    finally:
        if temporary_style is not None and temporary_style.exists():
            temporary_style.unlink()
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="")
        raise subprocess.CalledProcessError(result.returncode, cmd)
    slide_count = write_clean_slide_entrypoints(deck, out_dir)
    print(f"Slidev {deck.book_file}: {slide_count} diapositivas compiladas.")


def parse_jobs(value: str | None) -> int:
    if value is None or not value.strip():
        return DEFAULT_SLIDEV_JOBS
    try:
        jobs = int(value)
    except ValueError:
        raise SystemExit(f"ERROR: valor de jobs no valido: {value!r}.")
    if jobs < 1:
        raise SystemExit("ERROR: jobs debe ser >= 1.")
    return jobs


def build_decks(decks: list[Deck], site_base: str, html_dir: Path, *, jobs: int, clean: bool) -> None:
    if not SLIDEV_CLI.is_file():
        raise SystemExit("ERROR: falta Slidev en slides/node_modules. Ejecuta scripts/setup_env.py --yes.")
    node, node_version = node_runtime()
    hashes = tree_hashes(SLIDES_DIR, ignored_dirs=IGNORED_SLIDE_DIRS)
    deck_hashes = {deck.source: hashes.pop(deck.source.relative_to(SLIDES_DIR).as_posix()) for deck in decks}
    shared_key = fingerprint([node_version, platform.system(), platform.machine(), file_hash(Path(__file__)), hashes])
    all_deck_sources = fingerprint(sorted((deck.book_file, deck_hashes[deck.source]) for deck in decks))
    cache = SLIDE_CACHE_DIR / fingerprint(site_base)[:12]
    cache.mkdir(parents=True, exist_ok=True)

    pending = []
    outputs = {}
    for deck in decks:
        base = deck_base(site_base, deck.url)
        slot = fingerprint(deck.book_file)[:24]
        out_dir = cache / slot
        stamp = cache / f"{slot}.key"
        # Slidev can include another deck with src:, so those decks also depend on the other entries.
        includes = re.search(r"(?m)^\s*src\s*:", deck.source.read_text(encoding="utf-8"))
        key = fingerprint([base, shared_key, deck_hashes[deck.source], all_deck_sources if includes else None])
        outputs[deck] = out_dir
        reusable = (
            not clean and (out_dir / "index.html").is_file() and (out_dir / "assets").is_dir()
            and stamp.is_file() and stamp.read_text(encoding="utf-8") == key
        )
        if not reusable:
            stamp.unlink(missing_ok=True)
            remove_build_tree(out_dir)
            pending.append((deck, base, out_dir, stamp, key))

    print(f"Slidev: {len(pending)} para compilar, {len(decks) - len(pending)} en caché.")
    with ThreadPoolExecutor(max_workers=min(jobs, max(1, len(pending)))) as executor:
        future_to_deck = {
            executor.submit(build_deck, deck, base, out_dir, node): (deck, stamp, key)
            for deck, base, out_dir, stamp, key in pending
        }
        for future in as_completed(future_to_deck):
            deck, stamp, key = future_to_deck[future]
            try:
                future.result()
            except (OSError, subprocess.CalledProcessError) as exc:
                raise SystemExit(
                    f"ERROR: fallo construyendo slides {deck.lang} {deck.position} "
                    f"({deck.source.relative_to(PROJECT_ROOT)})."
                ) from exc
            stamp.write_text(key, encoding="utf-8")
    for deck, out_dir in outputs.items():
        shutil.copytree(out_dir, html_dir / "slides" / deck.book_file, dirs_exist_ok=True)


def copy_shared_public_assets(html_dir: Path) -> None:
    """Expose shared Slidev public assets at /slides/public/."""
    source_dir = SLIDES_DIR / "public"
    if not source_dir.is_dir():
        return
    target_dir = html_dir / "slides" / "public"
    remove_build_tree(target_dir)
    shutil.copytree(source_dir, target_dir)
    print(f"Assets publicos de Slidev copiados: {target_dir.relative_to(PROJECT_ROOT)}")


def hub_title(lang: str) -> str:
    return "Slides" if lang == "en" else "Diapositivas"


def write_hubs(decks: list[Deck], html_dir: Path) -> None:
    by_lang: dict[str, list[Deck]] = {}
    for deck in decks:
        by_lang.setdefault(deck.lang, []).append(deck)

    for lang, lang_decks in by_lang.items():
        hub_dir = html_dir / "slides" / lang
        hub_dir.mkdir(parents=True, exist_ok=True)
        title = hub_title(lang)
        prefix = "slides/" if lang == "default" else f"slides/{lang}/"
        parent = "../" if lang == "default" else ""
        items = "\n".join(
            f'<li><a href="{html.escape(parent + deck.url.removeprefix(prefix))}">'
            f"{html.escape(deck.title)}</a>"
            f' <span>{deck.position}</span></li>'
            for deck in lang_decks
        )
        markup = f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; color: #172026; background: #f6f8fa; }}
    main {{ max-width: 960px; margin: 0 auto; padding: 48px 24px; }}
    h1 {{ font-size: 2.25rem; margin: 0 0 1rem; }}
    p {{ color: #53616f; }}
    ul {{ list-style: none; margin: 2rem 0 0; padding: 0; display: grid; gap: 0.75rem; }}
    li {{ align-items: center; background: white; border: 1px solid #d8dee4; border-radius: 8px; display: flex; justify-content: space-between; padding: 0.9rem 1rem; }}
    a {{ color: #005a8b; font-weight: 650; text-decoration: none; }}
    span {{ color: #6e7781; font-size: 0.82rem; }}
  </style>
</head>
<body>
  <main>
    <h1>{title}</h1>
    <p>{'Coleccion de diapositivas asociadas al libro.' if lang != 'en' else 'Collection of slide decks associated with the book.'}</p>
    <ul>
      {items}
    </ul>
  </main>
</body>
</html>
"""
        (hub_dir / "index.html").write_text(markup, encoding="utf-8", newline="\n")
        print(f"Hub generado: {(hub_dir / 'index.html').relative_to(PROJECT_ROOT)}")


def write_manifest(decks: list[Deck], html_dir: Path) -> None:
    static_dir = html_dir / "_static"
    static_dir.mkdir(parents=True, exist_ok=True)
    languages = sorted({deck.lang for deck in decks})
    pages: dict[str, str] = {}
    for deck in decks:
        pages[html_page_for_book_file(deck.book_file)] = deck.url
        for section_file in deck.section_files:
            pages[html_page_for_book_file(section_file)] = deck.url

    manifest = {
        "version": 1,
        "languages": languages,
        "hubs": {lang: f"slides/{lang}/index.html" for lang in languages},
        "pages": dict(sorted(pages.items())),
        "decks": [
            {
                key: value
                for key, value in asdict(deck).items()
                if key in {"lang", "position", "title"}
            }
            | {
                "source": str(deck.source.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                "url": deck.url,
            }
            for deck in decks
        ],
    }
    target = static_dir / "slides_manifest.json"
    target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"Manifest generado: {target.relative_to(PROJECT_ROOT)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Construye slides Slidev del TeachBook.")
    parser.add_argument(
        "--site-base",
        default=os.environ.get("TEACHBOOK_SITE_BASE", "/"),
        help="Base publica del sitio, por ejemplo /repo/ en GitHub Pages.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Valida, genera hubs y manifest sin ejecutar Slidev.",
    )
    parser.add_argument("--clean", action="store_true", help="Reconstruir las presentaciones sin reutilizar la caché.")
    parser.add_argument(
        "--jobs",
        type=parse_jobs,
        default=parse_jobs(os.environ.get("TEACHBOOK_SLIDEV_JOBS")),
        help=(
            "Numero de decks Slidev a compilar en paralelo. "
            "Tambien puede definirse con TEACHBOOK_SLIDEV_JOBS. Por defecto: 2."
        ),
    )
    return parser.parse_args()


def build_site_slides(html_dir: Path, site_base: str, *, jobs: int, clean: bool, skip_build: bool = False) -> None:
    if not (SLIDES_DIR / "package.json").is_file():
        raise SystemExit("ERROR: Slidev está activado, pero falta slides/package.json.")
    decks = collect_decks()
    validate_decks(decks)
    if not skip_build:
        build_decks(decks, normalize_site_base(site_base), html_dir, jobs=jobs, clean=clean)

    copy_shared_public_assets(html_dir)
    write_hubs(decks, html_dir)
    write_manifest(decks, html_dir)
    print("Build Slidev completado.")


def main() -> int:
    args = parse_args()
    if not slides_enabled():
        print("Slidev desactivado en teachbook.json.")
        return 0

    with build_lock():
        if args.skip_build:
            build_site_slides(HTML_DIR, args.site_base, jobs=args.jobs, clean=args.clean, skip_build=True)
            return 0
        with TemporaryDirectory(prefix=".slides-", dir=BUILD_ROOT, ignore_cleanup_errors=True) as stage:
            stage = Path(stage)
            build_site_slides(stage, args.site_base, jobs=args.jobs, clean=args.clean)
            target = HTML_DIR / "slides"
            manifest = HTML_DIR / "_static" / "slides_manifest.json"
            manifest.parent.mkdir(parents=True, exist_ok=True)
            previous = stage / "previous"
            if target.exists():
                if target.is_symlink() or target.is_junction():
                    raise ValueError(f"La salida Slidev no puede ser un enlace: {target}")
                target.replace(previous)
            try:
                (stage / "slides").replace(target)
                (stage / "_static" / manifest.name).replace(manifest)
            except OSError:
                remove_build_tree(target)
                if previous.exists():
                    previous.replace(target)
                raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
