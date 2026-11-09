"""Project settings shared by setup, build, preview and CI."""

import json
import re
import shutil
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_OPTIONS = PROJECT_ROOT / "teachbook.json"
SLIDES_DIR = PROJECT_ROOT / "slides"
SLIDEV_CLI = SLIDES_DIR / "node_modules" / "@slidev" / "cli" / "bin" / "slidev.mjs"
MIN_NODE_VERSION = (22, 18, 0)


def slides_enabled():
    try:
        options = json.loads(PROJECT_OPTIONS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return False
    except (OSError, ValueError) as exc:
        raise SystemExit(f"ERROR: no se pudo leer teachbook.json: {exc}") from exc
    if not isinstance(options, dict) or type(options.get("slides", False)) is not bool:
        raise SystemExit('ERROR: en teachbook.json, "slides" debe ser true o false.')
    return options.get("slides", False)


def node_runtime():
    node = shutil.which("node")
    if node:
        try:
            result = subprocess.run(
                [node, "--version"], capture_output=True, text=True, encoding="utf-8",
                errors="replace", check=False, timeout=15,
            )
        except (OSError, subprocess.TimeoutExpired):
            pass
        else:
            version = result.stdout.strip()
            match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", version)
            if result.returncode == 0 and match and tuple(map(int, match.groups())) >= MIN_NODE_VERSION:
                return node, version
    raise SystemExit(
        "ERROR: Slidev requiere Node.js >= 22.18.0. Instálalo desde https://nodejs.org/ "
        'o cambia "slides" a false en teachbook.json.'
    )


if __name__ == "__main__":
    print("true" if slides_enabled() else "false")
