import argparse
import importlib.util
import io
import json
import os
import platform
import site
import shutil
import subprocess
import sys
import sysconfig
import time
from pathlib import Path


# Keep setup output readable on Windows consoles that default to cp1252.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


TARGET_PYTHON_VERSION = "3.12"
VENV_DIR = ".venv"
REQUIREMENTS_FILE = "requirements.txt"
DEV_REQUIREMENTS_FILE = "requirements-dev.txt"
EXTRA_REQUIREMENTS = {
    "pdf": "requirements-pdf.txt",
    "notebooks": "requirements-notebooks.txt",
    "pdf-import": "requirements-pdf-import.txt",
}

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VENV_PATH = PROJECT_ROOT / VENV_DIR
BUILD_LOGS = PROJECT_ROOT / ".build_logs"

SKILLS_SOURCE = PROJECT_ROOT / ".github" / "skills"
SKILLS_DESTINATIONS = [
    PROJECT_ROOT / ".claude" / "skills",
    PROJECT_ROOT / ".agents" / "skills",
    PROJECT_ROOT / ".agent" / "skills",
]
AGENTS_MD = PROJECT_ROOT / "AGENTS.md"
COPILOT_INSTRUCTIONS = PROJECT_ROOT / ".github" / "copilot-instructions.md"

BASE_REQUIRED_DISTS = [
    "pip",
    "jupyter-book",
    "sphinx-design",
    "sphinxcontrib-bibtex",
    "sphinx-thebe",
    "sphinx-kroki",
    "Pillow",
    "PyYAML",
]
EXTRA_REQUIRED_DISTS = {
    "pdf": [
        "sphinx-jupyterbook-latex",
        "cairosvg",
        "svglib",
        "reportlab",
    ],
    "notebooks": [
        "jupyterquiz",
        "matplotlib",
        "numpy",
        "pandas",
        "scipy",
        "sympy",
        "schemdraw",
        "ipywidgets",
    ],
    "pdf-import": [
        "pymupdf4llm",
        "PyMuPDF",
    ],
}


class Profiler:
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.events = []

    def phase(self, name):
        return _ProfilePhase(self, name)

    def add(self, name, seconds):
        if self.enabled:
            self.events.append({"phase": name, "seconds": round(seconds, 3)})

    def write(self, target_python, use_uv):
        if not self.enabled:
            return
        BUILD_LOGS.mkdir(exist_ok=True)
        data = {
            "target_python": target_python,
            "extras": sorted(getattr(self, "extras", [])),
            "platform": platform.platform(),
            "venv_python": get_venv_version() if get_venv_python().is_file() else None,
            "package_manager": "uv" if use_uv else "pip",
            "events": self.events,
            "total_seconds": round(sum(item["seconds"] for item in self.events), 3),
        }
        out = BUILD_LOGS / "setup_env_profile.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nPerfil guardado en {out.relative_to(PROJECT_ROOT)}")


class _ProfilePhase:
    def __init__(self, profiler, name):
        self.profiler = profiler
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.profiler.add(self.name, time.perf_counter() - self.start)
        return False


def run(cmd, *, cwd=PROJECT_ROOT, check=True, capture=False):
    kwargs = {
        "cwd": str(cwd),
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
    }
    if capture:
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.STDOUT
    sys.stdout.flush()
    sys.stderr.flush()
    result = subprocess.run(cmd, **kwargs)
    sys.stdout.flush()
    sys.stderr.flush()
    if check and result.returncode != 0:
        if capture and result.stdout:
            print(result.stdout)
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def get_venv_python():
    if os.name == "nt":
        return VENV_PATH / "Scripts" / "python.exe"
    return VENV_PATH / "bin" / "python"


def get_venv_version():
    python_cmd = get_venv_python()
    if not python_cmd.is_file():
        return None
    code = "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
    try:
        return run([str(python_cmd), "-c", code], capture=True).stdout.strip()
    except Exception:
        return None


def get_venv_major_minor():
    version = get_venv_version()
    if not version:
        return None
    parts = version.split(".")
    return ".".join(parts[:2])


def detect_uv():
    fix_path_for_uv()
    return shutil.which("uv") is not None


def get_uv_version():
    if not detect_uv():
        return None
    try:
        return run(["uv", "--version"], capture=True).stdout.strip()
    except Exception:
        return None


def fix_path_for_uv():
    home = Path.home()
    extra_dirs = []
    scripts_path = sysconfig.get_path("scripts")
    if scripts_path:
        extra_dirs.append(Path(scripts_path))
    user_base = site.getuserbase()
    if user_base:
        extra_dirs.append(Path(user_base) / ("Scripts" if os.name == "nt" else "bin"))
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            extra_dirs.append(Path(local_app_data) / "uv")
        extra_dirs.extend([home / ".local" / "bin", home / ".cargo" / "bin"])
    else:
        extra_dirs.extend([home / ".local" / "bin", home / ".cargo" / "bin"])

    current = os.environ.get("PATH", "")
    parts = current.split(os.pathsep) if current else []
    for directory in extra_dirs:
        directory_str = str(directory)
        if directory.is_dir() and directory_str not in parts:
            parts.insert(0, directory_str)
    os.environ["PATH"] = os.pathsep.join(parts)


def install_uv_noninteractive():
    system = platform.system()
    print("Instalando uv...")
    installer_cmd = (
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "irm https://astral.sh/uv/install.ps1 | iex"]
        if system == "Windows"
        else ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]
    )

    try:
        run(installer_cmd)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"Instalador oficial de uv no disponible: {exc}")
        print("Instalando uv mediante pip como fallback...")
        try:
            run([sys.executable, "-m", "pip", "install", "--upgrade", "uv"])
        except subprocess.CalledProcessError:
            run([sys.executable, "-m", "pip", "install", "--user", "--upgrade", "uv"])
    finally:
        fix_path_for_uv()


def ensure_uv(yes=False):
    if detect_uv():
        print(f"uv detectado: {get_uv_version()}")
        return True

    if not yes:
        try:
            answer = input("uv no esta instalado. Instalarlo ahora? [Y/n]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return False
        if answer in {"n", "no"}:
            return False

    try:
        install_uv_noninteractive()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"No se pudo instalar uv: {exc}")
        return False

    if detect_uv():
        print(f"uv instalado: {get_uv_version()}")
        return True

    print("uv parece instalado, pero no esta disponible en esta terminal.")
    return False


def explain_wrong_os_venv():
    has_windows_python = (VENV_PATH / "Scripts" / "python.exe").is_file()
    has_posix_python = (VENV_PATH / "bin" / "python").is_file()

    print(f"ERROR: '{VENV_DIR}' existe, pero no corresponde a este sistema.")
    print("No se crearan entornos paralelos ni backups automaticos.")
    print()
    if os.name != "nt" and has_windows_python and not has_posix_python:
        print("Detectado: .venv de Windows en Linux/macOS/WSL.")
        print("Usa Windows o borra .venv y ejecuta de nuevo desde este sistema.")
    elif os.name == "nt" and has_posix_python and not has_windows_python:
        print("Detectado: .venv de Linux/macOS en Windows.")
        print("Usa Linux/macOS/WSL o borra .venv y ejecuta de nuevo desde Windows.")
    else:
        print("Borra .venv y ejecuta de nuevo: python scripts/setup_env.py")


def remove_venv_safely():
    resolved = VENV_PATH.resolve()
    root = PROJECT_ROOT.resolve()
    if resolved.name != VENV_DIR or os.path.commonpath([str(root), str(resolved)]) != str(root):
        raise RuntimeError(f"Ruta de .venv no segura: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def ensure_target_python(target_python):
    print(f"Preparando Python {target_python} con uv...")
    try:
        run(["uv", "python", "install", target_python])
    except subprocess.CalledProcessError as exc:
        print(f"No se pudo instalar/localizar Python {target_python} con uv.")
        raise exc


def create_or_validate_venv(target_python, recreate=False):
    if VENV_PATH.exists():
        if not get_venv_python().is_file():
            explain_wrong_os_venv()
            raise SystemExit(1)

        current = get_venv_major_minor()
        if current != target_python:
            if not recreate:
                print(
                    f"ERROR: .venv usa Python {get_venv_version()}, pero este proyecto requiere Python {target_python}."
                )
                print("Para recrearlo de forma explicita ejecuta:")
                print(f"  python scripts/setup_env.py --recreate --yes --python {target_python}")
                raise SystemExit(1)
            print(f"Recreando .venv: Python {current} -> {target_python}")
            remove_venv_safely()
        else:
            print(f".venv correcto: Python {get_venv_version()}")
            return

    print(f"Creando .venv con Python {target_python}...")
    run(["uv", "venv", str(VENV_PATH), "--python", target_python, "--seed"])
    print(f".venv creado: Python {get_venv_version()}")


def normalize_extras(raw_extras=None, *, all_extras=False, dev_mode=False):
    extras = set()
    if raw_extras:
        for chunk in raw_extras:
            for item in chunk.split(","):
                item = item.strip().lower()
                if item:
                    extras.add(item)
    if all_extras:
        extras.update(EXTRA_REQUIREMENTS)
    if dev_mode:
        extras.add("dev")
    unknown = sorted(extras.difference(set(EXTRA_REQUIREMENTS) | {"dev"}))
    if unknown:
        valid = ", ".join(sorted(EXTRA_REQUIREMENTS))
        raise SystemExit(f"ERROR: extras no reconocidos: {', '.join(unknown)}. Validos: {valid}")
    return extras


def install_requirement_file(requirements_file, label):
    python_cmd = str(get_venv_python())
    req = PROJECT_ROOT / requirements_file
    if req.is_file():
        print(f"Instalando {label} desde {requirements_file}...")
        run(["uv", "pip", "install", "--python", python_cmd, "-r", str(req)])
    else:
        print(f"AVISO: {requirements_file} no existe.")


def install_requirements(dev_mode=False, extras=None):
    python_cmd = str(get_venv_python())
    install_requirement_file(REQUIREMENTS_FILE, "dependencias base")

    for extra in sorted(extras or []):
        if extra == "dev":
            continue
        install_requirement_file(EXTRA_REQUIREMENTS[extra], f"extra '{extra}'")

    if dev_mode:
        dev_req = PROJECT_ROOT / DEV_REQUIREMENTS_FILE
        if dev_req.is_file():
            print(f"Instalando dependencias de desarrollo desde {DEV_REQUIREMENTS_FILE}...")
            run(["uv", "pip", "install", "--python", python_cmd, "-r", str(dev_req)])
            install_playwright_browsers(python_cmd)
        else:
            print(f"AVISO: {DEV_REQUIREMENTS_FILE} no existe.")


def install_playwright_browsers(python_cmd):
    print("Instalando navegadores Playwright...")
    try:
        run([python_cmd, "-m", "playwright", "install"])
    except subprocess.CalledProcessError:
        print("AVISO: no se pudieron instalar navegadores Playwright.")


def verify_installation(dev_mode=False, target_python=TARGET_PYTHON_VERSION, extras=None):
    python_cmd = str(get_venv_python())
    print("\nVerificando entorno:")

    version = get_venv_major_minor()
    if version != target_python:
        raise SystemExit(f"ERROR: .venv usa Python {version}; se esperaba {target_python}.")
    print(f"  Python: {get_venv_version()}")

    required = list(BASE_REQUIRED_DISTS)
    for extra in sorted(extras or []):
        if extra == "dev":
            continue
        required.extend(EXTRA_REQUIRED_DISTS[extra])
    if dev_mode:
        required.append("playwright")

    code = r"""
import importlib.metadata as md
import json
import sys

required = json.loads(sys.argv[1])
missing = []
versions = {}
for name in required:
    try:
        dist = md.distribution(name)
        versions[name] = dist.version
    except md.PackageNotFoundError:
        missing.append(name)
print(json.dumps({"missing": missing, "versions": versions}, ensure_ascii=False))
"""
    result = run([python_cmd, "-c", code, json.dumps(required)], capture=True)
    data = json.loads(result.stdout)
    if data["missing"]:
        print("  Paquetes faltantes:", ", ".join(data["missing"]))
        raise SystemExit(1)

    manim_check = run(
        [
            python_cmd,
            "-c",
            "import importlib.util; raise SystemExit(0 if importlib.util.find_spec('manim') is None else 1)",
        ],
        check=False,
    )
    if manim_check.returncode != 0:
        raise SystemExit("ERROR: manim no debe estar instalado en el entorno base.")

    print(f"  Paquetes clave: {len(required)} OK")
    print("  Manim: ausente OK")


def verify_runtime_tools():
    print("\nVerificando herramientas externas:")
    if shutil.which("git"):
        print("  Git: disponible")
    else:
        print("  Git: no encontrado. Necesario para publicar en GitHub.")

    if shutil.which("tectonic"):
        print("  Tectonic: disponible")
    else:
        print("  Tectonic: no encontrado. Para PDF ejecuta:")
        print("    python scripts/setup_latex.py --yes --full")


def sync_skills():
    print("\nSincronizando skills...")
    if not SKILLS_SOURCE.is_dir():
        print(f"ERROR: origen de skills no encontrado: {SKILLS_SOURCE}")
        return False

    ok = True
    for dest in SKILLS_DESTINATIONS:
        try:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(SKILLS_SOURCE, dest)
            print(f"  OK {dest.relative_to(PROJECT_ROOT)}")
        except Exception as exc:
            ok = False
            print(f"  ERROR {dest.relative_to(PROJECT_ROOT)}: {exc}")
    return ok


def sync_instructions():
    print("\nSincronizando instrucciones...")
    if not AGENTS_MD.is_file():
        print(f"ERROR: no existe {AGENTS_MD}")
        return False
    try:
        COPILOT_INSTRUCTIONS.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(AGENTS_MD, COPILOT_INSTRUCTIONS)
        print(f"  OK {COPILOT_INSTRUCTIONS.relative_to(PROJECT_ROOT)}")
        return True
    except Exception as exc:
        print(f"  ERROR copilot-instructions.md: {exc}")
        return False


def print_diagnostics(target_python):
    print("TeachBook - diagnostico del sistema")
    print("=" * 40)
    print(f"OS:      {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Python:  {sys.executable} ({sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})")
    print(f"Objetivo:{target_python}")
    print(f"Git:     {'disponible' if shutil.which('git') else 'no encontrado'}")
    print(f"uv:      {get_uv_version() or 'no encontrado'}")
    print(f".venv:   {'existe' if VENV_PATH.exists() else 'no existe'}")
    if get_venv_python().is_file():
        print(f".venv Python: {get_venv_version()}")
    print()


def print_summary(dev_mode=False, target_python=TARGET_PYTHON_VERSION, extras=None):
    skills_ok = all(dest.is_dir() for dest in SKILLS_DESTINATIONS)
    print()
    print("Entorno TeachBook listo.")
    print(f"  Python objetivo: {target_python}")
    print(f"  Python .venv:    {get_venv_version()}")
    print(f"  Modo:            {'desarrollo' if dev_mode else 'produccion'}")
    print(f"  Extras:          {', '.join(sorted(extras or [])) if extras else 'ninguno'}")
    print(f"  Skills:          {'sincronizadas' if skills_ok else 'incompletas'}")
    print()
    print("Siguientes comandos habituales:")
    print("  python scripts/build_book.py")
    print("  python scripts/setup_env.py --yes --extras pdf")
    print("  python scripts/setup_latex.py --yes --full")
    print("  python scripts/export_pdf.py --engine auto")


def parse_args():
    parser = argparse.ArgumentParser(description="Configurar entorno TeachBook")
    parser.add_argument("--dev", action="store_true", help="Instalar herramientas de desarrollo")
    parser.add_argument(
        "--sync-only",
        action="store_true",
        help="Solo sincronizar skills e instrucciones, sin tocar .venv",
    )
    parser.add_argument("--yes", action="store_true", help="Modo no interactivo")
    parser.add_argument(
        "--python",
        default=TARGET_PYTHON_VERSION,
        help=f"Version Python objetivo (por defecto: {TARGET_PYTHON_VERSION})",
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Borrar y recrear .venv si ya existe con otra version",
    )
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Medir tiempos por fase y guardar .build_logs/setup_env_profile.json",
    )
    parser.add_argument(
        "--extras",
        action="append",
        default=[],
        help="Extras opcionales separados por coma: pdf,notebooks,pdf-import",
    )
    parser.add_argument("--pdf", action="store_true", help="Alias de --extras pdf")
    parser.add_argument("--notebooks", action="store_true", help="Alias de --extras notebooks")
    parser.add_argument("--pdf-import", action="store_true", help="Alias de --extras pdf-import")
    parser.add_argument("--all", action="store_true", help="Instalar todos los extras opcionales")
    return parser.parse_args()


def main():
    args = parse_args()
    profiler = Profiler(args.profile)
    raw_extras = list(args.extras)
    if args.pdf:
        raw_extras.append("pdf")
    if args.notebooks:
        raw_extras.append("notebooks")
    if args.pdf_import:
        raw_extras.append("pdf-import")
    extras = normalize_extras(raw_extras, all_extras=args.all, dev_mode=args.dev)
    profiler.extras = extras

    if args.sync_only:
        print("TeachBook - sincronizacion")
        print("=" * 40)
        sync_ok = sync_skills()
        instr_ok = sync_instructions()
        if not (sync_ok and instr_ok):
            raise SystemExit(1)
        print("\nSincronizacion completa.")
        return

    with profiler.phase("diagnostics"):
        print_diagnostics(args.python)

    with profiler.phase("uv"):
        if not ensure_uv(yes=args.yes):
            print("ERROR: uv es necesario para crear un entorno determinista.")
            print("Instala uv o ejecuta de nuevo con --yes para instalarlo automaticamente.")
            raise SystemExit(1)

    with profiler.phase("python"):
        ensure_target_python(args.python)

    with profiler.phase("venv"):
        create_or_validate_venv(args.python, recreate=args.recreate)

    with profiler.phase("requirements"):
        install_requirements(dev_mode=args.dev, extras=extras)

    with profiler.phase("verification"):
        verify_installation(dev_mode=args.dev, target_python=args.python, extras=extras)
        verify_runtime_tools()

    with profiler.phase("skills"):
        sync_ok = sync_skills()
        instr_ok = sync_instructions()
        if not (sync_ok and instr_ok):
            raise SystemExit(1)

    profiler.write(args.python, use_uv=True)
    print_summary(dev_mode=args.dev, target_python=args.python, extras=extras)


if __name__ == "__main__":
    main()
