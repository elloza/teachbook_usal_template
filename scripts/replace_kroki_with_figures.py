#!/usr/bin/env python3
"""Replace rendered Kroki blocks with static MyST figure blocks.

This is the final step of the static-diagram workflow. It reads
``diagram_sources/manifest.json`` created by ``extract_kroki_sources.py`` and
replaces only the diagram blocks whose rendered SVG exists.

The script is deliberately conservative:

- it does not modify files in ``--dry-run`` mode;
- by default it skips entries whose expected image does not exist;
- it verifies that the target block still starts at the manifest line;
- it leaves examples inside literal Markdown fences untouched because the
  extractor never included them in the manifest.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "diagram_sources" / "manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replace extracted {kroki} blocks with static {figure} blocks."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to diagram_sources/manifest.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report replacements without modifying Markdown files.",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Replace even if the generated image does not exist yet. Not recommended.",
    )
    return parser.parse_args()


def slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value.lower()).strip("-") or "diagram"


def load_manifest(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Ejecuta primero: python scripts/extract_kroki_sources.py"
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("El manifest de extracción debe ser una lista.")
    return data


def find_kroki_block(lines: list[str], start_line: int) -> tuple[int, int] | None:
    """Return [start, end) indexes for a kroki block near a 1-based line."""
    start_index = start_line - 1
    search_from = max(0, start_index - 2)
    search_to = min(len(lines), start_index + 3)

    block_start = None
    for index in range(search_from, search_to):
        if lines[index].strip() == "```{kroki}":
            block_start = index
            break

    if block_start is None:
        return None

    for index in range(block_start + 1, len(lines)):
        if lines[index].strip() == "```":
            return block_start, index + 1
    return None


def remove_nearby_textual_caption(lines: list[str], block_start: int) -> int:
    """Remove generated textual intro/caption immediately before a kroki block.

    Returns the new block_start index after deletions.
    """
    start = block_start
    cursor = block_start - 1
    while cursor >= 0 and lines[cursor].strip() == "":
        cursor -= 1

    if cursor >= 0 and re.match(r"^\*\*(Diagrama|Diagram)[:.].+\*\*$", lines[cursor].strip()):
        delete_from = cursor
        cursor -= 1
        while cursor >= 0 and lines[cursor].strip() == "":
            delete_from = cursor
            cursor -= 1
        if cursor >= 0 and re.search(r"(diagrama siguiente|following diagram)", lines[cursor], re.I):
            delete_from = cursor
        del lines[delete_from:block_start]
        start = delete_from
    return start


def build_figure_block(item: dict[str, object]) -> list[str]:
    image_path = str(item["suggested_figure_path"])
    expected_output = Path(str(item["expected_output"]))
    caption = str(item.get("caption") or "Diagrama generado desde código.")
    language = str(item.get("language") or "es")
    label_prefix = "fig-diagram" if language == "en" else "fig-diagrama"
    label = f"{label_prefix}-{slug(expected_output.stem)}"
    alt = caption.strip(".*")

    return [
        f"Como muestra la {{numref}}`{label}`, el diagrama queda versionado como imagen estática." if language == "es" else f"As shown in {{numref}}`{label}`, the diagram is versioned as a static image.",
        "",
        f"```{{figure}} {image_path}",
        f":name: {label}",
        f":alt: {alt}",
        ":width: 90%",
        ":align: center",
        "",
        caption,
        "```",
    ]


def main() -> int:
    args = parse_args()
    manifest = load_manifest(args.manifest.resolve())

    grouped: dict[Path, list[dict[str, object]]] = {}
    skipped_missing = 0
    for item in manifest:
        output = PROJECT_ROOT / str(item["expected_output"])
        if not output.exists() and not args.allow_missing:
            skipped_missing += 1
            continue
        markdown = PROJECT_ROOT / str(item["source_markdown"])
        grouped.setdefault(markdown, []).append(item)

    replacements = 0
    skipped_mismatch = 0

    for markdown, items in grouped.items():
        lines = markdown.read_text(encoding="utf-8").splitlines()
        # Work from bottom to top so line numbers remain valid.
        for item in sorted(items, key=lambda entry: int(entry["line"]), reverse=True):
            found = find_kroki_block(lines, int(item["line"]))
            if found is None:
                skipped_mismatch += 1
                continue
            block_start, block_end = found
            block_start = remove_nearby_textual_caption(lines, block_start)
            lines[block_start:block_end] = build_figure_block(item)
            replacements += 1

        if not args.dry_run:
            markdown.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")

    print(f"Reemplazos posibles: {replacements}")
    print(f"Omitidos por imagen inexistente: {skipped_missing}")
    print(f"Omitidos por no encontrar bloque esperado: {skipped_mismatch}")
    if args.dry_run:
        print("Dry-run completado. No se han modificado archivos.")
    return 0 if skipped_mismatch == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
