import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PYTHON = "3.12"


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
    result = subprocess.run(cmd, **kwargs)
    if check and result.returncode != 0:
        if capture and result.stdout:
            print(result.stdout)
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def require_uv():
    if shutil.which("uv") is None:
        raise SystemExit("ERROR: uv no esta disponible. Ejecuta scripts/setup_env.py --yes primero.")


def venv_python(venv_path):
    if os.name == "nt":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def directory_size(path):
    total = 0
    if not path.exists():
        return 0
    for file_path in path.rglob("*"):
        if file_path.is_file():
            try:
                total += file_path.stat().st_size
            except OSError:
                pass
    return total


def profile_installed_packages(python_cmd, top_n=30):
    code = r"""
import importlib.metadata as md
import json
from pathlib import Path

rows = []
for dist in md.distributions():
    try:
        root = Path(dist.locate_file(""))
        files = list(dist.files or [])
        size = 0
        for item in files:
            path = root / item
            if path.is_file():
                try:
                    size += path.stat().st_size
                except OSError:
                    pass
        rows.append({"name": dist.metadata["Name"], "version": dist.version, "bytes": size})
    except Exception:
        continue
rows.sort(key=lambda item: item["bytes"], reverse=True)
print(json.dumps(rows, ensure_ascii=False))
"""
    result = run([str(python_cmd), "-c", code], capture=True)
    return json.loads(result.stdout)[:top_n]


def install_args_for_requirements(requirements):
    args = []
    for req in requirements:
        args.extend(["-r", str(req)])
    return args


def dry_run(requirements, python_version):
    temp_dir = Path(tempfile.mkdtemp(prefix="teachbook_deps_dry_"))
    target_dir = temp_dir / "target"
    start = time.perf_counter()
    try:
        result = run(
            [
                "uv",
                "pip",
                "install",
                "--dry-run",
                "--target",
                str(target_dir),
                "--python-version",
                python_version,
                *install_args_for_requirements(requirements),
            ],
            capture=True,
        )
        seconds = time.perf_counter() - start
        planned = [
            line.strip()[2:]
            for line in result.stdout.splitlines()
            if line.strip().startswith("+ ")
        ]
        return {
            "mode": "dry-run",
            "requirements": [str(req.relative_to(PROJECT_ROOT) if req.is_relative_to(PROJECT_ROOT) else req) for req in requirements],
            "seconds": round(seconds, 3),
            "planned_packages": planned,
            "planned_count": len(planned),
            "stdout_tail": result.stdout.splitlines()[-40:],
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def real_install(requirements, python_version, keep_temp=False):
    temp_dir = Path(tempfile.mkdtemp(prefix="teachbook_deps_real_"))
    venv = temp_dir / ".venv"
    start = time.perf_counter()
    try:
        run(["uv", "python", "install", python_version])
        run(["uv", "venv", str(venv), "--python", python_version, "--seed"])
        install_start = time.perf_counter()
        run(["uv", "pip", "install", "--python", str(venv_python(venv)), *install_args_for_requirements(requirements)])
        install_seconds = time.perf_counter() - install_start
        total_seconds = time.perf_counter() - start
        top_packages = profile_installed_packages(venv_python(venv))
        return {
            "mode": "real-install",
            "requirements": [str(req.relative_to(PROJECT_ROOT) if req.is_relative_to(PROJECT_ROOT) else req) for req in requirements],
            "seconds": round(total_seconds, 3),
            "install_seconds": round(install_seconds, 3),
            "temp_dir": str(temp_dir) if keep_temp else None,
            "venv_size_mb": round(directory_size(venv) / (1024 * 1024), 2),
            "top_packages_by_size": [
                {
                    "name": item["name"],
                    "version": item["version"],
                    "size_mb": round(item["bytes"] / (1024 * 1024), 2),
                }
                for item in top_packages
            ],
        }
    finally:
        if not keep_temp:
            shutil.rmtree(temp_dir, ignore_errors=True)


def write_json(path, data):
    target = Path(path)
    if not target.is_absolute():
        target = PROJECT_ROOT / target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Informe guardado en {target}")


def parse_args():
    parser = argparse.ArgumentParser(description="Perfilar dependencias del TeachBook")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Resolver sin instalar")
    mode.add_argument("--real-install", action="store_true", help="Instalar en un venv temporal")
    parser.add_argument(
        "--requirements",
        nargs="+",
        default=["requirements.txt"],
        help="Uno o varios archivos requirements",
    )
    parser.add_argument("--python", default=DEFAULT_PYTHON, help=f"Version Python objetivo ({DEFAULT_PYTHON})")
    parser.add_argument("--json", dest="json_path", help="Ruta para guardar informe JSON")
    parser.add_argument("--keep-temp", action="store_true", help="Conservar el venv temporal de --real-install")
    return parser.parse_args()


def main():
    args = parse_args()
    require_uv()

    requirements = []
    for item in args.requirements:
        req = Path(item)
        if not req.is_absolute():
            req = PROJECT_ROOT / req
        if not req.is_file():
            raise SystemExit(f"ERROR: no existe {req}")
        requirements.append(req)

    if args.dry_run:
        data = dry_run(requirements, args.python)
        print(f"Dry-run completado en {data['seconds']} s")
        print(f"Paquetes planificados: {data['planned_count']}")
    else:
        data = real_install(requirements, args.python, keep_temp=args.keep_temp)
        print(f"Instalacion temporal completada en {data['seconds']} s")
        print(f"Tiempo instalando paquetes: {data['install_seconds']} s")
        print(f"Tamano del venv: {data['venv_size_mb']} MB")
        print("Top paquetes por tamano:")
        for item in data["top_packages_by_size"][:10]:
            print(f"  {item['name']} {item['version']}: {item['size_mb']} MB")

    if args.json_path:
        write_json(args.json_path, data)


if __name__ == "__main__":
    main()
