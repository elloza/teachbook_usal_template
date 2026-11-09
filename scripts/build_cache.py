"""Shared filesystem helpers for the local book and Slidev build caches."""

import hashlib
import json
import os
import shutil
from contextlib import contextmanager
from pathlib import Path

from project_options import PROJECT_ROOT


BUILD_ROOT = PROJECT_ROOT / "book" / "_build"
CACHE_ROOT = BUILD_ROOT / ".cache"


def file_hash(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode("utf-8")).hexdigest()


def tree_hashes(root, *, ignored_dirs=(), ignored_files=()):
    files = {}
    for folder, dirs, names in os.walk(root):
        dirs[:] = [name for name in dirs if name not in ignored_dirs]
        for name in names:
            path = Path(folder) / name
            if name not in ignored_files and path.is_file():
                files[path.relative_to(root).as_posix()] = file_hash(path)
    return files


def read_cache_state(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def remove_build_tree(path):
    resolved = path.resolve()
    if not resolved.is_relative_to(BUILD_ROOT.resolve()) or resolved == BUILD_ROOT.resolve():
        raise ValueError(f"Ruta de compilación no segura: {path}")
    if path.is_symlink() or path.is_junction():
        raise ValueError(f"La salida de compilación no puede ser un enlace: {path}")
    if path.exists():
        shutil.rmtree(path)


@contextmanager
def build_lock():
    if BUILD_ROOT.resolve() != PROJECT_ROOT / "book" / "_build":
        raise SystemExit("ERROR: book/_build debe estar dentro del proyecto.")
    BUILD_ROOT.mkdir(parents=True, exist_ok=True)
    with (BUILD_ROOT / ".build.lock").open("a+b") as lock:
        try:
            if os.name == "nt":
                import msvcrt

                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise SystemExit("ERROR: ya hay una compilación en este proyecto. Espera a que termine.") from exc
        yield
