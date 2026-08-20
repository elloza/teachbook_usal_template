#!/usr/bin/env python3
"""Despliegue local del TeachBook por SFTP usando un .env privado."""

from __future__ import annotations

import argparse
import os
import posixpath
import re
import shutil
import socket
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VENV_DIR = PROJECT_ROOT / ".venv"
BUILD_DIR = PROJECT_ROOT / "book" / "_build" / "html"
TARGET_PYTHON = (3, 12)
REQUIRED_ENV = [
    "SFTP_SERVER",
    "SFTP_USERNAME",
    "SFTP_PASSWORD",
    "SFTP_REMOTE_DIR",
]
SECRET_NAME_HINTS = (
    "PASSWORD",
    "TOKEN",
    "PRIVATEKEY",
    "PRIVATE_KEY",
    "PRESHAREDKEY",
    "PRESHARED_KEY",
    "SECRET",
)


class DeployError(RuntimeError):
    """Error esperado con mensaje listo para el usuario."""


@dataclass(frozen=True)
class SftpConfig:
    server: str
    port: int
    username: str
    password: str
    remote_dir: str
    env_file: Path


def ensure_utf8_output() -> None:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in {"utf-8", "utf8"}:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.stderr.encoding and sys.stderr.encoding.lower() not in {"utf-8", "utf8"}:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def expected_venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def is_same_path(left: Path, right: Path) -> bool:
    try:
        left_text = str(left.resolve())
        right_text = str(right.resolve())
    except OSError:
        left_text = str(left.absolute())
        right_text = str(right.absolute())
    if os.name == "nt":
        return left_text.lower() == right_text.lower()
    return left_text == right_text


def ensure_project_venv() -> None:
    expected = expected_venv_python()
    if not expected.is_file():
        has_windows = (VENV_DIR / "Scripts" / "python.exe").is_file()
        has_posix = (VENV_DIR / "bin" / "python").is_file()
        print("ERROR: no se puede usar este script sin el .venv correcto del proyecto.")
        if os.name != "nt" and has_windows and not has_posix:
            print("Detectado .venv de Windows, pero este terminal es Linux/macOS/WSL.")
            print("Usa PowerShell o recrea .venv para este sistema solo si procede.")
        elif os.name == "nt" and has_posix and not has_windows:
            print("Detectado .venv de Linux/macOS/WSL, pero este terminal es Windows.")
            print("Usa Linux/macOS/WSL o recrea .venv para Windows solo si procede.")
        else:
            print("Ejecuta primero: python scripts/setup_env.py --yes")
        raise SystemExit(1)

    executable = Path(sys.executable)
    prefix = Path(sys.prefix)
    if not is_same_path(prefix, VENV_DIR) and not is_same_path(executable, expected):
        print("ERROR: ejecuta este script con el Python de .venv.")
        if os.name == "nt":
            print(r"Comando: .venv\Scripts\python.exe scripts\local\deploy_sftp_from_env.py --plan-only")
        else:
            print("Comando: .venv/bin/python scripts/local/deploy_sftp_from_env.py --plan-only")
        raise SystemExit(1)

    if sys.version_info[:2] != TARGET_PYTHON:
        found = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        expected_version = ".".join(str(part) for part in TARGET_PYTHON)
        raise DeployError(f".venv usa Python {found}; este proyecto requiere Python {expected_version}.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Publica el TeachBook por SFTP desde un ordenador local conectado a eduVPN. "
            "Por defecto NO sube nada: hace dry-run."
        )
    )
    parser.add_argument(
        "--env-file",
        default=str(PROJECT_ROOT / ".env"),
        help="Ruta al .env privado con SFTP_SERVER, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD y SFTP_REMOTE_DIR.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Ejecuta el despliegue real por SFTP.")
    mode.add_argument("--dry-run", action="store_true", help="Valida y construye, pero no sube archivos.")
    mode.add_argument(
        "--plan-only",
        action="store_true",
        help="Solo valida el .env y muestra un plan seguro; no conecta, no construye y no sube.",
    )
    parser.add_argument(
        "--build-policy",
        choices=["auto", "always", "never"],
        default="auto",
        help="auto construye si falta HTML; always reconstruye; never exige HTML ya existente.",
    )
    parser.add_argument(
        "--skip-pdf",
        action="store_true",
        help="No genera PDFs antes del HTML. Usar solo para pruebas rápidas, no para publicación final.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="Timeout en segundos para la comprobación de puerto y SFTP.",
    )
    return parser.parse_args()


def parse_env_file(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise DeployError(
            f"No existe el archivo .env indicado: {path}. "
            "Copia .env.example como .env y rellena los valores privados."
        )

    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise DeployError(f"El archivo {path} debe estar guardado como UTF-8.") from exc

    for index, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            raise DeployError(f"Linea {index} de {path.name}: se esperaba FORMATO=valor.")
        key, value = line.split("=", 1)
        key = key.strip()
        value = strip_inline_comment(value.strip())
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise DeployError(f"Linea {index} de {path.name}: nombre de variable no valido.")
        values[key] = unquote_env_value(value)

    return values


def strip_inline_comment(value: str) -> str:
    if not value or value[0] in {"'", '"'}:
        return value
    marker = value.find(" #")
    if marker >= 0:
        return value[:marker].strip()
    return value


def unquote_env_value(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        body = value[1:-1]
        if value[0] == '"':
            return (
                body.replace(r"\\", "\\")
                .replace(r"\"", '"')
                .replace(r"\n", "\n")
                .replace(r"\r", "\r")
                .replace(r"\t", "\t")
            )
        return body
    return value


def validate_remote_dir(remote_dir: str) -> str:
    remote_dir = remote_dir.strip()
    if remote_dir.startswith("/"):
        raise DeployError("SFTP_REMOTE_DIR debe ser una ruta relativa segura, por ejemplo public_html.")
    remote_dir = remote_dir.rstrip("/")
    unsafe = {"", ".", "..", "~", "~/"}
    if remote_dir in unsafe:
        raise DeployError("SFTP_REMOTE_DIR no puede estar vacio ni ser una ruta peligrosa.")
    if "\\" in remote_dir or ".." in remote_dir.split("/"):
        raise DeployError("SFTP_REMOTE_DIR debe ser una ruta relativa segura, por ejemplo public_html.")
    if not re.fullmatch(r"[A-Za-z0-9._/-]+", remote_dir):
        raise DeployError("SFTP_REMOTE_DIR solo puede contener letras, numeros, '.', '_', '-' y '/'.")
    return remote_dir


def load_config(env_file: Path) -> SftpConfig:
    values = parse_env_file(env_file)
    missing = [name for name in REQUIRED_ENV if not values.get(name)]
    if missing:
        raise DeployError(f"Faltan variables en {env_file.name}: {', '.join(missing)}.")

    raw_port = values.get("SFTP_PORT", "22").strip()
    if not raw_port.isdigit():
        raise DeployError("SFTP_PORT debe ser numerico.")
    port = int(raw_port)
    if port < 1 or port > 65535:
        raise DeployError("SFTP_PORT debe estar entre 1 y 65535.")

    return SftpConfig(
        server=values["SFTP_SERVER"].strip(),
        port=port,
        username=values["SFTP_USERNAME"].strip(),
        password=values["SFTP_PASSWORD"],
        remote_dir=validate_remote_dir(values["SFTP_REMOTE_DIR"]),
        env_file=env_file,
    )


def redacted_values(config: SftpConfig) -> list[str]:
    values = [config.password]
    for value in (config.server, config.username):
        if value and len(value) > 2:
            values.append(value)
    return values


def redact(text: str, config: SftpConfig | None = None, extra: dict[str, str] | None = None) -> str:
    redacted = text
    for key, value in (extra or {}).items():
        if value and any(hint in key.upper() for hint in SECRET_NAME_HINTS):
            redacted = redacted.replace(value, "***")
    if config:
        for value in redacted_values(config):
            if value:
                redacted = redacted.replace(value, "***")
    return redacted


def print_plan(config: SftpConfig, *, mode: str, skip_pdf: bool, build_policy: str) -> None:
    print("Plan de despliegue SFTP local")
    print("=" * 34)
    print(f"Modo: {mode}")
    print(f".env: {config.env_file}")
    print("Servidor: configurado")
    print(f"Puerto: {config.port}")
    print("Usuario: configurado")
    print(f"Directorio remoto: {config.remote_dir}")
    print(f"Build HTML: {BUILD_DIR.relative_to(PROJECT_ROOT)}")
    print(f"Politica de build: {build_policy}")
    print(f"PDF antes del HTML: {'no' if skip_pdf else 'si'}")
    print("Subida real: si y solo si se usa --apply")


def check_tcp_port(config: SftpConfig, timeout: float) -> None:
    print("Comprobando puerto SFTP y acceso por eduVPN...")
    try:
        with socket.create_connection((config.server, config.port), timeout=timeout):
            pass
    except OSError as exc:
        raise DeployError(
            "No se pudo abrir una conexion TCP al servidor SFTP configurado. "
            "Comprueba que eduVPN esta conectada, que el servidor/puerto son correctos "
            "y que el servidor acepta conexiones SFTP."
        ) from exc
    print("  OK puerto SFTP accesible.")


def lftp_path() -> str | None:
    return shutil.which("lftp")


def lftp_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$").replace("`", "\\`")
    return f'"{escaped}"'


def run_lftp_script(script: str, config: SftpConfig, *, timeout: float) -> subprocess.CompletedProcess[str]:
    executable = lftp_path()
    if not executable:
        raise DeployError("lftp no esta disponible.")
    try:
        return subprocess.run(
            [executable],
            input=script,
            cwd=str(PROJECT_ROOT),
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=max(timeout, 30.0),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise DeployError("lftp no respondio a tiempo. Comprueba eduVPN y el servidor SFTP.") from exc
    except OSError as exc:
        raise DeployError("No se pudo ejecutar lftp.") from exc


def lftp_open_script(config: SftpConfig) -> str:
    return "\n".join(
        [
            "set sftp:auto-confirm yes",
            "set net:max-retries 2",
            "set net:timeout 30",
            (
                "open -u "
                f"{lftp_quote(config.username)},{lftp_quote(config.password)} "
                f"-p {config.port} {lftp_quote('sftp://' + config.server)}"
            ),
        ]
    )


def check_remote_dir_with_lftp(config: SftpConfig, timeout: float) -> bool:
    if not lftp_path():
        return False
    print("Comprobando acceso SFTP y directorio remoto con lftp...")
    script = "\n".join(
        [
            lftp_open_script(config),
            f"cd {lftp_quote(config.remote_dir)}",
            "pwd",
            "bye",
            "",
        ]
    )
    result = run_lftp_script(script, config, timeout=timeout)
    if result.returncode != 0:
        safe_output = redact(result.stdout or "", config).strip()
        detail = f" Detalle: {safe_output}" if safe_output else ""
        raise DeployError(
            "No se pudo acceder por SFTP al directorio remoto configurado. "
            "Comprueba credenciales, eduVPN y que SFTP_REMOTE_DIR exista." + detail
        )
    print("  OK acceso SFTP y directorio remoto.")
    return True


def import_paramiko():
    try:
        import paramiko  # type: ignore[import-not-found]
    except ImportError as exc:
        command = (
            r".venv\Scripts\python.exe -m pip install paramiko"
            if os.name == "nt"
            else ".venv/bin/python -m pip install paramiko"
        )
        raise DeployError(
            "lftp no esta disponible y falta la dependencia opcional paramiko. "
            f"Instalala dentro de .venv con: {command}"
        ) from exc
    return paramiko


def open_paramiko_sftp(config: SftpConfig, timeout: float):
    paramiko = import_paramiko()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=config.server,
            port=config.port,
            username=config.username,
            password=config.password,
            timeout=timeout,
            banner_timeout=timeout,
            auth_timeout=timeout,
            look_for_keys=False,
            allow_agent=False,
        )
        return client, client.open_sftp()
    except Exception as exc:
        client.close()
        raise DeployError(
            "No se pudo abrir una sesion SFTP. Comprueba credenciales, eduVPN y servidor."
        ) from exc


def check_remote_dir_with_paramiko(config: SftpConfig, timeout: float) -> None:
    print("Comprobando acceso SFTP y directorio remoto con paramiko...")
    client, sftp = open_paramiko_sftp(config, timeout)
    try:
        attrs = sftp.stat(config.remote_dir)
        if not stat.S_ISDIR(attrs.st_mode):
            raise DeployError("SFTP_REMOTE_DIR existe, pero no es un directorio.")
    except FileNotFoundError as exc:
        raise DeployError("SFTP_REMOTE_DIR no existe en el servidor.") from exc
    finally:
        sftp.close()
        client.close()
    print("  OK acceso SFTP y directorio remoto.")


def check_remote_dir(config: SftpConfig, timeout: float) -> str:
    if check_remote_dir_with_lftp(config, timeout):
        return "lftp"
    check_remote_dir_with_paramiko(config, timeout)
    return "paramiko"


def run_project_command(args: list[str], *, label: str) -> None:
    print(label)
    command = [sys.executable, *args]
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    try:
        result = subprocess.run(
            command,
            cwd=str(PROJECT_ROOT),
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        raise DeployError(f"No se pudo ejecutar {args[0]}.") from exc
    if result.returncode != 0:
        raise DeployError(f"Fallo el paso: {label}")


def build_output_exists() -> bool:
    return (BUILD_DIR / "index.html").is_file() and (BUILD_DIR / "_static").is_dir()


def ensure_build(skip_pdf: bool, build_policy: str) -> None:
    run_project_command(["scripts/check_encoding.py"], label="Comprobando UTF-8...")
    run_project_command(["scripts/optimize_static_assets.py", "--check"], label="Comprobando assets estaticos...")

    if build_policy == "never":
        if not build_output_exists():
            raise DeployError("No existe book/_build/html completo. Ejecuta build o usa --build-policy auto.")
        print("Build HTML existente: OK.")
        return

    should_build = build_policy == "always" or not build_output_exists() or not skip_pdf
    if not should_build:
        print("Build HTML existente: OK. No se reconstruye con --build-policy auto.")
        return

    if not skip_pdf:
        run_project_command(["scripts/setup_env.py", "--yes", "--extras", "pdf"], label="Preparando dependencias PDF...")
    if not skip_pdf:
        run_project_command(["scripts/setup_latex.py", "--yes", "--full"], label="Preparando toolchain PDF...")
        run_project_command(["scripts/export_pdf.py", "--engine", "auto"], label="Generando PDFs...")
    else:
        print("Generacion de PDFs omitida por --skip-pdf.")
    run_project_command(["scripts/build_book.py"], label="Compilando HTML...")
    (BUILD_DIR / ".nojekyll").touch()
    if not build_output_exists():
        raise DeployError("El build HTML termino sin generar book/_build/html/index.html y _static.")
    print("Build HTML listo.")


def deploy_with_lftp(config: SftpConfig, timeout: float) -> None:
    print("Desplegando con lftp mirror -R --delete --parallel=4...")
    local_dir = BUILD_DIR.as_posix()
    script = "\n".join(
        [
            lftp_open_script(config),
            f"mirror -R --delete --parallel=4 --verbose {lftp_quote(local_dir)} {lftp_quote(config.remote_dir)}",
            "bye",
            "",
        ]
    )
    result = run_lftp_script(script, config, timeout=max(timeout, 120.0))
    if result.returncode != 0:
        safe_output = redact(result.stdout or "", config).strip()
        detail = f" Detalle: {safe_output}" if safe_output else ""
        raise DeployError("Fallo el despliegue con lftp." + detail)
    print("Despliegue SFTP completado con lftp.")


def remote_join(base: str, relative: str) -> str:
    if not relative:
        return base
    return posixpath.join(base, relative.replace("\\", "/"))


def list_remote_tree(sftp, root: str) -> tuple[set[str], set[str]]:
    files: set[str] = set()
    dirs: set[str] = set()

    def walk(remote_path: str, rel: str = "") -> None:
        for attrs in sftp.listdir_attr(remote_path):
            name = attrs.filename
            child_rel = posixpath.join(rel, name) if rel else name
            child_remote = posixpath.join(remote_path, name)
            if stat.S_ISDIR(attrs.st_mode):
                dirs.add(child_rel)
                walk(child_remote, child_rel)
            elif stat.S_ISREG(attrs.st_mode):
                files.add(child_rel)

    walk(root)
    return files, dirs


def local_tree(root: Path) -> tuple[set[str], set[str]]:
    files: set[str] = set()
    dirs: set[str] = set()
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            dirs.add(rel)
        elif path.is_file():
            files.add(rel)
    return files, dirs


def ensure_remote_dirs(sftp, remote_root: str, dirs: set[str]) -> None:
    for rel in sorted(dirs, key=lambda item: (item.count("/"), item)):
        remote = remote_join(remote_root, rel)
        try:
            sftp.stat(remote)
        except FileNotFoundError:
            sftp.mkdir(remote)


def deploy_with_paramiko(config: SftpConfig, timeout: float) -> None:
    print("Desplegando con fallback paramiko (mirror con borrado, sin paralelismo)...")
    client, sftp = open_paramiko_sftp(config, timeout)
    try:
        local_files, local_dirs = local_tree(BUILD_DIR)
        remote_files, remote_dirs = list_remote_tree(sftp, config.remote_dir)
        ensure_remote_dirs(sftp, config.remote_dir, local_dirs)

        uploaded = 0
        for rel in sorted(local_files):
            local_path = BUILD_DIR / rel
            remote_path = remote_join(config.remote_dir, rel)
            sftp.put(str(local_path), remote_path)
            uploaded += 1

        deleted_files = 0
        for rel in sorted(remote_files - local_files, reverse=True):
            sftp.remove(remote_join(config.remote_dir, rel))
            deleted_files += 1

        deleted_dirs = 0
        for rel in sorted(remote_dirs - local_dirs, key=lambda item: item.count("/"), reverse=True):
            sftp.rmdir(remote_join(config.remote_dir, rel))
            deleted_dirs += 1
    finally:
        sftp.close()
        client.close()
    print(f"Despliegue SFTP completado con paramiko: {uploaded} archivos subidos, {deleted_files} archivos borrados, {deleted_dirs} carpetas borradas.")


def deploy(config: SftpConfig, backend: str, timeout: float) -> None:
    if backend == "lftp" and lftp_path():
        deploy_with_lftp(config, timeout)
    else:
        deploy_with_paramiko(config, timeout)


def main() -> int:
    ensure_utf8_output()
    args = parse_args()
    ensure_project_venv()
    env_file = Path(args.env_file).expanduser()
    if not env_file.is_absolute():
        env_file = (PROJECT_ROOT / env_file).resolve()
    config = load_config(env_file)

    mode = "apply" if args.apply else "plan-only" if args.plan_only else "dry-run"
    print_plan(config, mode=mode, skip_pdf=args.skip_pdf, build_policy=args.build_policy)
    if args.plan_only:
        print("Plan validado. No se ha conectado al servidor ni se ha construido el libro.")
        return 0

    check_tcp_port(config, args.timeout)
    backend = check_remote_dir(config, args.timeout)
    ensure_build(skip_pdf=args.skip_pdf, build_policy=args.build_policy)

    if not args.apply:
        print("Dry-run completado: no se ha subido ningun archivo.")
        print(f"Backend que se usaria para desplegar: {backend}.")
        return 0

    deploy(config, backend, args.timeout)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DeployError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
