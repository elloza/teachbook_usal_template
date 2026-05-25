#!/usr/bin/env python3
"""Safe launcher for TeachBook preview.

This script is intentionally small and conservative so IDE agents can run ONE
stable command without inventing virtual environments:

    python scripts/launch_preview.py

It does not create venvs. It only finds the project .venv that matches the
current OS and delegates to scripts/preview_book.py with that Python.
"""

from __future__ import annotations

import os
import platform
import signal
import subprocess
import sys
import time
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv"
PREVIEW = ROOT / "scripts" / "preview_book.py"
PID_FILE = ROOT / ".preview.pid"
LOG_FILE = ROOT / ".preview.log"
STATE_FILE = ROOT / ".preview.json"


# ---------------------------------------------------------------------------
# UTF-8 output, important on Windows consoles and CI
# ---------------------------------------------------------------------------

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def is_wsl() -> bool:
    try:
        return "microsoft" in Path("/proc/version").read_text(errors="ignore").lower()
    except FileNotFoundError:
        return False


def current_os_label() -> str:
    label = platform.system()
    if is_wsl():
        label += " (WSL)"
    return label


def expected_python() -> Path:
    if os.name == "nt":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def read_pid() -> int | None:
    try:
        return int(PID_FILE.read_text(encoding="utf-8").strip())
    except Exception:
        return None


def process_is_running(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        if os.name == "nt":
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True,
                text=True,
            )
            return str(pid) in result.stdout
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def read_preview_state() -> dict[str, object]:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def print_status() -> int:
    pid = read_pid()
    if process_is_running(pid):
        print(f"✅ Preview en ejecución (PID {pid})")
        state = read_preview_state()
        url = state.get("url")
        if url:
            print(f"   URL: {url}")
        else:
            print("   URL: arrancando todavía; usa --log si tarda demasiado")
        print(f"   Log: {LOG_FILE}")
        return 0
    print("ℹ️  No hay preview en ejecución.")
    if PID_FILE.exists():
        print("   PID antiguo eliminado.")
        PID_FILE.unlink(missing_ok=True)
    STATE_FILE.unlink(missing_ok=True)
    return 1


def stop_preview() -> int:
    pid = read_pid()
    if not process_is_running(pid):
        print("ℹ️  No hay preview en ejecución.")
        PID_FILE.unlink(missing_ok=True)
        return 0

    assert pid is not None
    print(f"🛑 Deteniendo preview (PID {pid})...")
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False)
        else:
            os.kill(pid, signal.SIGTERM)
            for _ in range(20):
                if not process_is_running(pid):
                    break
                time.sleep(0.2)
            if process_is_running(pid):
                os.kill(pid, signal.SIGKILL)
    finally:
        PID_FILE.unlink(missing_ok=True)
        STATE_FILE.unlink(missing_ok=True)
    print("✅ Preview detenido.")
    return 0


def print_log(lines: int = 80) -> int:
    if not LOG_FILE.exists():
        print("ℹ️  No existe .preview.log todavía.")
        return 1
    content = LOG_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in content[-lines:]:
        print(line)
    return 0


def print_help() -> int:
    print("""TeachBook preview launcher

Uso:
  python scripts/launch_preview.py              # primer plano, para humanos
  python scripts/launch_preview.py --background # segundo plano, para agentes/IDEs
  python scripts/launch_preview.py --status     # ver si sigue vivo
  python scripts/launch_preview.py --log        # ver últimas líneas del log
  python scripts/launch_preview.py --stop       # detener preview

Opciones pasadas a preview_book.py:
  --port 8010       usar otro puerto
  --no-browser      no abrir navegador
  --no-watch        compilar una vez y servir sin vigilar cambios

Regla: este lanzador NO crea entornos. Si .venv no corresponde al sistema
actual, se detiene y muestra diagnóstico.
""")
    return 0


def wrong_os_hint() -> None:
    has_windows_venv = (VENV / "Scripts" / "python.exe").exists()
    has_posix_venv = (VENV / "bin" / "python").exists()

    print("\n❌ No puedo lanzar la preview con seguridad.")
    print(f"   Sistema actual: {current_os_label()}")
    print(f"   Proyecto: {ROOT}")
    print()

    if is_wsl() and has_windows_venv and not has_posix_venv:
        print("El .venv parece creado en Windows, pero estás ejecutando desde WSL.")
        print("No crees otro venv paralelo. Para aquí y pide al usuario elegir UNA opción:")
        print()
        print("  Opción A — ejecutar desde Windows PowerShell:")
        print(r"    .venv\Scripts\python.exe scripts\preview_book.py")
        print()
        print("  Opción B — recrear .venv para WSL con el setup oficial SOLO si el usuario lo pide:")
        print("    python scripts/setup_env.py")
        print()
        return

    if os.name != "nt" and has_windows_venv and not has_posix_venv:
        print("El .venv tiene formato Windows (Scripts/), pero este terminal no es Windows.")
        print("Ejecuta desde Windows o pregunta al usuario si quiere recrear .venv en este sistema.")
        return

    if os.name == "nt" and has_posix_venv and not has_windows_venv:
        print("El .venv tiene formato Linux/macOS (bin/), pero este terminal es Windows.")
        print("Ejecuta desde Linux/macOS/WSL o pregunta al usuario si quiere recrear .venv en Windows.")
        return

    if not VENV.exists():
        print("No existe .venv.")
        print("Ejecuta el setup oficial una vez:")
        print("  python scripts/setup_env.py")
        return

    print(".venv existe, pero no contiene el Python esperado para este sistema.")
    print("Ejecuta el setup oficial, no crees entornos alternativos:")
    print("  python scripts/setup_env.py")


def main() -> int:
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        return print_help()
    if "--status" in args:
        return print_status()
    if "--stop" in args:
        return stop_preview()
    if "--log" in args:
        return print_log()

    py = expected_python()
    if not py.exists():
        wrong_os_hint()
        return 1

    try:
        result = subprocess.run([str(py), "--version"], cwd=ROOT, text=True)
        if result.returncode != 0:
            wrong_os_hint()
            return 1
    except Exception:
        wrong_os_hint()
        return 1

    background = "--background" in args
    passthrough = [arg for arg in args if arg != "--background"]

    if background:
        if process_is_running(read_pid()):
            print_status()
            return 0

        cmd = [str(py), str(PREVIEW), *passthrough]
        print(f"✅ Usando entorno del proyecto: {py}")
        print("▶️  Lanzando preview oficial en segundo plano...")
        print(f"   Log: {LOG_FILE}")
        with LOG_FILE.open("w", encoding="utf-8") as log:
            if os.name == "nt":
                process = subprocess.Popen(
                    cmd,
                    cwd=ROOT,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    cwd=ROOT,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
        PID_FILE.write_text(str(process.pid), encoding="utf-8")
        print(f"✅ Preview lanzado (PID {process.pid}).")
        print("   Espera a que el log muestre: ✅ Build correcto y 🌐 Preview listo")
        print("   Ver log: python scripts/launch_preview.py --log")
        print("   Estado:  python scripts/launch_preview.py --status")
        print("   Parar:   python scripts/launch_preview.py --stop")
        return 0

    cmd = [str(py), str(PREVIEW)] + passthrough
    print(f"✅ Usando entorno del proyecto: {py}")
    print("▶️  Lanzando preview oficial...")
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
