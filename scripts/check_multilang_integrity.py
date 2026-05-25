#!/usr/bin/env python3
"""Check that all TeachBook languages expose the same content structure.

The project is multi-language: every visible page in one language must have a
corresponding page in the other languages, in the same sidebar position.  This
script validates the TOC structure, missing files, and orphan content files.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

from check_encoding import force_utf8_stdio, scan_project


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"


def configured_languages() -> list[str]:
    languages = []
    for config in sorted(BOOK_DIR.glob("_config_*.yml")):
        languages.append(config.stem.replace("_config_", ""))
    return languages


def load_toc(language: str) -> dict[str, Any]:
    toc_path = BOOK_DIR / f"_toc_{language}.yml"
    if not toc_path.exists():
        raise FileNotFoundError(f"Falta {toc_path.relative_to(PROJECT_ROOT)}")
    return yaml.safe_load(toc_path.read_text(encoding="utf-8"))


def toc_entries(toc: dict[str, Any]) -> list[tuple[str, str]]:
    entries = [("root", toc["root"])]

    def walk(item: dict[str, Any], position: str) -> None:
        if "file" in item:
            entries.append((position, item["file"]))
        for index, section in enumerate(item.get("sections", []) or []):
            walk(section, f"{position}/s{index}")

    for part_index, part in enumerate(toc.get("parts", []) or []):
        for chapter_index, chapter in enumerate(part.get("chapters", []) or []):
            walk(chapter, f"p{part_index}/c{chapter_index}")
    return entries


def toc_shape(toc: dict[str, Any]) -> list[list[int]]:
    return [
        [len(chapter.get("sections", []) or []) for chapter in part.get("chapters", []) or []]
        for part in toc.get("parts", []) or []
    ]


def content_files(language: str) -> set[str]:
    files: set[str] = set()
    lang_dir = BOOK_DIR / language
    for suffix in ("*.md", "*.ipynb"):
        for path in lang_dir.rglob(suffix):
            files.add(path.relative_to(BOOK_DIR).with_suffix("").as_posix())
    return files


def entry_exists(entry: str) -> bool:
    return (BOOK_DIR / f"{entry}.md").exists() or (BOOK_DIR / f"{entry}.ipynb").exists()


def main() -> int:
    force_utf8_stdio()
    languages = configured_languages()
    encoding_checked, encoding_issues = scan_project()
    if encoding_issues:
        print("❌ Problemas de codificación detectados:")
        for issue in encoding_issues:
            where = f"{issue.path}"
            if issue.line_number is not None:
                where += f":{issue.line_number}"
            print(f"   - {where}: {issue.reason}")
            if issue.excerpt:
                print(f"     {issue.excerpt}")
        return 1
    print(f"✅ Codificación UTF-8 OK ({encoding_checked} archivos de texto revisados).")

    if len(languages) < 2:
        print("ℹ️  Solo hay un idioma configurado; no hay correspondencia multi-idioma que validar.")
        return 0

    print(f"🌐 Idiomas configurados: {', '.join(languages)}")
    tocs = {language: load_toc(language) for language in languages}
    reference_language = languages[0]
    reference_shape = toc_shape(tocs[reference_language])
    ok = True

    for language in languages:
        shape = toc_shape(tocs[language])
        if shape != reference_shape:
            ok = False
            print(f"❌ Estructura TOC distinta en {language}: {shape} != {reference_shape}")

    flat_entries = {language: toc_entries(toc) for language, toc in tocs.items()}
    reference_positions = [position for position, _ in flat_entries[reference_language]]
    for language, entries in flat_entries.items():
        positions = [position for position, _ in entries]
        if positions != reference_positions:
            ok = False
            print(f"❌ Posiciones del menú distintas en {language}")

    for language, entries in flat_entries.items():
        referenced = {entry for _, entry in entries}
        missing = sorted(entry for entry in referenced if not entry_exists(entry))
        orphans = sorted(content_files(language) - referenced)
        if missing:
            ok = False
            print(f"❌ Entradas TOC sin archivo en {language}:")
            for item in missing:
                print(f"   - {item}")
        if orphans:
            ok = False
            print(f"❌ Archivos huérfanos no visibles en el TOC de {language}:")
            for item in orphans:
                print(f"   - {item}")
        if not missing and not orphans:
            print(f"✅ {language}: {len(referenced)} entradas visibles, sin roturas ni huérfanos")

    if not ok:
        print("\n🛑 La estructura multi-idioma NO es consistente.")
        return 1

    print("\n✅ Estructura multi-idioma consistente: mismos menús, mismo orden y archivos completos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
