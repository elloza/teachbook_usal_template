#!/usr/bin/env python3
"""TeachBook live preview.

This preview intentionally uses the same build pipeline as production:

    scripts/build_book.py  ->  book/_build/html  ->  local HTTP server

Why not sphinx-autobuild?
    This project has a custom multi-language build pipeline. The real output is
    produced from _config_<lang>.yml and _toc_<lang>.yml, then post-processed by
    build_book.py. A generic sphinx-autobuild process uses the wrong config path
    and can show stale/incomplete pages. Preview must serve the real build.

Usage:
    python scripts/preview_book.py
    python scripts/preview_book.py --port 8010
    python scripts/preview_book.py --no-browser
"""

from __future__ import annotations

import argparse
import functools
import http.server
import io
import os
import platform
import shutil
import signal
import socket
import socketserver
import subprocess
import sys
import threading
import time
import json
from pathlib import Path


# ---------------------------------------------------------------------------
# UTF-8 output, important on Windows consoles
# ---------------------------------------------------------------------------

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"
BUILD_SCRIPT = PROJECT_ROOT / "scripts" / "build_book.py"
HTML_DIR = BOOK_DIR / "_build" / "html"
PID_FILE = PROJECT_ROOT / ".preview.pid"
STATE_FILE = PROJECT_ROOT / ".preview.json"

WATCH_EXTENSIONS = {
    ".md",
    ".ipynb",
    ".yml",
    ".yaml",
    ".bib",
    ".css",
    ".js",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
}

IGNORED_DIR_NAMES = {
    "_build",
    ".ipynb_checkpoints",
    "__pycache__",
}

IGNORED_FILE_NAMES = {
    # build_book.py regenerates this file; watching it causes rebuild loops
    "languages.json",
}


# ---------------------------------------------------------------------------
# Platform / environment helpers
# ---------------------------------------------------------------------------


def is_wsl() -> bool:
    try:
        return "microsoft" in Path("/proc/version").read_text(errors="ignore").lower()
    except FileNotFoundError:
        return False


def venv_python() -> Path | None:
    if os.name == "nt":
        candidate = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        candidate = PROJECT_ROOT / ".venv" / "bin" / "python"
    return candidate if candidate.exists() else None


def check_python_venv() -> bool:
    """Validate that .venv is usable from the current OS."""
    venv_dir = PROJECT_ROOT / ".venv"
    if not venv_dir.exists():
        print("❌ No existe .venv.")
        print("   Ejecuta: python scripts/setup_env.py")
        return False

    py = venv_python()
    if not py:
        print("❌ .venv existe, pero no corresponde a este sistema operativo.")
        if is_wsl() and (venv_dir / "Scripts").exists():
            print("   Estás en WSL, pero el .venv fue creado en Windows.")
            print("   Usa PowerShell para ejecutar el preview, o crea un venv Linux para WSL.")
        else:
            print("   Recrea el entorno: python scripts/setup_env.py")
        return False

    try:
        result = subprocess.run(
            [str(py), "-c", "import sys; print(sys.version); raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            timeout=15,
        )
    except Exception as exc:
        print(f"❌ No se pudo ejecutar {py}: {exc}")
        return False

    if result.returncode != 0:
        version = result.stdout.strip().splitlines()[0] if result.stdout.strip() else "desconocida"
        print(f"❌ Python del .venv demasiado antiguo: {version}")
        print("   Se requiere Python 3.10+.")
        return False

    print(f"✅ Python .venv OK: {result.stdout.strip().splitlines()[0]}")
    return True


def open_browser(url: str) -> None:
    try:
        if is_wsl():
            subprocess.Popen(["cmd.exe", "/c", "start", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif platform.system() == "Windows":
            os.startfile(url)  # type: ignore[attr-defined]
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print(f"ℹ️  Abre manualmente: {url}")


def port_is_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def choose_port(requested: int) -> int:
    for port in range(requested, requested + 20):
        if port_is_available(port):
            return port
    raise RuntimeError("No hay puertos libres entre 8000 y 8019.")


# ---------------------------------------------------------------------------
# Build pipeline
# ---------------------------------------------------------------------------


build_lock = threading.Lock()
last_build_ok = False
last_build_started = 0.0


def run_real_build(reason: str) -> bool:
    """Run scripts/build_book.py exactly like production."""
    global last_build_ok, last_build_started

    py = venv_python() or Path(sys.executable)
    started = time.time()
    last_build_started = started

    with build_lock:
        print("\n" + "=" * 72)
        print(f"🔨 Recompilando libro completo ({reason})")
        print("   Pipeline real: scripts/build_book.py -> book/_build/html")
        print("=" * 72)

        env = os.environ.copy()
        env.setdefault("PYTHONUTF8", "1")

        process = subprocess.Popen(
            [str(py), str(BUILD_SCRIPT)],
            cwd=PROJECT_ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )

        assert process.stdout is not None
        for line in process.stdout:
            print(line, end="")

        return_code = process.wait()
        elapsed = time.time() - started

        if return_code == 0 and (HTML_DIR / "index.html").exists():
            last_build_ok = True
            print(f"\n✅ Build correcto en {elapsed:.1f}s")
            print(f"📂 Sirviendo: {HTML_DIR}")
            return True

        last_build_ok = False
        print(f"\n❌ Build falló (exit code {return_code}) tras {elapsed:.1f}s")
        print("   No se abrirá una web vieja como si fuera correcta.")
        return False


# ---------------------------------------------------------------------------
# File watching by polling (portable; no extra watcher magic)
# ---------------------------------------------------------------------------


def is_watchable(path: Path) -> bool:
    if path.name in IGNORED_FILE_NAMES:
        return False
    if path.suffix.lower() not in WATCH_EXTENSIONS:
        return False
    parts = set(path.parts)
    if parts.intersection(IGNORED_DIR_NAMES):
        return False
    return True


def snapshot_sources() -> dict[str, float]:
    snapshot: dict[str, float] = {}
    if not BOOK_DIR.exists():
        return snapshot

    for path in BOOK_DIR.rglob("*"):
        if path.is_file() and is_watchable(path):
            try:
                snapshot[str(path)] = path.stat().st_mtime
            except OSError:
                pass
    return snapshot


def watcher_loop(stop_event: threading.Event, interval: float = 2.0) -> None:
    previous = snapshot_sources()
    pending_since: float | None = None

    while not stop_event.is_set():
        time.sleep(interval)
        current = snapshot_sources()

        if current != previous:
            previous = current
            pending_since = time.time()
            print("\n📝 Cambio detectado. Esperando a que termine de guardar...")
            continue

        # debounce: only rebuild once files have been stable for ~2 seconds
        if pending_since and time.time() - pending_since >= 2.0:
            pending_since = None
            if build_lock.locked():
                print("⏳ Build en curso; se recompilará en el siguiente cambio estable.")
                continue
            run_real_build("cambio detectado")


# ---------------------------------------------------------------------------
# Static HTTP server with no-cache headers
# ---------------------------------------------------------------------------


class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        # Keep output teacher-friendly; no noisy request logs.
        return


class ReusableTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def start_server(port: int) -> ReusableTCPServer:
    handler = functools.partial(NoCacheHTTPRequestHandler, directory=str(HTML_DIR))
    server = ReusableTCPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TeachBook live preview")
    parser.add_argument("--port", type=int, default=8000, help="Puerto local (por defecto: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="No abrir el navegador automáticamente")
    parser.add_argument("--no-watch", action="store_true", help="Compilar una vez y servir sin vigilar cambios")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print("\n📘 TeachBook Live Preview")
    print("   Usa el MISMO build que producción: scripts/build_book.py")
    print(f"   Sistema: {platform.system()}{' (WSL)' if is_wsl() else ''}")

    if not check_python_venv():
        return 1

    port = choose_port(args.port)
    if port != args.port:
        print(f"⚠️  Puerto {args.port} ocupado. Usando {port}.")

    # Initial build first. This prevents opening stale HTML from yesterday.
    if not run_real_build("arranque inicial"):
        return 1

    server = start_server(port)
    stop_event = threading.Event()
    STATE_FILE.write_text(
        json.dumps(
            {
                "pid": os.getpid(),
                "port": port,
                "url": f"http://127.0.0.1:{port}",
                "html_dir": str(HTML_DIR),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    watcher_thread: threading.Thread | None = None
    if not args.no_watch:
        watcher_thread = threading.Thread(target=watcher_loop, args=(stop_event,), daemon=True)
        watcher_thread.start()

    url = f"http://localhost:{port}"
    print("\n" + "=" * 72)
    print(f"🌐 Preview listo: {url}")
    print("   Si ves algo viejo: Ctrl+F5. El servidor manda cabeceras no-cache.")
    print("   Pulsa Ctrl+C para detener.")
    print("=" * 72 + "\n")

    if not args.no_browser:
        open_browser(url)

    def shutdown(_signum: int | None = None, _frame: object | None = None) -> None:
        print("\n🛑 Deteniendo preview...")
        stop_event.set()
        server.shutdown()
        server.server_close()
        try:
            PID_FILE.unlink(missing_ok=True)
        except Exception:
            pass
        try:
            STATE_FILE.unlink(missing_ok=True)
        except Exception:
            pass

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")

    try:
        while not stop_event.is_set():
            time.sleep(0.5)
    finally:
        shutdown()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
