#!/usr/bin/env python3
"""Audit and safely optimize static assets used by the TeachBook.

The script keeps the original file format and path. It only replaces an image
when Pillow can re-open the optimized bytes and the result is smaller.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image
except ImportError:  # pragma: no cover - user-facing diagnostic
    Image = None  # type: ignore[assignment]


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"
STATIC_DIR = BOOK_DIR / "_static"
REPORT_DEFAULT = PROJECT_ROOT / ".build_logs" / "static_assets.json"
OPTIMIZABLE_SUFFIXES = {".png", ".jpg", ".jpeg"}
AUDIT_SUFFIXES = OPTIMIZABLE_SUFFIXES | {
    ".gif",
    ".svg",
    ".webp",
    ".mp4",
    ".pdf",
    ".wav",
    ".mp3",
    ".ogg",
    ".m4a",
}
GIF_REFERENCE_PATTERN = re.compile(r"(?P<path>[^\s<>\"')]+\.gif)", re.IGNORECASE)
MIN_SAVING_BYTES = 1024


@dataclass
class AssetRecord:
    path: str
    suffix: str
    before_bytes: int
    after_bytes: int | None = None
    saved_bytes: int = 0
    status: str = "scanned"
    detail: str = ""


@dataclass
class MissingGifFallback:
    source: str
    gif: str
    expected_png: str


def force_utf8_stdio() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        if stream.encoding and stream.encoding.lower() in {"utf-8", "utf8"}:
            continue
        wrapped = io.TextIOWrapper(stream.buffer, encoding="utf-8", errors="replace")
        setattr(sys, stream_name, wrapped)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit and conservatively optimize files under book/_static."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="Only report issues and exit with error if optimization is pending.",
    )
    mode.add_argument(
        "--fix",
        action="store_true",
        help="Optimize safe PNG/JPG assets in place when the output is smaller.",
    )
    parser.add_argument(
        "--static-dir",
        type=Path,
        default=STATIC_DIR,
        help="Static asset directory to scan (default: book/_static).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Optional JSON report path, e.g. .build_logs/static_assets.json.",
    )
    return parser.parse_args()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def iter_assets(static_dir: Path) -> Iterable[Path]:
    if not static_dir.exists():
        return []
    return (
        path
        for path in sorted(static_dir.rglob("*"))
        if path.is_file() and path.suffix.lower() in AUDIT_SUFFIXES
    )


def optimize_png(image: Image.Image) -> bytes:
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True)
    return out.getvalue()


def optimize_jpeg(image: Image.Image) -> bytes:
    out = io.BytesIO()
    save_kwargs: dict[str, object] = {
        "format": "JPEG",
        "optimize": True,
        "progressive": True,
    }
    try:
        image.save(out, quality="keep", subsampling="keep", **save_kwargs)
    except Exception:
        out = io.BytesIO()
        image.save(out, quality=95, **save_kwargs)
    return out.getvalue()


def validate_image_bytes(original: Path, candidate: bytes) -> tuple[bool, str]:
    before = Image.open(original)
    before.load()
    before_size = before.size
    before_frames = getattr(before, "n_frames", 1)
    before_format = before.format

    after = Image.open(io.BytesIO(candidate))
    after.load()
    after_size = after.size
    after_frames = getattr(after, "n_frames", 1)
    after_format = after.format

    if after_size != before_size:
        return False, f"dimensiones cambiadas: {before_size} -> {after_size}"
    if after_frames != before_frames:
        return False, f"fotogramas cambiados: {before_frames} -> {after_frames}"
    if after_format != before_format:
        return False, f"formato cambiado: {before_format} -> {after_format}"
    return True, ""


def optimized_bytes(path: Path) -> bytes:
    with Image.open(path) as image:
        image.load()
        suffix = path.suffix.lower()
        if suffix == ".png":
            return optimize_png(image)
        if suffix in {".jpg", ".jpeg"}:
            return optimize_jpeg(image)
    raise ValueError(f"Formato no optimizable: {path.suffix}")


def scan_asset(path: Path, fix: bool) -> AssetRecord:
    suffix = path.suffix.lower()
    before = path.stat().st_size
    record = AssetRecord(
        path=relative(path),
        suffix=suffix,
        before_bytes=before,
        after_bytes=before,
    )

    if suffix not in OPTIMIZABLE_SUFFIXES:
        record.status = "audit-only"
        record.detail = "formato no modificado por esta herramienta"
        return record

    try:
        candidate = optimized_bytes(path)
        valid, detail = validate_image_bytes(path, candidate)
    except Exception as exc:
        record.status = "error"
        record.detail = str(exc)
        return record

    if not valid:
        record.status = "skipped"
        record.detail = detail
        return record

    after = len(candidate)
    record.after_bytes = after
    if after >= before:
        record.status = "already-optimal"
        return record

    record.saved_bytes = before - after
    if record.saved_bytes < MIN_SAVING_BYTES:
        record.status = "already-optimal"
        record.detail = (
            f"ahorro menor que {MIN_SAVING_BYTES} bytes; "
            "se ignora para evitar diferencias entre sistemas"
        )
        record.saved_bytes = 0
        return record

    if fix:
        path.write_bytes(candidate)
        record.status = "optimized"
    else:
        record.status = "optimizable"
    return record


def iter_content_files() -> Iterable[Path]:
    ignored_parts = {"_build", ".ipynb_checkpoints"}
    suffixes = {".md", ".ipynb", ".yml", ".yaml", ".html"}
    for path in sorted(BOOK_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        yield path


def resolve_gif_reference(source: Path, ref: str) -> Path | None:
    if ref.startswith(("http://", "https://", "data:")):
        return None
    normalized = ref.replace("\\", "/").split("#", 1)[0].split("?", 1)[0]
    if "_static/" in normalized:
        static_rel = normalized.split("_static/", 1)[1]
        return STATIC_DIR / static_rel
    return (source.parent / normalized).resolve()


def scan_gif_fallbacks() -> list[MissingGifFallback]:
    missing: list[MissingGifFallback] = []
    seen: set[tuple[str, str]] = set()
    for source in iter_content_files():
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line in text.splitlines():
            if ".gif" not in line.lower():
                continue
            for match in GIF_REFERENCE_PATTERN.finditer(line):
                ref = match.group("path")
                gif_path = resolve_gif_reference(source, ref)
                if gif_path is None:
                    continue
                png_path = gif_path.with_suffix(".png")
                key = (relative(source), relative(gif_path))
                if key in seen:
                    continue
                seen.add(key)
                if not png_path.exists():
                    missing.append(
                        MissingGifFallback(
                            source=relative(source),
                            gif=relative(gif_path),
                            expected_png=relative(png_path),
                        )
                    )
    return missing


def write_report(report_path: Path, payload: dict) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    force_utf8_stdio()
    args = parse_args()
    if Image is None:
        print("ERROR: falta Pillow. Instala dependencias con scripts/setup_env.py.")
        return 2

    static_dir = args.static_dir.resolve()
    if not static_dir.exists():
        print(f"ERROR: no existe el directorio estático: {static_dir}")
        return 2

    fix = bool(args.fix)
    records = [scan_asset(path, fix=fix) for path in iter_assets(static_dir)]
    missing_fallbacks = scan_gif_fallbacks()

    optimizable = [item for item in records if item.status == "optimizable"]
    optimized = [item for item in records if item.status == "optimized"]
    errors = [item for item in records if item.status == "error"]

    payload = {
        "mode": "fix" if fix else "check",
        "static_dir": relative(static_dir),
        "summary": {
            "assets_scanned": len(records),
            "optimized": len(optimized),
            "optimizable": len(optimizable),
            "errors": len(errors),
            "missing_gif_fallbacks": len(missing_fallbacks),
            "saved_bytes": sum(item.saved_bytes for item in records),
        },
        "assets": [asdict(item) for item in records],
        "missing_gif_fallbacks": [asdict(item) for item in missing_fallbacks],
    }

    if args.report:
        write_report(args.report.resolve(), payload)

    print("Auditoría de assets estáticos")
    print(f"  Directorio: {relative(static_dir)}")
    print(f"  Assets revisados: {len(records)}")
    if fix:
        print(f"  Optimizados: {len(optimized)}")
    else:
        print(f"  Optimizables pendientes: {len(optimizable)}")
    print(f"  Ahorro potencial/aplicado: {payload['summary']['saved_bytes'] / 1024:.1f} KiB")
    print(f"  GIFs referenciados sin PNG fallback: {len(missing_fallbacks)}")

    for item in (optimized or optimizable)[:20]:
        print(
            f"  - {item.status}: {item.path} "
            f"({item.before_bytes} -> {item.after_bytes} bytes)"
        )
    if len(optimized or optimizable) > 20:
        print("  ...")

    for item in missing_fallbacks[:20]:
        print(f"  - falta fallback: {item.gif} -> {item.expected_png}")
    if len(missing_fallbacks) > 20:
        print("  ...")

    if errors:
        print("ERROR: hay assets que Pillow no pudo procesar:")
        for item in errors:
            print(f"  - {item.path}: {item.detail}")
        return 1

    if missing_fallbacks:
        print("ERROR: crea un PNG con el mismo nombre base junto a cada GIF referenciado.")
        return 1

    if optimizable and not fix:
        print("ERROR: hay assets optimizables. Ejecuta el script con --fix.")
        return 1

    print("OK: assets estáticos listos para web y PDF.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
