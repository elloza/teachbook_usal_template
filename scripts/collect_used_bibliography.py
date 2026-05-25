"""Collect cited BibTeX entries from TeachBook source files.

The script keeps `book/_static/references.bib` as the source of truth, validates
that every MyST citation key exists, and can write a reduced BibTeX file with
only the entries used by one language.  It also collects LaTeX citations inside
`{raw} latex` fallbacks so PDF-only alternatives contribute to the final PDF
bibliography.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from pybtex.database import BibliographyData, parse_file
from pybtex.database.output.bibtex import Writer


if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BIB_FILE = PROJECT_ROOT / "book" / "_static" / "references.bib"
CITE_RE = re.compile(r"(?<!`)\{cite(?::[^}\s]+)?\}`([^`\n]+)`")
LATEX_CITE_RE = re.compile(
    r"\\(?:cite|citep|citet|parencite|textcite|autocite|footcite)"
    r"(?:\[[^\]]*\]){0,2}\{([^}]+)\}"
)
FENCE_RE = re.compile(r"^\s*([`~]{3,})(.*)$")
SKIPPED_DIRECTIVES = {
    "bibliography",
    "code-block",
    "code-cell",
    "eval-rst",
    "kroki",
    "literalinclude",
}


class BibliographyError(RuntimeError):
    """Raised when bibliography validation cannot continue."""


@dataclass(frozen=True)
class CitationUse:
    key: str
    source: Path
    line: int
    note: str = ""

    def label(self) -> str:
        rel = self.source
        try:
            rel = self.source.relative_to(PROJECT_ROOT)
        except ValueError:
            pass
        suffix = f" ({self.note})" if self.note else ""
        return f"{rel.as_posix()}:{self.line}{suffix}"


@dataclass
class Fence:
    char: str
    length: int
    mode: str


@dataclass
class BibliographyResult:
    content_dir: Path
    bib_file: Path
    citation_count: int
    used_keys: list[str]
    output_file: Path | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate MyST citation keys and optionally write a used-only BibTeX file."
    )
    parser.add_argument(
        "--lang",
        help="Language code to scan, for example es or en. Used when --content-dir is omitted.",
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        help="Directory containing .md/.ipynb sources to scan.",
    )
    parser.add_argument(
        "--bib-file",
        type=Path,
        default=DEFAULT_BIB_FILE,
        help="Master BibTeX file. Defaults to book/_static/references.bib.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output BibTeX file containing only used entries.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print errors.",
    )
    return parser.parse_args()


def resolve_content_dir(lang: str | None, content_dir: Path | None) -> Path:
    if content_dir:
        return content_dir.resolve()
    if not lang:
        raise BibliographyError("Use --lang or --content-dir to choose what to scan.")
    if lang == "default":
        return (PROJECT_ROOT / "book").resolve()
    return (PROJECT_ROOT / "book" / lang).resolve()


def get_myst_directive(info: str) -> tuple[str | None, str]:
    stripped = info.strip()
    if not stripped or not stripped.startswith("{"):
        return None, ""
    if "}" not in stripped:
        return None, ""
    directive = stripped[1:].split("}", 1)[0].strip().split()[0]
    argument = stripped.split("}", 1)[1].strip()
    return directive, argument


def fence_scan_mode(info: str) -> str:
    directive, argument = get_myst_directive(info)
    if directive is None:
        return "skip"
    if directive == "raw":
        raw_format = argument.split(None, 1)[0].lower() if argument else ""
        return "latex" if raw_format in {"latex", "tex"} else "skip"
    if directive in SKIPPED_DIRECTIVES:
        return "skip"
    return "markdown"


def current_scan_mode(stack: list[Fence]) -> str:
    if not stack:
        return "markdown"
    return stack[-1].mode


def iter_citation_lines(text: str) -> list[tuple[int, str, str]]:
    stack: list[Fence] = []
    scannable: list[tuple[int, str, str]] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            fence_text = fence_match.group(1)
            info = fence_match.group(2).strip()
            fence_char = fence_text[0]
            fence_len = len(fence_text)

            if (
                stack
                and fence_char == stack[-1].char
                and fence_len >= stack[-1].length
                and not info
            ):
                stack.pop()
                continue

            if current_scan_mode(stack) != "skip":
                stack.append(
                    Fence(
                        char=fence_char,
                        length=fence_len,
                        mode=fence_scan_mode(info),
                    )
                )
            continue

        mode = current_scan_mode(stack)
        if mode != "skip":
            scannable.append((line_number, mode, line))

    return scannable


def split_citation_keys(raw_keys: str) -> list[str]:
    keys = []
    for raw_key in raw_keys.split(","):
        key = raw_key.strip()
        if key:
            keys.append(key)
    return keys


def collect_citations_from_markdown(text: str, source: Path, note: str = "") -> list[CitationUse]:
    uses: list[CitationUse] = []
    for line_number, mode, line in iter_citation_lines(text):
        if mode == "markdown":
            pattern = CITE_RE
        elif mode == "latex":
            pattern = LATEX_CITE_RE
        else:
            continue
        for match in pattern.finditer(line):
            for key in split_citation_keys(match.group(1)):
                cite_note = note
                if mode == "latex":
                    cite_note = f"{note}; raw latex".strip("; ")
                uses.append(
                    CitationUse(key=key, source=source, line=line_number, note=cite_note)
                )
    return uses


def collect_citations_from_notebook(path: Path) -> list[CitationUse]:
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BibliographyError(f"No se pudo leer el notebook {path}: {exc}") from exc

    uses: list[CitationUse] = []
    for index, cell in enumerate(notebook.get("cells", []), start=1):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        uses.extend(
            collect_citations_from_markdown(source, path, note=f"cell {index}")
        )
    return uses


def iter_source_files(content_dir: Path) -> list[Path]:
    if not content_dir.exists():
        raise BibliographyError(f"No existe el directorio de contenido: {content_dir}")

    files: list[Path] = []
    for path in content_dir.rglob("*"):
        if path.is_dir():
            continue
        if any(part in {"_build", ".ipynb_checkpoints"} for part in path.parts):
            continue
        if path.suffix.lower() in {".md", ".ipynb"}:
            files.append(path)
    return sorted(files)


def collect_citations(content_dir: Path) -> list[CitationUse]:
    uses: list[CitationUse] = []
    for path in iter_source_files(content_dir):
        if path.suffix.lower() == ".md":
            uses.extend(
                collect_citations_from_markdown(path.read_text(encoding="utf-8"), path)
            )
        elif path.suffix.lower() == ".ipynb":
            uses.extend(collect_citations_from_notebook(path))
    return uses


def find_duplicate_bib_keys(bib_file: Path) -> dict[str, list[int]]:
    key_lines: dict[str, list[int]] = {}
    entry_re = re.compile(r"^\s*@\w+\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)
    for line_number, line in enumerate(bib_file.read_text(encoding="utf-8").splitlines(), start=1):
        match = entry_re.match(line)
        if match:
            key_lines.setdefault(match.group(1), []).append(line_number)
    return {key: lines for key, lines in key_lines.items() if len(lines) > 1}


def load_bib_database(bib_file: Path) -> BibliographyData:
    if not bib_file.exists():
        raise BibliographyError(f"No existe el archivo BibTeX: {bib_file}")

    duplicates = find_duplicate_bib_keys(bib_file)
    if duplicates:
        details = "\n".join(
            f"  - {key}: lineas {', '.join(str(line) for line in lines)}"
            for key, lines in sorted(duplicates.items())
        )
        raise BibliographyError(f"Hay claves BibTeX duplicadas en {bib_file}:\n{details}")

    return parse_file(str(bib_file), bib_format="bibtex")


def unique_keys_in_order(uses: list[CitationUse]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for use in uses:
        if use.key not in seen:
            seen.add(use.key)
            ordered.append(use.key)
    return ordered


def validate_keys(uses: list[CitationUse], available_keys: set[str], bib_file: Path) -> None:
    missing: dict[str, list[CitationUse]] = {}
    for use in uses:
        if use.key not in available_keys:
            missing.setdefault(use.key, []).append(use)

    if not missing:
        return

    lines = [f"Hay citas sin entrada en {bib_file}:"]
    for key, key_uses in sorted(missing.items()):
        locations = ", ".join(use.label() for use in key_uses[:5])
        if len(key_uses) > 5:
            locations += f", ... ({len(key_uses)} usos)"
        lines.append(f"  - {key}: {locations}")
    raise BibliographyError("\n".join(lines))


def write_used_bib(bib_data: BibliographyData, used_keys: list[str], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    selected_entries = {
        key: bib_data.entries[key]
        for key in used_keys
        if key in bib_data.entries
    }
    used_data = BibliographyData(entries=selected_entries)
    if selected_entries:
        Writer().write_file(used_data, str(output_file))
    else:
        output_file.write_text(
            "% Auto-generated by scripts/collect_used_bibliography.py\n",
            encoding="utf-8",
            newline="\n",
        )


def collect_used_bibliography(
    content_dir: Path,
    bib_file: Path,
    output_file: Path | None = None,
) -> BibliographyResult:
    content_dir = content_dir.resolve()
    bib_file = bib_file.resolve()
    output_file = output_file.resolve() if output_file else None

    bib_data = load_bib_database(bib_file)
    uses = collect_citations(content_dir)
    used_keys = unique_keys_in_order(uses)
    validate_keys(uses, set(bib_data.entries), bib_file)

    if output_file:
        write_used_bib(bib_data, used_keys, output_file)

    return BibliographyResult(
        content_dir=content_dir,
        bib_file=bib_file,
        citation_count=len(uses),
        used_keys=used_keys,
        output_file=output_file,
    )


def main() -> int:
    args = parse_args()
    try:
        content_dir = resolve_content_dir(args.lang, args.content_dir)
        result = collect_used_bibliography(
            content_dir=content_dir,
            bib_file=args.bib_file,
            output_file=args.output,
        )
    except BibliographyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not args.quiet:
        lang_label = args.lang or result.content_dir.name
        print(
            f"Bibliografia {lang_label}: "
            f"{result.citation_count} cita(s), "
            f"{len(result.used_keys)} clave(s) usadas."
        )
        if result.output_file:
            print(f"BibTeX usado generado en: {result.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
