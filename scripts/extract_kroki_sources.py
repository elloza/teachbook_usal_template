#!/usr/bin/env python3
"""Extract existing MyST ``kroki`` blocks into versioned source files.

This is the first half of the static-diagram workflow:

1. Extract editable diagram sources from ``book/es`` and ``book/en``.
2. Render those sources with ``scripts/render_diagrams.py``.
3. Replace important ``kroki`` blocks with normal ``figure`` blocks that point
   to the generated images.

The extractor does NOT modify book content. It only creates files under
``diagram_sources/`` and writes a manifest with enough metadata to review or
automate a later replacement step.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, asdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "diagram_sources"

TYPE_TO_EXTENSION = {
    "mermaid": ".mermaid",
    "plantuml": ".plantuml",
    "graphviz": ".graphviz",
    "wavedrom": ".wavedrom",
    "structurizr": ".structurizr",
    "d2": ".d2",
    "vega": ".vega",
    "vegalite": ".vegalite",
    "tikz": ".tikz",
}


@dataclass(frozen=True)
class ExtractedDiagram:
    source_markdown: str
    line: int
    language: str
    diagram_type: str
    source_file: str
    expected_output: str
    suggested_figure_path: str
    caption: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract book {kroki} blocks into diagram_sources/."
    )
    parser.add_argument(
        "--book-dir",
        type=Path,
        default=BOOK_DIR,
        help="Book directory to scan (default: book/).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where sources will be written (default: diagram_sources/).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing extracted sources.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be extracted without writing files.",
    )
    return parser.parse_args()


def slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "_", ascii_value.lower()).strip("_") or "diagram"


def parse_options(option_lines: list[str]) -> dict[str, str]:
    options: dict[str, str] = {}
    for line in option_lines:
        match = re.match(r"^:([^:]+):\s*(.*)$", line.strip())
        if match:
            options[match.group(1)] = match.group(2).strip()
    return options


def detect_caption(lines: list[str], start_index: int, language: str) -> str:
    for index in range(start_index - 1, max(-1, start_index - 8), -1):
        candidate = lines[index].strip()
        match = re.match(r"^\*\*(.+?)\*\*$", candidate)
        if match:
            return match.group(1).strip()
    return "Diagrama generado desde código." if language == "es" else "Diagram generated from code."


def compute_markdown_relative_path(markdown_path: Path, output_path: Path) -> str:
    """Return a POSIX relative path from a Markdown file to an output image."""
    return Path(os.path.relpath(output_path, markdown_path.parent)).as_posix()


def extract_from_file(markdown_path: Path, output_dir: Path, force: bool, dry_run: bool) -> list[ExtractedDiagram]:
    text = markdown_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    language = "es" if f"{os.sep}es{os.sep}" in str(markdown_path) else "en"
    extracted: list[ExtractedDiagram] = []
    literal_fence: str | None = None
    diagram_index = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        fence_match = re.match(r"^(`{3,})(.*)$", line)

        if literal_fence:
            if line.startswith(literal_fence):
                literal_fence = None
            i += 1
            continue

        if fence_match and len(fence_match.group(1)) >= 4:
            literal_fence = fence_match.group(1)
            i += 1
            continue

        if line.strip() != "```{kroki}":
            i += 1
            continue

        start_line = i + 1
        option_lines: list[str] = []
        source_lines: list[str] = []
        i += 1

        while i < len(lines) and lines[i].startswith(":"):
            option_lines.append(lines[i])
            i += 1

        if i < len(lines) and lines[i].strip() == "":
            i += 1

        while i < len(lines) and lines[i].strip() != "```":
            source_lines.append(lines[i])
            i += 1

        # Skip closing fence.
        if i < len(lines) and lines[i].strip() == "```":
            i += 1

        options = parse_options(option_lines)
        diagram_type = options.get("type", "mermaid").lower()
        extension = TYPE_TO_EXTENSION.get(diagram_type, f".{diagram_type}")
        diagram_index += 1

        relative_markdown = markdown_path.relative_to(BOOK_DIR / language)
        base_name = f"{slug(relative_markdown.with_suffix('').as_posix())}_{diagram_index:02d}"
        source_file = output_dir / language / f"{base_name}{extension}"
        # Keep SVG as the book-facing artifact: HTML stays crisp and PDF export
        # converts SVG to a LaTeX-safe vector PDF whenever possible.
        expected_output = PROJECT_ROOT / "book" / "_static" / "generated" / "diagrams" / language / f"{base_name}.svg"
        caption = detect_caption(lines, start_line - 1, language)

        if not dry_run:
            source_file.parent.mkdir(parents=True, exist_ok=True)
            if force or not source_file.exists():
                source_file.write_text("\n".join(source_lines).rstrip() + "\n", encoding="utf-8", newline="\n")

        extracted.append(
            ExtractedDiagram(
                source_markdown=str(markdown_path.relative_to(PROJECT_ROOT)),
                line=start_line,
                language=language,
                diagram_type=diagram_type,
                source_file=str(source_file.relative_to(PROJECT_ROOT)),
                expected_output=str(expected_output.relative_to(PROJECT_ROOT)),
                suggested_figure_path=compute_markdown_relative_path(markdown_path, expected_output),
                caption=caption,
            )
        )

    return extracted


def main() -> int:
    args = parse_args()
    book_dir = args.book_dir.resolve()
    output_dir = args.output_dir.resolve()

    all_extracted: list[ExtractedDiagram] = []
    for language in ("es", "en"):
        language_dir = book_dir / language
        if not language_dir.exists():
            continue
        for markdown_path in sorted(language_dir.rglob("*.md")):
            all_extracted.extend(
                extract_from_file(markdown_path, output_dir, args.force, args.dry_run)
            )

    if not all_extracted:
        print("ℹ️  No se han encontrado bloques {kroki} reales fuera de ejemplos literales.")
        return 0

    print(f"🧩 Bloques Kroki detectados: {len(all_extracted)}")
    for item in all_extracted:
        print(
            f"   - {item.source_markdown}:{item.line} -> {item.source_file} "
            f"({item.diagram_type})"
        )

    if args.dry_run:
        print("✅ Dry-run completado. No se han escrito fuentes.")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps([asdict(item) for item in all_extracted], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"✅ Manifest escrito en: {manifest_path.relative_to(PROJECT_ROOT)}")
    print("Siguiente paso: python scripts/render_diagrams.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
