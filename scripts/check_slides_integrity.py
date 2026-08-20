#!/usr/bin/env python3
"""Valida la estructura multiidioma de las diapositivas Slidev."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"
SLIDES_DIR = PROJECT_ROOT / "slides"


@dataclass(frozen=True)
class ExpectedDeck:
    lang: str
    position: str
    book_file: str
    slide_file: Path


def detect_languages() -> list[str]:
    languages = sorted(
        path.stem.replace("_config_", "", 1)
        for path in BOOK_DIR.glob("_config_*.yml")
    )
    if languages:
        return languages
    if (BOOK_DIR / "_config.yml").is_file():
        return ["default"]
    return []


def load_toc(lang: str) -> dict:
    toc_name = "_toc.yml" if lang == "default" else f"_toc_{lang}.yml"
    toc_path = BOOK_DIR / toc_name
    with toc_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def slide_path_for_book_file(book_file: str) -> Path:
    return SLIDES_DIR / book_file / "slides.md"


def expected_for_language(lang: str) -> list[ExpectedDeck]:
    toc = load_toc(lang)
    expected: list[ExpectedDeck] = []

    root_file = toc.get("root")
    if root_file:
        expected.append(
            ExpectedDeck(
                lang=lang,
                position="root",
                book_file=root_file,
                slide_file=slide_path_for_book_file(root_file),
            )
        )

    for part_index, part in enumerate(toc.get("parts", []) or []):
        for chapter_index, chapter in enumerate(part.get("chapters", []) or []):
            chapter_file = chapter.get("file")
            if not chapter_file:
                continue
            expected.append(
                ExpectedDeck(
                    lang=lang,
                    position=f"p{part_index}/c{chapter_index}",
                    book_file=chapter_file,
                    slide_file=slide_path_for_book_file(chapter_file),
                )
            )
    return expected


def find_orphan_decks(expected_paths: set[Path], languages: list[str]) -> list[Path]:
    orphans: list[Path] = []
    for lang in languages:
        lang_dir = SLIDES_DIR / lang
        if not lang_dir.is_dir():
            continue
        for slide_file in lang_dir.rglob("slides.md"):
            if slide_file not in expected_paths:
                orphans.append(slide_file)
    return sorted(orphans)


def validate() -> list[str]:
    errors: list[str] = []
    languages = detect_languages()
    if not languages:
        return ["No se han detectado idiomas en book/_config_<lang>.yml."]
    if not SLIDES_DIR.is_dir():
        return ["No existe la carpeta slides/."]

    expected_by_lang = {lang: expected_for_language(lang) for lang in languages}
    reference_lang = languages[0]
    reference_positions = [deck.position for deck in expected_by_lang[reference_lang]]

    for lang, expected in expected_by_lang.items():
        positions = [deck.position for deck in expected]
        if positions != reference_positions:
            errors.append(
                f"La estructura de posiciones de {lang} no coincide con {reference_lang}."
            )
        for deck in expected:
            if not deck.slide_file.is_file():
                errors.append(
                    "Falta deck esperada: "
                    f"{deck.slide_file.relative_to(PROJECT_ROOT)} "
                    f"({deck.position}, {deck.book_file})."
                )

    expected_paths = {
        deck.slide_file
        for expected in expected_by_lang.values()
        for deck in expected
    }
    for orphan in find_orphan_decks(expected_paths, languages):
        errors.append(f"Deck huerfana: {orphan.relative_to(PROJECT_ROOT)}.")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Comprueba integridad Slidev multiidioma.")
    parser.add_argument("--quiet", action="store_true", help="Muestra solo errores.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate()
    if errors:
        print("ERROR: integridad Slidev fallida.")
        for error in errors:
            print(f"  - {error}")
        print("Ejecuta: python scripts/sync_slide_templates.py")
        return 1
    if not args.quiet:
        print("Integridad Slidev correcta.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
