#!/usr/bin/env python3
"""Construye las diapositivas Slidev dentro del sitio HTML del TeachBook."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"
SLIDES_DIR = PROJECT_ROOT / "slides"
HTML_DIR = BOOK_DIR / "_build" / "html"
STATIC_DIR = HTML_DIR / "_static"
MIN_NODE_VERSION = (22, 18, 0)


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
    return SLIDES_DIR / book_file / "slides.md"


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


def npx_command() -> str:
    return "npx.cmd" if os.name == "nt" else "npx"


def parse_node_version(output: str) -> tuple[int, int, int] | None:
    match = re.search(r"v?(\d+)\.(\d+)\.(\d+)", output.strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def ensure_node_available() -> None:
    try:
        node = subprocess.run(
            ["node", "--version"],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        node = None
    if node is None or node.returncode != 0:
        raise SystemExit(
            "ERROR: Node.js no esta instalado. Instala Node.js >= 22.18.0 desde "
            "https://nodejs.org/ y vuelve a ejecutar scripts/setup_env.py --yes."
        )
    version = parse_node_version(node.stdout)
    if version is None or version < MIN_NODE_VERSION:
        raise SystemExit(
            "ERROR: Node.js demasiado antiguo: "
            f"{node.stdout.strip() or 'desconocido'}. Se requiere >= 22.18.0."
        )
    if shutil.which("npm") is None or shutil.which(npx_command()) is None:
        raise SystemExit("ERROR: npm/npx no esta disponible. Reinstala Node.js desde https://nodejs.org/.")


def slidev_supports_without_notes() -> bool:
    result = subprocess.run(
        [npx_command(), "slidev", "build", "--help"],
        cwd=SLIDES_DIR,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return "--without-notes" in ((result.stdout or "") + (result.stderr or ""))


def build_deck(deck: Deck, site_base: str, *, without_notes: bool) -> None:
    out_dir = HTML_DIR / "slides" / deck.book_file
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        npx_command(),
        "slidev",
        "build",
        str(deck.source.resolve()),
        "--base",
        deck_base(site_base, deck.url),
        "--out",
        str(out_dir.resolve()),
    ]
    if without_notes:
        cmd.append("--without-notes")
    print(f"Construyendo slides: {deck.lang} {deck.position} -> {deck.url}")
    result = subprocess.run(
        cmd,
        cwd=SLIDES_DIR,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n")
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)


def hub_title(lang: str) -> str:
    return "Slides" if lang == "en" else "Diapositivas"


def write_hubs(decks: list[Deck]) -> None:
    by_lang: dict[str, list[Deck]] = {}
    for deck in decks:
        by_lang.setdefault(deck.lang, []).append(deck)

    for lang, lang_decks in by_lang.items():
        hub_dir = HTML_DIR / "slides" / lang
        hub_dir.mkdir(parents=True, exist_ok=True)
        title = hub_title(lang)
        items = "\n".join(
            f'<li><a href="{deck.url.removeprefix(f"slides/{lang}/")}">{deck.title}</a>'
            f' <span>{deck.position}</span></li>'
            for deck in lang_decks
        )
        html = f"""<!doctype html>
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
        (hub_dir / "index.html").write_text(html, encoding="utf-8", newline="\n")
        print(f"Hub generado: {(hub_dir / 'index.html').relative_to(PROJECT_ROOT)}")


def write_manifest(decks: list[Deck]) -> None:
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
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
    target = STATIC_DIR / "slides_manifest.json"
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
    return parser.parse_args()


def main() -> int:
    if not (SLIDES_DIR / "package.json").is_file():
        print("No existe slides/package.json; se omite Slidev.")
        return 0

    decks = collect_decks()
    validate_decks(decks)
    HTML_DIR.mkdir(parents=True, exist_ok=True)

    args = parse_args()
    site_base = normalize_site_base(args.site_base)
    if not args.skip_build:
        ensure_node_available()
        without_notes = slidev_supports_without_notes()
        if not without_notes:
            print("AVISO: esta version de Slidev no soporta --without-notes; se compila sin esa bandera.")
        for deck in decks:
            build_deck(deck, site_base, without_notes=without_notes)
    else:
        print("Modo --skip-build: no se ejecuta Slidev.")

    write_hubs(decks)
    write_manifest(decks)
    print("Build Slidev completado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
