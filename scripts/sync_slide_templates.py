#!/usr/bin/env python3
"""Crea plantillas Slidev para root y capitulos del TeachBook."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"
SLIDES_DIR = PROJECT_ROOT / "slides"


@dataclass(frozen=True)
class DeckSpec:
    lang: str
    position: str
    book_file: str
    slide_file: Path
    title: str


def detect_languages() -> list[str]:
    languages = sorted(
        path.stem.replace("_config_", "", 1)
        for path in BOOK_DIR.glob("_config_*.yml")
    )
    if languages:
        return languages
    if (BOOK_DIR / "_config.yml").is_file():
        return ["default"]
    raise SystemExit("ERROR: no se han encontrado configuraciones book/_config_<lang>.yml.")


def load_toc(lang: str) -> dict:
    toc_name = "_toc.yml" if lang == "default" else f"_toc_{lang}.yml"
    toc_path = BOOK_DIR / toc_name
    if not toc_path.is_file():
        raise SystemExit(f"ERROR: falta {toc_path.relative_to(PROJECT_ROOT)}.")
    with toc_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data


def slide_path_for_book_file(book_file: str) -> Path:
    return SLIDES_DIR / book_file / "slides.md"


def candidate_content_paths(book_file: str) -> list[Path]:
    raw = BOOK_DIR / book_file
    if raw.suffix:
        return [raw]
    return [raw.with_suffix(".md"), raw.with_suffix(".ipynb")]


def strip_markdown_title(line: str) -> str:
    title = line.lstrip("#").strip()
    title = re.sub(r"\{[^}]*\}$", "", title).strip()
    title = re.sub(r"`([^`]*)`", r"\1", title)
    title = re.sub(r"\*\*([^*]*)\*\*", r"\1", title)
    title = re.sub(r"\*([^*]*)\*", r"\1", title)
    return title or "Diapositivas"


def title_from_markdown(path: Path) -> str | None:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith("#"):
                return strip_markdown_title(line)
    except UnicodeDecodeError:
        return None
    return None


def title_from_notebook(path: Path) -> str | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    for cell in data.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", [])
        lines = source if isinstance(source, list) else str(source).splitlines()
        for line in lines:
            if line.lstrip().startswith("#"):
                return strip_markdown_title(line)
    return None


def title_for_book_file(book_file: str) -> str:
    for candidate in candidate_content_paths(book_file):
        if not candidate.is_file():
            continue
        if candidate.suffix.lower() == ".ipynb":
            title = title_from_notebook(candidate)
        else:
            title = title_from_markdown(candidate)
        if title:
            return title
    return Path(book_file).name.replace("_", " ").replace("-", " ").title()


def expected_decks_for_language(lang: str) -> list[DeckSpec]:
    toc = load_toc(lang)
    decks: list[DeckSpec] = []

    root_file = toc.get("root")
    if root_file:
        decks.append(
            DeckSpec(
                lang=lang,
                position="root",
                book_file=root_file,
                slide_file=slide_path_for_book_file(root_file),
                title=title_for_book_file(root_file),
            )
        )

    for part_index, part in enumerate(toc.get("parts", []) or []):
        for chapter_index, chapter in enumerate(part.get("chapters", []) or []):
            chapter_file = chapter.get("file")
            if not chapter_file:
                continue
            decks.append(
                DeckSpec(
                    lang=lang,
                    position=f"p{part_index}/c{chapter_index}",
                    book_file=chapter_file,
                    slide_file=slide_path_for_book_file(chapter_file),
                    title=title_for_book_file(chapter_file),
                )
            )
    return decks


def template_for_deck(deck: DeckSpec) -> str:
    if deck.lang == "en":
        subtitle = "Teaching slides template"
        agenda = "Session plan"
        objectives = "Learning objectives"
        activity = "Class activity"
        closing = "Closing"
        pending = "Replace this placeholder with the final slides for this section."
        notes = "These slides are generated from the TeachBook slide template."
    else:
        subtitle = "Plantilla de diapositivas docentes"
        agenda = "Plan de la sesion"
        objectives = "Objetivos de aprendizaje"
        activity = "Actividad de clase"
        closing = "Cierre"
        pending = "Sustituye este placeholder por las diapositivas finales de esta parte."
        notes = "Estas diapositivas se generan desde la plantilla Slidev del TeachBook."

    yaml_title = "'" + deck.title.replace("'", "''") + "'"

    return f"""---
theme: default
layout: cover
title: {yaml_title}
titleTemplate: "%s"
info: |
  {notes}
class: teachbook-slidev
transition: slide-left
mdc: true
drawings:
  enabled: true
  persist: true
---

# {deck.title}

<p class="subtitle">{subtitle}</p>

---

# {agenda}

- {objectives}
- {activity}
- {closing}

---

# {objectives}

{pending}

---

# {activity}

- Punto de partida
- Desarrollo guiado
- Discusion final

---

# {closing}

- Ideas clave
- Preguntas abiertas
- Proximos pasos
"""


def sync_templates(dry_run: bool = False) -> int:
    created = 0
    for lang in detect_languages():
        for deck in expected_decks_for_language(lang):
            if deck.slide_file.exists():
                continue
            created += 1
            relative = deck.slide_file.relative_to(PROJECT_ROOT)
            if dry_run:
                print(f"CREARIA {relative}")
                continue
            deck.slide_file.parent.mkdir(parents=True, exist_ok=True)
            deck.slide_file.write_text(template_for_deck(deck), encoding="utf-8", newline="\n")
            print(f"Creado {relative}")
    return created


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sincroniza plantillas Slidev desde los TOC.")
    parser.add_argument("--dry-run", action="store_true", help="Muestra lo que se crearia sin escribir archivos.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    created = sync_templates(dry_run=args.dry_run)
    if created == 0:
        print("Plantillas Slidev ya sincronizadas.")
    elif args.dry_run:
        print(f"Plantillas que faltan: {created}")
    else:
        print(f"Plantillas creadas: {created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
