#!/usr/bin/env python3
"""Render diagram source files into static images for the TeachBook.

This script is intentionally simple: it lets the book include pre-rendered
images with normal MyST ``figure`` blocks, so the Jupyter Book build does not
depend on kroki.io for those diagrams.

Source layout::

    diagram_sources/<lang>/<name>.<type>

Examples::

    diagram_sources/es/flujo_experimento.mermaid
    diagram_sources/en/experiment_flow.mermaid
    diagram_sources/es/dependencias.graphviz

Generated files are written to::

    book/_static/generated/diagrams/<lang>/<name>.svg

By default existing outputs are kept. Use ``--force`` to re-render everything.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover - handled for user-friendly diagnostics
    requests = None  # type: ignore[assignment]


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "diagram_sources"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "book" / "_static" / "generated" / "diagrams"
DEFAULT_PDF_FALLBACK_DIR = PROJECT_ROOT / "book" / "_static" / "generated" / "diagrams_pdf"
DEFAULT_KROKI_URL = "https://kroki.io/"

EXTENSION_TO_KROKI_TYPE = {
    ".mermaid": "mermaid",
    ".mmd": "mermaid",
    ".plantuml": "plantuml",
    ".puml": "plantuml",
    ".graphviz": "graphviz",
    ".dot": "graphviz",
    ".wavedrom": "wavedrom",
    ".structurizr": "structurizr",
    ".d2": "d2",
    ".ditaa": "ditaa",
    ".vega": "vega",
    ".vegalite": "vegalite",
    ".tikz": "tikz",
}


@dataclass(frozen=True)
class DiagramJob:
    source: Path
    output: Path
    diagram_type: str
    output_format: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render diagram_sources/ files into book/_static/generated/diagrams/."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Directory with diagram source files (default: diagram_sources/).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for rendered images (default: book/_static/generated/diagrams/).",
    )
    parser.add_argument(
        "--pdf-fallback-dir",
        type=Path,
        default=DEFAULT_PDF_FALLBACK_DIR,
        help="Directory for PDF-only Mermaid PNG fallbacks (default: book/_static/generated/diagrams_pdf/).",
    )
    parser.add_argument(
        "--format",
        default="svg",
        choices=("svg", "png", "pdf"),
        help="Output image format (default: svg; crisp for HTML and converted for PDF export).",
    )
    parser.add_argument(
        "--kroki-url",
        default=DEFAULT_KROKI_URL,
        help="Kroki endpoint URL (default: https://kroki.io/). Can point to a local service.",
    )
    parser.add_argument(
        "--request-mode",
        choices=("path", "json"),
        default="path",
        help=(
            "How to call Kroki. 'path' uses POST /<type>/<format> with text/plain "
            "(official docs, default). 'json' uses POST / with JSON."
        ),
    )
    parser.add_argument(
        "--mermaid-renderer",
        choices=("auto", "mmdc", "kroki"),
        default="auto",
        help=(
            "Renderer for Mermaid sources. 'auto' prefers local Mermaid CLI "
            "when available and falls back to Kroki."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-render even when the output file already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would be rendered without contacting Kroki.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="HTTP timeout in seconds per request (default: 60).",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Number of attempts per diagram (default: 3).",
    )
    parser.add_argument(
        "--max-failures",
        type=int,
        default=3,
        help="Stop after this many failed diagrams (default: 3). Use 0 to never stop early.",
    )
    return parser.parse_args()


def discover_jobs(source_dir: Path, output_dir: Path, output_format: str) -> list[DiagramJob]:
    if not source_dir.exists():
        return []

    jobs: list[DiagramJob] = []
    for source in sorted(source_dir.rglob("*")):
        if not source.is_file():
            continue
        diagram_type = EXTENSION_TO_KROKI_TYPE.get(source.suffix.lower())
        if not diagram_type:
            continue

        relative = source.relative_to(source_dir)
        output = output_dir / relative.with_suffix(f".{output_format}")
        jobs.append(
            DiagramJob(
                source=source,
                output=output,
                diagram_type=diagram_type,
                output_format=output_format,
            )
        )
    return jobs


def render_job(
    job: DiagramJob,
    kroki_url: str,
    timeout: int,
    retries: int,
    request_mode: str,
    mermaid_renderer: str = "auto",
) -> None:
    if job.diagram_type == "mermaid" and mermaid_renderer in ("auto", "mmdc"):
        if render_mermaid_with_mmdc(job, mermaid_renderer):
            return

    if requests is None:
        raise RuntimeError(
            "No se puede importar 'requests'. Ejecuta el script con el Python de .venv."
        )

    diagram_source = job.source.read_text(encoding="utf-8")
    base_url = kroki_url.rstrip("/")

    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            if request_mode == "json":
                payload = {
                    "diagram_source": diagram_source,
                    "diagram_type": job.diagram_type,
                    "output_format": job.output_format,
                }
                response = requests.post(base_url + "/", json=payload, timeout=timeout)
            else:
                response = requests.post(
                    f"{base_url}/{job.diagram_type}/{job.output_format}",
                    data=diagram_source.encode("utf-8"),
                    headers={
                        "Content-Type": "text/plain; charset=utf-8",
                        "Accept": f"image/{job.output_format}",
                    },
                    timeout=timeout,
                )
            response.raise_for_status()
            job.output.parent.mkdir(parents=True, exist_ok=True)
            job.output.write_bytes(response.content)
            return
        except Exception as exc:  # requests exposes several exception classes
            last_error = exc
            if attempt < retries:
                wait_seconds = attempt * 5
                print(
                    f"   ⚠️  Intento {attempt}/{retries} falló para {job.source}. "
                    f"Reintentando en {wait_seconds}s..."
                )
                time.sleep(wait_seconds)

    raise RuntimeError(f"No se pudo renderizar {job.source}: {last_error}")


def render_mermaid_with_mmdc(job: DiagramJob, mermaid_renderer: str) -> bool:
    """Render Mermaid locally with Mermaid CLI when available.

    This keeps ES/EN diagrams visually consistent and avoids Kroki availability
    changing the published result. If `auto` is selected and neither `mmdc` nor
    `npx` is available, return False so the caller can fall back to Kroki.
    """
    if sys.platform == "win32":
        mmdc = shutil.which("mmdc.cmd") or shutil.which("mmdc.exe") or shutil.which("mmdc")
        npx = shutil.which("npx.cmd") or shutil.which("npx.exe") or shutil.which("npx")
    else:
        mmdc = shutil.which("mmdc")
        npx = shutil.which("npx")

    if mmdc:
        cmd = [mmdc]
    elif npx:
        cmd = [npx, "--yes", "@mermaid-js/mermaid-cli"]
    elif mermaid_renderer == "mmdc":
        raise RuntimeError("No se encontró Mermaid CLI (mmdc) ni npx para renderizar Mermaid localmente.")
    else:
        return False

    background = "white" if job.output_format == "png" else "transparent"
    cmd.extend(["-i", str(job.source), "-o", str(job.output), "-b", background])
    if job.output_format == "png":
        cmd.extend(["-s", "2"])
    job.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True)
    return True


def maybe_render_pdf_fallback_png(
    job: DiagramJob,
    source_dir: Path,
    pdf_fallback_dir: Path,
    kroki_url: str,
    timeout: int,
    retries: int,
    request_mode: str,
    mermaid_renderer: str,
    force: bool,
) -> None:
    """Render a PDF-only PNG sidecar for Mermaid SVG diagrams.

    Kroki's Mermaid SVG can contain `foreignObject` HTML labels. Those are crisp
    in browsers, but some SVG converters drop the text. Kroki's native PNG
    endpoint preserves the labels, so PDF export can use this sidecar when no
    vector SVG→PDF converter is available.
    """
    if job.output_format != "svg" or job.diagram_type != "mermaid":
        return

    relative = job.source.relative_to(source_dir)
    output = pdf_fallback_dir / relative.with_suffix(".png")
    if output.exists() and not force:
        return

    print(f"   🧩 Generando fallback PDF Mermaid PNG: {output.relative_to(PROJECT_ROOT)}")
    render_job(
        DiagramJob(
            source=job.source,
            output=output,
            diagram_type=job.diagram_type,
            output_format="png",
        ),
        kroki_url,
        timeout,
        retries,
        request_mode,
        mermaid_renderer,
    )


def write_manifest(jobs: list[DiagramJob], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_by": "scripts/render_diagrams.py",
        "items": [
            {
                "source": str(job.source.relative_to(PROJECT_ROOT)),
                "output": str(job.output.relative_to(PROJECT_ROOT)),
                "type": job.diagram_type,
                "format": job.output_format,
            }
            for job in jobs
        ],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    source_dir = args.source_dir.resolve()
    output_dir = args.output_dir.resolve()
    pdf_fallback_dir = args.pdf_fallback_dir.resolve()

    jobs = discover_jobs(source_dir, output_dir, args.format)

    if not jobs:
        print(f"ℹ️  No hay fuentes de diagramas en: {source_dir}")
        print("   Crea archivos como diagram_sources/es/flujo.mermaid para renderizarlos.")
        return 0

    print(f"🖼️  Diagramas encontrados: {len(jobs)}")
    for job in jobs:
        status = "existe" if job.output.exists() else "nuevo"
        print(f"   - {job.source.relative_to(PROJECT_ROOT)} -> {job.output.relative_to(PROJECT_ROOT)} ({status})")

    if args.dry_run:
        print("✅ Dry-run completado. No se ha contactado con Kroki.")
        return 0

    rendered: list[DiagramJob] = []
    skipped = 0
    failed = 0
    for job in jobs:
        if job.output.exists() and not args.force:
            try:
                maybe_render_pdf_fallback_png(
                    job,
                    source_dir,
                    pdf_fallback_dir,
                    args.kroki_url,
                    args.timeout,
                    args.retries,
                    args.request_mode,
                    args.mermaid_renderer,
                    args.force,
                )
            except Exception as exc:
                failed += 1
                print(f"❌ {exc}")
                if args.max_failures and failed >= args.max_failures:
                    print(f"🛑 Parando tras {failed} fallos. Usa --max-failures 0 para continuar siempre.")
                    break
                continue
            skipped += 1
            rendered.append(job)
            continue
        try:
            print(f"🔧 Renderizando {job.source.relative_to(PROJECT_ROOT)}...")
            render_job(
                job,
                args.kroki_url,
                args.timeout,
                args.retries,
                args.request_mode,
                args.mermaid_renderer,
            )
            maybe_render_pdf_fallback_png(
                job,
                source_dir,
                pdf_fallback_dir,
                args.kroki_url,
                args.timeout,
                args.retries,
                args.request_mode,
                args.mermaid_renderer,
                args.force,
            )
            rendered.append(job)
        except Exception as exc:
            failed += 1
            print(f"❌ {exc}")
            if args.max_failures and failed >= args.max_failures:
                print(f"🛑 Parando tras {failed} fallos. Usa --max-failures 0 para continuar siempre.")
                break

    write_manifest(rendered, output_dir)

    print("\nResumen:")
    print(f"  ✅ Renderizados/registrados: {len(rendered)}")
    print(f"  ⏭️  Omitidos por existir: {skipped}")
    print(f"  ❌ Fallidos: {failed}")

    if failed:
        print("\nEl build del libro puede seguir usando las imágenes ya existentes.")
        print("Si faltan imágenes nuevas, reintenta cuando Kroki responda o usa --kroki-url con un servicio local.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
