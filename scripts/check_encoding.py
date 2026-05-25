#!/usr/bin/env python3
"""Validate UTF-8 text files and detect common mojibake.

This project intentionally contains Spanish text with accents and symbols.  A
file may be valid UTF-8 and still be wrong if it contains mojibake produced by
decoding UTF-8 bytes as Latin-1 or Windows-1252.  This script catches both
cases before the broken text reaches the book.
"""

from __future__ import annotations

import io
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TEXT_SUFFIXES = {
    ".bib",
    ".css",
    ".ipynb",
    ".js",
    ".json",
    ".md",
    ".mermaid",
    ".py",
    ".tex",
    ".txt",
    ".yaml",
    ".yml",
}

SUSPICIOUS_SEQUENCES = {
    "\ufffd": "caracter de reemplazo U+FFFD",
    "\u00c3": "mojibake típico de acentos UTF-8 leídos como Latin-1/Windows-1252",
    "\u00c2": "mojibake típico de signos o espacios UTF-8 leídos como Latin-1/Windows-1252",
    "\u00e2\u20ac": "mojibake típico de comillas, guiones o puntos suspensivos",
    "\u00e2\u0153": "mojibake típico de símbolos como checks",
    "\u00f0\u0178": "mojibake típico de emojis",
}

BROKEN_QUESTION_RE = re.compile(
    r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü]\?[A-Za-zÁÉÍÓÚáéíóúÑñÜü]"
)


@dataclass(frozen=True)
class EncodingIssue:
    path: Path
    reason: str
    line_number: int | None = None
    excerpt: str | None = None


def force_utf8_stdio() -> None:
    """Make diagnostics readable when launched from Windows consoles/agents."""
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def project_files() -> list[Path]:
    """Return tracked and untracked project files, honoring .gitignore."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        return [
            PROJECT_ROOT / line
            for line in result.stdout.splitlines()
            if line and (PROJECT_ROOT / line).exists()
        ]
    except Exception:
        skipped = {".git", ".venv", "_build", "__pycache__", ".build_logs", "latex_exports"}
        files: list[Path] = []
        for path in PROJECT_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skipped or part.startswith("_temp_build_") for part in path.parts):
                continue
            files.append(path)
        return files


def line_for_offset(text: str, offset: int) -> tuple[int, str]:
    line_number = text.count("\n", 0, offset) + 1
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    if line_end == -1:
        line_end = len(text)
    return line_number, text[line_start:line_end].strip()


def is_expected_question_mark_context(line: str) -> bool:
    """Skip URL query strings such as watch?v=... and cache busters."""
    return "http" in line or "?v=" in line


def scan_file(path: Path) -> list[EncodingIssue]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return []

    relative = path.relative_to(PROJECT_ROOT)
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [
            EncodingIssue(
                relative,
                f"no es UTF-8 válido: {exc}",
                None,
                None,
            )
        ]

    issues: list[EncodingIssue] = []
    for token, reason in SUSPICIOUS_SEQUENCES.items():
        index = text.find(token)
        if index != -1:
            line_number, excerpt = line_for_offset(text, index)
            issues.append(EncodingIssue(relative, reason, line_number, excerpt))

    for line_number, line in enumerate(text.splitlines(), start=1):
        if BROKEN_QUESTION_RE.search(line) and not is_expected_question_mark_context(line):
            issues.append(
                EncodingIssue(
                    relative,
                    "posible acento sustituido por '?' dentro de una palabra",
                    line_number,
                    line.strip(),
                )
            )
            break

    if path.suffix.lower() == ".ipynb":
        issues.extend(scan_notebook_code_cells(relative, text))
    return issues


def scan_notebook_code_cells(relative: Path, text: str) -> list[EncodingIssue]:
    """Notebook Markdown may use accents; code cells must stay ASCII-safe."""
    try:
        notebook = json.loads(text)
    except json.JSONDecodeError as exc:
        return [EncodingIssue(relative, f"notebook JSON inválido: {exc}", None, None)]

    issues: list[EncodingIssue] = []
    for index, cell in enumerate(notebook.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            source_text = "".join(source)
        else:
            source_text = str(source)
        bad_chars = sorted({char for char in source_text if ord(char) > 127})
        if bad_chars:
            escaped = "".join(bad_chars).encode("ascii", "backslashreplace").decode("ascii")
            issues.append(
                EncodingIssue(
                    relative,
                    "celda de código con texto no ASCII; usa ASCII en labels, títulos, prints y comentarios de Python",
                    None,
                    f"celda {index}: caracteres {escaped}",
                )
            )
        if "===" in source_text:
            issues.append(
                EncodingIssue(
                    relative,
                    "celda de código con '==='; revisa si viene de una sustitución incorrecta de símbolos o acentos",
                    None,
                    f"celda {index}",
                )
            )
    return issues


def scan_project() -> tuple[int, list[EncodingIssue]]:
    checked = 0
    issues: list[EncodingIssue] = []
    for path in project_files():
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        checked += 1
        issues.extend(scan_file(path))
    return checked, issues


def main() -> int:
    force_utf8_stdio()
    checked, issues = scan_project()
    if not issues:
        print(f"✅ Codificación OK: {checked} archivos de texto en UTF-8, sin mojibake detectado.")
        return 0

    print("❌ Problemas de codificación detectados:")
    for issue in issues:
        where = f"{issue.path}"
        if issue.line_number is not None:
            where += f":{issue.line_number}"
        print(f"   - {where}: {issue.reason}")
        if issue.excerpt:
            print(f"     {issue.excerpt}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
