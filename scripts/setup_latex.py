import io
import subprocess
import sys
import shutil
import platform
import os
import json
import stat
import urllib.request
import zipfile
import tarfile
import tempfile
import time
import urllib.error

# Fix: Windows cp1252 can't encode emojis — force UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


VENV_DIR = ".venv"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, "requirements-pdf.txt")
PDF_REQUIRED_DISTS = [
    "sphinx-jupyterbook-latex",
    "cairosvg",
    "svglib",
    "reportlab",
]
TECTONIC_RELEASE_TAG = os.environ.get("TECTONIC_RELEASE_TAG", "tectonic@0.15.0")
TINYTEX_VERSION = os.environ.get("TINYTEX_VERSION", "2026.04")
TINYTEX_INSTALLER = os.environ.get("TINYTEX_INSTALLER", "TinyTeX-1")
# TinyTeX-1 already brings the LaTeX base, XeTeX, latexmk, fontspec,
# hyperref, xcolor, amsmath, babel and other essentials. Keep this list
# surgical: only packages required by the TeachBook templates/Sphinx output
# that may be missing in the base image. Do NOT add heavy collections here.
TINYTEX_PACKAGES = [
    "latexmk",
    "xetex",
    "fontspec",
    "framed",
    "fancyvrb",
    "fancyhdr",
    "fncychap",
    "footnotehyper",
    "tabulary",
    "varwidth",
    "wrapfig",
    "needspace",
    "capt-of",
    "caption",
    "cmap",
    "colortbl",
    "ellipse",
    "pict2e",
    "parskip",
    "titlesec",
    "ucharclasses",
    "upquote",
    "pgf",
    "pgfplots",
    "jknapltx",  # provides mathrsfs.sty
    "rsfs",  # provides the rsfs fonts used by mathrsfs.sty
    "amsmath",
    "amsfonts",
    "bbm",
    "bbm-macros",
    "changepage",
    "babel-spanish",
    "babel-english",
    "polyglossia",
    "hyphen-spanish",
    "hyphen-english",
    "gnu-freefont",
    "hypcap",
    "xindy",
]
TINYTEX_REQUIRED_FILES = [
    "amscd.sty",
    "bbm.sty",
    "capt-of.sty",
    "caption.sty",
    "changepage.sty",
    "cmap.sty",
    "colortbl.sty",
    "ellipse.sty",
    "fancyhdr.sty",
    "fncychap.sty",
    "footnotehyper.sty",
    "hypcap.sty",
    "mathrsfs.sty",
    "needspace.sty",
    "pgfplots.sty",
    "pict2e.sty",
    "parskip.sty",
    "titlesec.sty",
    "ucharclasses.sty",
    "polyglossia.sty",
    "rsfs10.mf",
    "tabulary.sty",
    "tikz.sty",
    "upquote.sty",
    "varwidth.sty",
    "wrapfig.sty",
]
HEAVY_TINYTEX_COLLECTIONS = {
    "collection-latexextra",
    "collection-xetex",
    "collection-latexrecommended",
    "collection-fontsrecommended",
    "collection-langspanish",
    "collection-langenglish",
    "scheme-full",
}
TINYTEX_DOWNLOAD_ESTIMATES_MB = {
    "windows": "~72 MB",
    "darwin": "~65 MB",
    "linux": "~50–53 MB",
}
TINYTEX_EXPECTED_SPACE_MB = "300–800 MB"


def run(cmd, **kwargs):
    """Run a command, showing it for transparent CI logs."""
    printable = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    print(f"$ {printable}")
    return subprocess.run(cmd, check=True, **kwargs)


def add_github_path(path):
    """Persist a PATH entry for later GitHub Actions steps."""
    github_path = os.environ.get("GITHUB_PATH")
    if github_path and os.path.isdir(path):
        with open(github_path, "a", encoding="utf-8") as f:
            f.write(path + "\n")
        print(f"✅ Añadido a GITHUB_PATH: {path}")


def prepend_path(path):
    """Make a tool directory visible to the current process and GitHub steps."""
    if not path or not os.path.isdir(path):
        return
    current = os.environ.get("PATH", "")
    paths = current.split(os.pathsep) if current else []
    if path not in paths:
        os.environ["PATH"] = path + os.pathsep + current
    add_github_path(path)


def get_project_tool_dir(*parts):
    """Return a project-controlled tool directory inside .venv."""
    return os.path.join(VENV_DIR, "tools", *parts)


def get_tectonic_cache_dir():
    cache_dir = get_project_tool_dir("tectonic-cache")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.abspath(cache_dir)


def get_tinytex_parent_dir():
    parent = get_project_tool_dir("tinytex")
    os.makedirs(parent, exist_ok=True)
    return os.path.abspath(parent)


def get_tinytex_root():
    return os.path.join(get_tinytex_parent_dir(), "TinyTeX")


def get_tinytex_bin_dir():
    root = get_tinytex_root()
    bin_root = os.path.join(root, "bin")
    if not os.path.isdir(bin_root):
        return None
    if os.name == "nt":
        candidate = os.path.join(bin_root, "windows")
        return candidate if os.path.isdir(candidate) else None
    for name in os.listdir(bin_root):
        candidate = os.path.join(bin_root, name)
        if os.path.isdir(candidate):
            return candidate
    return None


def activate_tinytex_path():
    bin_dir = get_tinytex_bin_dir()
    if bin_dir:
        prepend_path(bin_dir)
    return bin_dir


def format_size_mb(size_bytes):
    return f"{size_bytes / (1024 * 1024):.0f} MB"


def get_directory_size_bytes(path):
    """Return a best-effort recursive directory size without failing checks."""
    if not os.path.isdir(path):
        return 0
    total = 0
    for root, _dirs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                if not os.path.islink(file_path):
                    total += os.path.getsize(file_path)
            except OSError:
                continue
    return total


def read_tinytex_installed_packages():
    """Read installed package names from TinyTeX's texlive.tlpdb if available."""
    tlpdb_path = os.path.join(get_tinytex_root(), "tlpkg", "texlive.tlpdb")
    if not os.path.isfile(tlpdb_path):
        return []
    packages = []
    try:
        with open(tlpdb_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("name "):
                    name = line.split(maxsplit=1)[1].strip()
                    if name:
                        packages.append(name)
    except OSError:
        return []
    return packages


def get_installed_heavy_tinytex_collections(packages=None):
    if packages is None:
        packages = read_tinytex_installed_packages()
    installed = set(packages)
    return sorted(HEAVY_TINYTEX_COLLECTIONS.intersection(installed))


def get_tinytex_diagnostic_info():
    root = get_tinytex_root()
    packages = read_tinytex_installed_packages()
    return {
        "root": root,
        "exists": os.path.isdir(root),
        "size_bytes": get_directory_size_bytes(root),
        "package_count": len(packages),
        "heavy_collections": get_installed_heavy_tinytex_collections(packages),
    }


def print_tinytex_diagnostics():
    """Print lightweight diagnostics for an existing project-local TinyTeX."""
    info = get_tinytex_diagnostic_info()
    if not info["exists"]:
        print("ℹ️  TinyTeX portable aún no está instalado en .venv/tools/tinytex.")
        return info

    print("📊 Diagnóstico TinyTeX portable:")
    print(f"   Ubicación: {info['root']}")
    print(f"   Tamaño aproximado: {format_size_mb(info['size_bytes'])}")
    if info["package_count"]:
        print(f"   Paquetes instalados aprox.: {info['package_count']}")
    else:
        print("   Paquetes instalados aprox.: no se pudo leer tlpkg/texlive.tlpdb")

    warning_needed = info["size_bytes"] > 1024 * 1024 * 1024 or bool(info["heavy_collections"])
    if warning_needed:
        print("⚠️  Esta instalación parece más grande de lo necesario para un docente.")
        if info["size_bytes"] > 1024 * 1024 * 1024:
            print("   Supera 1 GB; lo esperado con este flujo ligero suele ser 300–800 MB.")
        if info["heavy_collections"]:
            print("   Contiene colecciones pesadas:")
            for collection in info["heavy_collections"]:
                print(f"   • {collection}")
        print("   No se borrará nada automáticamente. Si quieres adelgazarla, haz copia y reinstala TinyTeX dentro de .venv cuando proceda.")
    return info


def print_tinytex_full_mode_notice():
    """Explain the size implications of --full before installing TinyTeX."""
    system = platform.system().lower()
    download_estimate = TINYTEX_DOWNLOAD_ESTIMATES_MB.get(system, "~50–72 MB")
    print("ℹ️  Modo --full: se mantiene Tectonic como motor principal y se prepara TinyTeX solo como red de seguridad.")
    print(f"   Descarga base TinyTeX-1 estimada para {platform.system()}: {download_estimate}.")
    print(f"   Espacio local esperado con paquetes mínimos: {TINYTEX_EXPECTED_SPACE_MB}.")
    print("   Instalaremos paquetes concretos, no colecciones enormes como collection-latexextra ni scheme-full.")


def command_exists(command):
    return shutil.which(command) is not None


def local_binary_candidates(binary_name):
    candidates = []
    venv_bin = get_venv_bin_dir()
    if os.path.isdir(venv_bin):
        candidates.append(os.path.join(venv_bin, binary_name))

    if os.name == "nt":
        appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
        candidates.append(os.path.join(appdata, "teachbook", binary_name))
    else:
        candidates.append(os.path.expanduser(os.path.join("~", ".local", "bin", binary_name)))

    candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), binary_name))
    return candidates


def get_python_launcher():
    return get_effective_python()


def python_module_available(module_name):
    python = get_python_launcher()
    try:
        result = subprocess.run(
            [python, "-c", f"import {module_name}"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
        )
        return result.returncode == 0
    except Exception:
        return False


def pip_available():
    python = get_python_launcher()
    try:
        result = subprocess.run(
            [python, "-m", "pip", "--version"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
        )
        return result.returncode == 0
    except Exception:
        return False


def ensure_pip_available():
    if pip_available():
        return True
    python = get_python_launcher()
    print("🧰 Pip no está disponible en el Python del proyecto. Intentando activarlo...")
    try:
        result = subprocess.run(
            [python, "-m", "ensurepip", "--upgrade"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
    except Exception as exc:
        print(f"⚠️  No se pudo activar pip automáticamente: {exc}")
        return False
    return pip_available()


def verify_svg_converter():
    resvg = get_resvg_command()
    if resvg:
        print(f"✅ Conversor SVG detectado: {resvg}")
        return True

    converter = shutil.which("rsvg-convert")
    if converter:
        print(f"✅ Conversor SVG detectado: {converter}")
        return True

    if python_module_available("cairosvg"):
        print("✅ CairoSVG disponible en el Python del proyecto.")
        return True

    print("❌ Falta conversor SVG robusto (rsvg-convert o CairoSVG).")
    return False


def verify_svg_vector_converter():
    """Return True when SVG can be converted to vector PDF for LaTeX.

    `resvg` is an excellent SVG->PNG renderer, but it does not provide the
    vector PDF output we prefer for crisp diagram PDFs. For vector output we
    need `rsvg-convert --format pdf` or CairoSVG.
    """
    converter = shutil.which("rsvg-convert")
    if converter:
        print(f"✅ Conversor SVG→PDF detectado: {converter}")
        return True

    if python_module_available("cairosvg"):
        print("✅ CairoSVG disponible para conversión SVG→PDF.")
        return True

    if python_module_available("svglib") and python_module_available("reportlab"):
        print("✅ svglib/reportlab disponible para conversión SVG→PDF vectorial.")
        return True

    print("⚠️  Falta conversor vectorial SVG→PDF (rsvg-convert o CairoSVG).")
    return False


def find_command_with_common_latex_paths(command_name):
    """Find LaTeX tools, preferring project-local TinyTeX."""
    activate_tinytex_path()
    found = shutil.which(command_name)
    if found:
        return found

    executable = f"{command_name}.exe" if os.name == "nt" else command_name
    candidates = []

    tinytex_bin = get_tinytex_bin_dir()
    if tinytex_bin:
        candidates.append(os.path.join(tinytex_bin, executable))
        if os.name == "nt":
            candidates.append(os.path.join(tinytex_bin, f"{command_name}.bat"))

    if os.name == "nt":
        candidates.extend(
            [
                os.path.join("C:\\Program Files\\MiKTeX\\miktex\\bin\\x64", executable),
                os.path.join("C:\\Program Files\\MiKTeX\\miktex\\bin", executable),
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "MiKTeX", "miktex", "bin", "x64", executable),
            ]
        )
    else:
        candidates.extend(
            [
                os.path.join("/Library/TeX/texbin", executable),
                os.path.join("/usr/local/bin", executable),
                os.path.join("/usr/bin", executable),
            ]
        )

    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate
    return None


def install_cairosvg_with_pip():
    if not ensure_pip_available():
        return False

    python = get_python_launcher()
    print("📦 Intentando instalar CairoSVG en el entorno del proyecto...")
    try:
        result = subprocess.run(
            [python, "-m", "pip", "install", "cairosvg"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=900,
        )
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
        return result.returncode == 0
    except Exception as exc:
        print(f"⚠️  Falló la instalación de CairoSVG con pip: {exc}")
        return False


def install_svglib_with_pip():
    if not ensure_pip_available():
        return False

    python = get_python_launcher()
    print("📦 Intentando instalar svglib/reportlab en el entorno del proyecto...")
    try:
        result = subprocess.run(
            [python, "-m", "pip", "install", "svglib", "reportlab"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=900,
        )
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
        return result.returncode == 0
    except Exception as exc:
        print(f"⚠️  Falló la instalación de svglib/reportlab con pip: {exc}")
        return False


def missing_distributions_for_python(python, dist_names):
    check_script = r"""
import importlib.metadata as metadata
import json
import sys

missing = []
for dist_name in sys.argv[1:]:
    try:
        metadata.distribution(dist_name)
    except metadata.PackageNotFoundError:
        missing.append(dist_name)

print(json.dumps(missing))
"""
    try:
        result = subprocess.run(
            [python, "-c", check_script, *dist_names],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except Exception:
        return list(dist_names)

    if result.returncode != 0:
        return list(dist_names)
    try:
        return json.loads(result.stdout.strip() or "[]")
    except json.JSONDecodeError:
        return list(dist_names)


def missing_pdf_python_requirements():
    return missing_distributions_for_python(get_python_launcher(), PDF_REQUIRED_DISTS)


def install_pdf_python_requirements():
    missing = missing_pdf_python_requirements()
    if not missing:
        return True
    if not os.path.isfile(PDF_REQUIREMENTS_FILE):
        print(f"❌ Falta {PDF_REQUIREMENTS_FILE}; no se pueden instalar dependencias PDF.")
        return False

    python = get_python_launcher()
    print("📦 Instalando dependencias Python para exportación PDF...")
    print(f"   Faltan: {', '.join(missing)}")
    try:
        if shutil.which("uv"):
            subprocess.check_call(
                ["uv", "pip", "install", "--python", python, "-r", PDF_REQUIREMENTS_FILE],
                cwd=PROJECT_ROOT,
            )
        else:
            subprocess.check_call(
                [python, "-m", "pip", "install", "-r", PDF_REQUIREMENTS_FILE],
                cwd=PROJECT_ROOT,
            )
        return not missing_pdf_python_requirements()
    except subprocess.CalledProcessError:
        print("❌ Error instalando dependencias PDF.")
        print("   Ejecuta: python scripts/setup_env.py --yes --extras pdf")
        return False


def install_svg_converter():
    raster_converter_ready = verify_svg_converter()
    vector_converter_ready = verify_svg_vector_converter()
    if raster_converter_ready and vector_converter_ready:
        return True

    print("🖼️  Instalando soporte SVG para PDF con Tectonic...")
    if not raster_converter_ready and install_resvg_binary():
        raster_converter_ready = verify_svg_converter()
    if not vector_converter_ready and install_cairosvg_with_pip():
        vector_converter_ready = verify_svg_vector_converter()
    if not vector_converter_ready and install_svglib_with_pip():
        vector_converter_ready = verify_svg_vector_converter()
    if raster_converter_ready and vector_converter_ready:
        return True

    if os.environ.get("TEACHBOOK_ALLOW_SYSTEM_LATEX_DEPS") == "1":
        system = platform.system().lower()
        if system == "darwin" and command_exists("brew"):
            try:
                run(["brew", "install", "librsvg", "cairo", "pkg-config"])
                return verify_svg_converter()
            except Exception as exc:
                print(f"⚠️  No se pudo instalar librsvg con Homebrew: {exc}")
        if system == "linux" and (os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS")):
            try:
                apt = ["apt-get"] if os.geteuid() == 0 else ["sudo", "apt-get"]
                run(apt + ["update"])
                run(apt + ["install", "-y", "librsvg2-bin"])
                return verify_svg_converter()
            except Exception as exc:
                print(f"⚠️  No se pudo instalar librsvg en Linux: {exc}")

    print("⚠️  No se pudo dejar listo el conversor SVG automáticamente.")
    print("   El flujo PDF con Tectonic necesita rsvg-convert o CairoSVG para los SVG/Kroki.")
    return False


def verify_full_latex():
    """Verify the advanced fallback PDF toolchain (latexmk + XeLaTeX)."""
    activate_tinytex_path()
    print_tinytex_diagnostics()
    latexmk = find_command_with_common_latex_paths("latexmk")
    xelatex = find_command_with_common_latex_paths("xelatex")
    if latexmk and xelatex:
        missing_files = find_missing_tinytex_required_files()
        if missing_files:
            print("❌ Toolchain LaTeX encontrada, pero faltan paquetes usados por las plantillas:")
            for filename in missing_files:
                print(f"   • {filename}")
            return False
        print("✅ Toolchain LaTeX completa detectada.")
        print(f"   latexmk: {latexmk}")
        print(f"   xelatex: {xelatex}")
        try:
            subprocess.run([xelatex, "--version"], check=False, timeout=15)
        except Exception:
            pass
        return True

    print("❌ Falta toolchain LaTeX completa.")
    print(f"   latexmk: {latexmk or 'NO encontrado'}")
    print(f"   xelatex: {xelatex or 'NO encontrado'}")
    return False


def find_missing_tinytex_required_files():
    """Check representative .sty files required by the custom PDF templates."""
    kpsewhich = find_command_with_common_latex_paths("kpsewhich")
    if not kpsewhich:
        return []
    env = os.environ.copy()
    bin_dir = get_tinytex_bin_dir()
    if bin_dir:
        env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")
    missing = []
    for filename in TINYTEX_REQUIRED_FILES:
        result = subprocess.run(
            [kpsewhich, filename],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=30,
        )
        if result.returncode != 0 or not result.stdout.strip():
            missing.append(filename)
    return missing


def install_full_latex_ci():
    """Install the advanced XeLaTeX + latexmk fallback toolchain.

    Tectonic remains the default user-facing flow. The fallback is TinyTeX
    installed inside the project venv, without Chocolatey/Homebrew/apt and
    without admin permissions.
    """
    print("🔧 Preparando fallback LaTeX completo con TinyTeX portable...")
    print_tinytex_full_mode_notice()

    full_latex_ready = verify_full_latex()

    if full_latex_ready and verify_svg_converter():
        return True
    if not install_tinytex_portable():
        return False
    if not install_tinytex_packages():
        return False
    print_tinytex_diagnostics()
    return verify_full_latex() and verify_svg_converter()


def get_venv_python():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")


def get_effective_python():
    venv_python = get_venv_python()
    if os.path.isfile(venv_python):
        return venv_python
    return sys.executable


def get_venv_bin_dir():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts")
    return os.path.join(VENV_DIR, "bin")


def local_tectonic_candidates():
    executable_name = "tectonic.exe" if os.name == "nt" else "tectonic"
    return local_binary_candidates(executable_name)


def local_resvg_candidates():
    executable_name = "resvg.exe" if os.name == "nt" else "resvg"
    return local_binary_candidates(executable_name)


def get_tectonic_command():
    found = shutil.which("tectonic")
    if found:
        return found
    for candidate in local_tectonic_candidates():
        if os.path.isfile(candidate):
            return candidate
    return None


def get_resvg_command():
    found = shutil.which("resvg")
    if found:
        return found
    for candidate in local_resvg_candidates():
        if os.path.isfile(candidate):
            return candidate
    return None


def is_tectonic_installed():
    return get_tectonic_command() is not None


def verify_tectonic():
    tectonic = get_tectonic_command()
    if not tectonic:
        return False
    try:
        env = os.environ.copy()
        env["TECTONIC_CACHE_DIR"] = get_tectonic_cache_dir()
        result = subprocess.run(
            [tectonic, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            env=env,
        )
        if result.returncode == 0:
            version = result.stdout.strip().split("\n")[0]
            if not verify_tectonic_minimal_compile(tectonic, env):
                return False
            print(f"✅ Tectonic {version} funcionando correctamente.")
            print(f"   Ejecutable: {tectonic}")
            print(f"   Cache: {env['TECTONIC_CACHE_DIR']}")
            return True
    except (subprocess.TimeoutExpired, OSError):
        pass
    print("❌ Tectonic se instaló pero no se pudo ejecutar.")
    return False


def verify_tectonic_minimal_compile(tectonic, env):
    """Compile a tiny document so --check catches broken Tectonic installs."""
    # `tectonic` may be a project-relative path such as `.venv/bin/tectonic`.
    # The compile probe runs with `cwd=tmp`, so a relative executable path would
    # be resolved from the temporary directory and fail immediately in CI.
    tectonic = os.path.abspath(tectonic)
    with tempfile.TemporaryDirectory(prefix="tectonic_check_") as tmp:
        tex_path = os.path.join(tmp, "check.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write("\\documentclass{article}\n\\begin{document}\nTeachBook OK\n\\end{document}\n")
        try:
            result = subprocess.run(
                [tectonic, "--keep-logs", tex_path],
                cwd=tmp,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
                env=env,
            )
            if result.returncode == 0 and os.path.isfile(os.path.join(tmp, "check.pdf")):
                return True
            print("❌ Tectonic ejecuta --version, pero no compila un documento mínimo.")
            if result.stdout:
                print(result.stdout[-1000:])
            if result.stderr:
                print(result.stderr[-1000:])
            return False
        except Exception as exc:
            print(f"❌ Tectonic falló compilando documento mínimo: {exc}")
            return False


def install_tectonic_pip():
    print("📦 Intentando instalar Tectonic con pip...")
    python = get_python_launcher()
    is_venv = python != sys.executable
    if is_venv:
        print(f"   Usando entorno virtual: {python}")
    else:
        print("   Usando Python del sistema.")
    try:
        result = subprocess.run(
            [python, "-m", "pip", "install", "tectonic"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            print("❌ Tectonic no está disponible como paquete pip para esta plataforma.")
            print("   Esto es normal en muchos equipos; se usará descarga directa del binario oficial.")
            return False
        print("✅ Tectonic instalado correctamente con pip.")
        return True
    except Exception as exc:
        print(f"❌ Error ejecutando pip: {exc}")
        return False


def get_arch_tag():
    machine = platform.machine().lower()
    if machine in ("x86_64", "amd64"):
        return "amd64"
    if machine in ("arm64", "aarch64"):
        return "arm64"
    return None


def get_platform_target():
    system = platform.system().lower()
    arch = get_arch_tag()
    if arch is None:
        return None, None, None
    targets = {
        ("windows", "amd64"): ("x86_64-pc-windows-msvc", ".zip"),
        ("darwin", "amd64"): ("x86_64-apple-darwin", ".tar.gz"),
        ("darwin", "arm64"): ("aarch64-apple-darwin", ".tar.gz"),
        ("linux", "amd64"): ("x86_64-unknown-linux-musl", ".tar.gz"),
        ("linux", "arm64"): ("aarch64-unknown-linux-musl", ".tar.gz"),
    }
    result = targets.get((system, arch))
    if result is None:
        return None, None, None
    return system, result[0], result[1]


def fetch_latest_release():
    api_url = f"https://api.github.com/repos/tectonic-typesetting/tectonic/releases/tags/{TECTONIC_RELEASE_TAG}"
    data = fetch_github_json(api_url, f"Tectonic {TECTONIC_RELEASE_TAG}")
    if data:
        return data.get("tag_name"), data.get("assets", [])
    return None, []


def fetch_latest_release_for_repo(repo_slug):
    api_url = f"https://api.github.com/repos/{repo_slug}/releases/latest"
    data = fetch_github_json(api_url, f"GitHub API ({repo_slug})")
    if data:
        return data.get("tag_name"), data.get("assets", [])
    return None, []


def fetch_github_json(api_url, label):
    """Fetch public GitHub JSON, retrying without GITHUB_TOKEN on auth errors."""
    base_headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "teachbook-setup",
    }
    token = os.environ.get("GITHUB_TOKEN")
    header_sets = []
    if token:
        header_sets.append({**base_headers, "Authorization": f"Bearer {token}"})
    header_sets.append(base_headers)

    last_error = None
    for headers in header_sets:
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code in (401, 403) and "Authorization" in headers:
                print(
                    f"⚠️  GitHub rechazó el token para {label}; "
                    "reintentando sin credenciales."
                )
                continue
            break
        except Exception as exc:
            last_error = exc
            break

    print(f"❌ Error consultando {label}: {last_error}")
    return None


def download_file_with_retries(url, destination, label, attempts=4):
    """Download a release asset with retries and CI-friendly headers."""
    base_headers = {"User-Agent": "teachbook-setup"}
    token = os.environ.get("GITHUB_TOKEN")
    header_sets = []
    if token and "github.com" in url:
        header_sets.append({**base_headers, "Authorization": f"Bearer {token}"})
    header_sets.append(base_headers)

    last_error = None
    for headers in header_sets:
        for attempt in range(1, attempts + 1):
            try:
                print(f"   Descargando {label} (intento {attempt}/{attempts})...")
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=120) as resp:
                    with open(destination, "wb") as f:
                        shutil.copyfileobj(resp, f)
                if os.path.getsize(destination) > 0:
                    return True
                last_error = "archivo descargado vacío"
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code in (401, 403) and "Authorization" in headers:
                    print(
                        "   ⚠️  GitHub rechazó el token de descarga; "
                        "reintentando sin credenciales."
                    )
                    break
            except Exception as exc:
                last_error = exc

            if attempt < attempts:
                wait_seconds = min(2 * attempt, 8)
                print(
                    f"   ⚠️  Descarga fallida ({last_error}). "
                    f"Reintentando en {wait_seconds}s..."
                )
                time.sleep(wait_seconds)

    print(f"❌ Error descargando {label}: {last_error}")
    return False


def find_asset_url(assets, rust_target, ext):
    for asset in assets:
        name = asset.get("name", "")
        if rust_target in name and name.endswith(ext):
            return asset.get("browser_download_url"), name
    return None, None


def get_binary_install_dir():
    venv_bin = get_venv_bin_dir()
    if os.path.isdir(venv_bin):
        # Prefer installing inside the project venv. This is the most robust
        # option for Windows agents because it avoids global PATH edits.
        return venv_bin

    if os.name == "nt":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
        dest = os.path.join(base, "teachbook")
    else:
        dest = os.path.expanduser("~/.local/bin")
    os.makedirs(dest, exist_ok=True)
    return dest


def verify_resvg():
    resvg = get_resvg_command()
    if not resvg:
        return False
    try:
        result = subprocess.run(
            [resvg, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        if result.returncode == 0:
            version = (result.stdout or result.stderr).strip().split("\n")[0]
            print(f"✅ resvg {version} funcionando correctamente.")
            print(f"   Ejecutable: {resvg}")
            return True
    except (subprocess.TimeoutExpired, OSError):
        pass
    print("❌ resvg se instaló pero no se pudo ejecutar.")
    return False


def get_resvg_asset_name(system, arch):
    mapping = {
        ("windows", "amd64"): ("resvg-win64.zip", ".zip"),
        ("darwin", "amd64"): ("resvg-macos-x86_64.zip", ".zip"),
        ("darwin", "arm64"): ("resvg-macos-aarch64.zip", ".zip"),
        ("linux", "amd64"): ("resvg-linux-x86_64.tar.gz", ".tar.gz"),
    }
    return mapping.get((system, arch), (None, None))


def install_resvg_binary():
    print("⬇️  Intentando instalar resvg (conversor SVG portable)...")
    system = platform.system().lower()
    arch = get_arch_tag()
    asset_name, ext = get_resvg_asset_name(system, arch)
    if not asset_name or not ext:
        print(f"⚠️  No hay binario resvg predefinido para {platform.system()} {platform.machine()}.")
        return False

    tag_name, assets = fetch_latest_release_for_repo("linebender/resvg")
    if not tag_name or not assets:
        print("❌ No se pudo obtener la última release de resvg.")
        return False

    asset = next((item for item in assets if item.get("name") == asset_name), None)
    if not asset:
        print(f"❌ No se encontró el asset {asset_name} en la release {tag_name}.")
        return False

    download_url = asset.get("browser_download_url")
    install_dir = get_binary_install_dir()
    executable_name = "resvg.exe" if system == "windows" else "resvg"

    with tempfile.TemporaryDirectory(prefix="resvg_") as tmp:
        archive_path = os.path.join(tmp, asset_name)
        extract_dir = os.path.join(tmp, "extracted")
        os.makedirs(extract_dir, exist_ok=True)

        if not download_file_with_retries(download_url, archive_path, asset_name):
            return False

        try:
            if ext == ".zip":
                with zipfile.ZipFile(archive_path, "r") as zf:
                    zf.extractall(extract_dir)
            else:
                with tarfile.open(archive_path, "r:gz") as tf:
                    tf.extractall(extract_dir)
        except Exception as e:
            print(f"❌ Error extrayendo resvg: {e}")
            return False

        extracted_bin = os.path.join(extract_dir, executable_name)
        if not os.path.isfile(extracted_bin):
            for root, dirs, files in os.walk(extract_dir):
                if executable_name in files:
                    extracted_bin = os.path.join(root, executable_name)
                    break

        if not os.path.isfile(extracted_bin):
            print("❌ No se encontró el ejecutable de resvg dentro del archivo descargado.")
            return False

        dest_path = os.path.join(install_dir, executable_name)
        shutil.copy2(extracted_bin, dest_path)
        if system != "windows":
            st = os.stat(dest_path)
            os.chmod(dest_path, st.st_mode | stat.S_IEXEC)

    print(f"✅ resvg instalado en: {dest_path}")
    if os.path.abspath(install_dir) == os.path.abspath(get_venv_bin_dir()):
        print("   Instalado dentro de .venv: no hace falta tocar el PATH global.")
    return verify_resvg()


def install_tectonic_binary():
    print("⬇️  Descargando binario de Tectonic desde GitHub...")

    system, rust_target, ext = get_platform_target()
    if rust_target is None:
        machine = platform.machine()
        sysname = platform.system()
        print(f"❌ Plataforma no soportada: {sysname} {machine}")
        print("   Plataformas soportadas: Windows/macOS/Linux en x86_64 o ARM64.")
        return False

    tag_name, assets = fetch_latest_release()
    if not tag_name or not assets:
        print("❌ No se pudo obtener la última versión desde GitHub.")
        return False

    version = tag_name.lstrip("tectonic@")
    print(f"   Última versión disponible: {version}")

    download_url, asset_name = find_asset_url(assets, rust_target, ext)
    if not download_url:
        print(f"❌ No se encontró binario para {rust_target} en la release {tag_name}.")
        print("   Revisa https://github.com/tectonic-typesetting/tectonic/releases")
        return False

    install_dir = get_binary_install_dir()
    with tempfile.TemporaryDirectory(prefix="tectonic_") as tmp:
        archive_path = os.path.join(tmp, asset_name)

        if not download_file_with_retries(download_url, archive_path, asset_name):
            return False

        print("📦 Extrayendo...")
        extract_dir = os.path.join(tmp, "extracted")
        os.makedirs(extract_dir, exist_ok=True)

        if ext == ".zip":
            with zipfile.ZipFile(archive_path, "r") as zf:
                zf.extractall(extract_dir)
        else:
            with tarfile.open(archive_path, "r:gz") as tf:
                tf.extractall(extract_dir)

        executable_name = "tectonic.exe" if system == "windows" else "tectonic"
        extracted_bin = os.path.join(extract_dir, executable_name)

        if not os.path.isfile(extracted_bin):
            for root, dirs, files in os.walk(extract_dir):
                if executable_name in files:
                    extracted_bin = os.path.join(root, executable_name)
                    break

        if not os.path.isfile(extracted_bin):
            print("❌ No se encontró el ejecutable dentro del archivo descargado.")
            return False

        dest_path = os.path.join(install_dir, executable_name)
        shutil.copy2(extracted_bin, dest_path)

        if system != "windows":
            st = os.stat(dest_path)
            os.chmod(dest_path, st.st_mode | stat.S_IEXEC)

    print(f"✅ Tectonic instalado en: {dest_path}")

    if os.path.abspath(install_dir) == os.path.abspath(get_venv_bin_dir()):
        print("   Instalado dentro de .venv: no hace falta tocar el PATH global.")
        return True

    if not shutil.which("tectonic"):
        print()
        print(
            "⚠️  Tectonic no está en tu PATH. Para usarlo, añade esta línea a tu shell:"
        )
        if system == "windows":
            print(f'   set PATH="%APPDATA%\\teachbook;%PATH%"')
            print(
                "   (O añade la carpeta en Configuración → Sistema → Variables de entorno)"
            )
            print("   Los scripts del proyecto también buscarán Tectonic en %APPDATA%\\teachbook.")
        else:
            print(f'   export PATH="{install_dir}:$PATH"')
            shell_rc = os.path.expanduser("~/.bashrc")
            preferred_shell = os.environ.get("SHELL", "")
            if "zsh" in preferred_shell:
                shell_rc = os.path.expanduser("~/.zshrc")
            print(f"   O añade la línea anterior a {shell_rc}")
        print()

    return True


def get_tinytex_asset_name(system, arch):
    """Return the TinyTeX monthly release asset for this platform."""
    installer = TINYTEX_INSTALLER
    version = TINYTEX_VERSION
    if system == "windows":
        return f"{installer}-windows-v{version}.exe"
    if system == "darwin":
        return f"{installer}-darwin-v{version}.tar.xz"
    if system == "linux":
        if arch == "arm64":
            return f"{installer}-linux-arm64-v{version}.tar.xz"
        return f"{installer}-linux-x86_64-v{version}.tar.xz"
    return None


def fetch_tinytex_release_assets():
    api_url = f"https://api.github.com/repos/rstudio/tinytex-releases/releases/tags/v{TINYTEX_VERSION}"
    data = fetch_github_json(api_url, f"TinyTeX v{TINYTEX_VERSION}")
    if data:
        return data.get("assets", [])
    return []


def install_tinytex_portable():
    """Install TinyTeX inside .venv/tools/tinytex without touching system PATH."""
    print("⬇️  Preparando TinyTeX portable...")
    activate_tinytex_path()
    if verify_full_latex():
        return True

    if os.path.isdir(get_tinytex_root()) and get_tinytex_bin_dir():
        print("ℹ️  TinyTeX portable ya existe; instalaré solo los paquetes que falten.")
        return True

    system = platform.system().lower()
    arch = get_arch_tag()
    asset_name = get_tinytex_asset_name(system, arch)
    if not asset_name:
        print(f"❌ TinyTeX portable no soportado para {platform.system()} {platform.machine()}.")
        return False

    assets = fetch_tinytex_release_assets()
    asset = next((item for item in assets if item.get("name") == asset_name), None)
    if not asset:
        print(f"❌ No se encontró {asset_name} en TinyTeX v{TINYTEX_VERSION}.")
        return False

    download_url = asset.get("browser_download_url")
    parent_dir = get_tinytex_parent_dir()
    tinytex_root = get_tinytex_root()

    with tempfile.TemporaryDirectory(prefix="tinytex_") as tmp:
        archive_path = os.path.join(tmp, asset_name)
        if not download_file_with_retries(download_url, archive_path, asset_name, attempts=3):
            return False

        extract_dir = os.path.join(tmp, "extract")
        os.makedirs(extract_dir, exist_ok=True)
        print("📦 Extrayendo TinyTeX...")
        try:
            if asset_name.endswith(".exe"):
                run([archive_path, "-y"], cwd=extract_dir)
            else:
                with tarfile.open(archive_path, "r:*") as tf:
                    tf.extractall(extract_dir)
        except Exception as exc:
            print(f"❌ Error extrayendo TinyTeX: {exc}")
            return False

        extracted_root = find_extracted_tinytex_root(extract_dir)
        if not os.path.isdir(extracted_root):
            print("❌ No se encontró la carpeta TinyTeX dentro del paquete descargado.")
            return False

        if os.path.isdir(tinytex_root):
            shutil.rmtree(tinytex_root)
        os.makedirs(parent_dir, exist_ok=True)
        shutil.move(extracted_root, tinytex_root)

    bin_dir = activate_tinytex_path()
    if not bin_dir:
        print("❌ TinyTeX se extrajo, pero no se encontró su carpeta binaria.")
        return False

    print(f"✅ TinyTeX instalado en: {tinytex_root}")
    print("   Instalación portable dentro de .venv; no se ha usado Chocolatey/Homebrew/apt.")
    return True


def find_extracted_tinytex_root(extract_dir):
    """Find the TinyTeX root regardless of archive top-level layout."""
    direct = os.path.join(extract_dir, "TinyTeX")
    if is_tinytex_root(direct):
        return direct
    if is_tinytex_root(extract_dir):
        return extract_dir

    for root, dirs, _files in os.walk(extract_dir):
        if "TinyTeX" in dirs:
            candidate = os.path.join(root, "TinyTeX")
            if is_tinytex_root(candidate):
                return candidate
        if "tlpkg" in dirs and "bin" in dirs:
            return root
    return direct


def is_tinytex_root(path):
    return os.path.isdir(os.path.join(path, "tlpkg")) and os.path.isdir(os.path.join(path, "bin"))


def get_tlmgr_command():
    activate_tinytex_path()
    if os.name == "nt":
        candidates = ["tlmgr.bat", "tlmgr.exe", "tlmgr"]
    else:
        candidates = ["tlmgr"]
    tinytex_bin = get_tinytex_bin_dir()
    for name in candidates:
        if tinytex_bin:
            candidate = os.path.join(tinytex_bin, name)
            if os.path.isfile(candidate):
                return candidate
        found = shutil.which(name)
        if found:
            return found
    return None


def install_tinytex_packages():
    """Install the LaTeX packages needed by this TeachBook fallback."""
    forbidden = sorted(HEAVY_TINYTEX_COLLECTIONS.intersection(TINYTEX_PACKAGES))
    if forbidden:
        print("❌ La lista TinyTeX contiene colecciones pesadas, y eso rompería el objetivo docente ligero:")
        for package in forbidden:
            print(f"   • {package}")
        return False

    tlmgr = get_tlmgr_command()
    if not tlmgr:
        print("❌ No se encontró tlmgr en TinyTeX.")
        return False

    env = os.environ.copy()
    bin_dir = get_tinytex_bin_dir()
    if bin_dir:
        env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")

    print("📦 Instalando paquetes LaTeX mínimos necesarios en TinyTeX...")
    print(f"   Paquetes explícitos: {', '.join(TINYTEX_PACKAGES)}")
    try:
        subprocess.run([tlmgr, "option", "repository", "ctan"], check=False, env=env, timeout=60)
        subprocess.run([tlmgr, "update", "--self"], check=False, env=env, timeout=600)
        run([tlmgr, "install", *TINYTEX_PACKAGES], env=env)
        subprocess.run([tlmgr, "postaction", "install", "script", "xetex"], check=False, env=env, timeout=300)
    except Exception as exc:
        print(f"❌ Error instalando paquetes TinyTeX: {exc}")
        return False
    return True


def main():
    print("🔍 Verificando entorno LaTeX...")

    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
Uso:
  python scripts/setup_latex.py            # pregunta antes de instalar Tectonic
  python scripts/setup_latex.py --yes      # instala Tectonic sin preguntar
  python scripts/setup_latex.py --yes --full # instala el toolchain PDF completo usado por CI/CD
  python scripts/setup_latex.py --check    # solo verifica Tectonic
  python scripts/setup_latex.py --ci-full  # instala latexmk + XeLaTeX como fallback avanzado
  python scripts/setup_latex.py --check-full # verifica el fallback avanzado

En Windows usa siempre el Python del proyecto:
  .venv\\Scripts\\python.exe scripts\\setup_latex.py --yes
""")
        return

    if "--ci-full" in sys.argv:
        print("ℹ️  Modo avanzado: instalando fallback completo latexmk + XeLaTeX.")
        if install_full_latex_ci():
            return
        sys.exit(1)

    if "--check-full" in sys.argv:
        if verify_full_latex():
            return
        sys.exit(1)

    if not install_pdf_python_requirements():
        sys.exit(1)

    full_mode = "--full" in sys.argv

    def finish_after_tectonic_ready():
        if not full_mode:
            return True
        print("ℹ️  Modo completo: preparando también el fallback latexmk + XeLaTeX usado por CI/CD.")
        return install_full_latex_ci()

    if is_tectonic_installed():
        if verify_tectonic():
            if verify_svg_converter():
                if finish_after_tectonic_ready():
                    return
                sys.exit(1)
                return
            print("⚠️  Tectonic está bien, pero falta el conversor SVG necesario para PDF.")
            if "--check" in sys.argv:
                sys.exit(1)
            if install_svg_converter():
                if finish_after_tectonic_ready():
                    return
                sys.exit(1)
                return
            sys.exit(1)
        print("⚠️  Tectonic encontrado pero no funciona. Se reinstalará.")

    if "--check" in sys.argv:
        print("❌ Tectonic no está instalado/no funciona, o falta el conversor SVG.")
        sys.exit(1)

    auto_confirm = "--yes" in sys.argv or "-y" in sys.argv
    print("ℹ️  No se encontró Tectonic (motor LaTeX ligero para generar PDFs).")

    if auto_confirm:
        confirm = "s"
    else:
        confirm = input("¿Quieres instalarlo ahora? (s/n): ").strip().lower()

    if confirm != "s":
        print("⚠️  Instalación cancelada. No se podrán generar PDFs.")
        return

    if install_tectonic_pip():
        if verify_tectonic() and install_svg_converter():
            if finish_after_tectonic_ready():
                return
            sys.exit(1)
            return

    print("⚠️  Pip falló. Intentando descarga directa del binario...")
    if install_tectonic_binary():
        if verify_tectonic() and install_svg_converter():
            if finish_after_tectonic_ready():
                return
            sys.exit(1)
            return
        sys.exit(1)
    else:
        print()
        print("❌ No se pudo instalar Tectonic automáticamente.")
        print("   Puedes instalarlo manualmente:")
        print("   • pip install tectonic")
        print("   • https://tectonic-typesetting.github.io/book/latest/installation/")
        sys.exit(1)


if __name__ == "__main__":
    main()
