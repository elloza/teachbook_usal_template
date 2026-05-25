import io
import subprocess
import sys
import datetime

# Fix: Windows cp1252 can't encode emojis — force UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def run_git(args):
    try:
        subprocess.check_call(["git"] + args)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando: git {' '.join(args)}")
        sys.exit(1)


def run_project_check(script):
    try:
        subprocess.check_call([sys.executable, script])
    except subprocess.CalledProcessError:
        print(f"❌ La comprobación local ha fallado: {script}")
        sys.exit(1)


def has_staged_changes():
    return subprocess.call(["git", "diff", "--cached", "--quiet"]) != 0


def main():
    print("🚀 Iniciando proceso de guardado y publicación...")

    # 1. Status
    print("\n📄 Estado actual:")
    run_git(["status", "-s"])

    # 2. Local preflight checks
    print("\n🔎 Comprobando codificación UTF-8...")
    run_project_check("scripts/check_encoding.py")

    # 3. Add all changes
    print("\n➕ Añadiendo cambios...")
    run_git(["add", "."])
    if not has_staged_changes():
        print("⚠️  No hay cambios para guardar.")
        return

    # 4. Commit
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Actualización automática {timestamp}"
    print(f"\n💾 Guardando versión: {message}")
    run_git(["commit", "-m", message])

    # 5. Push
    print("\n☁️  Subiendo a GitHub...")
    run_git(["push"])

    print("\n✨ ¡Todo guardado y publicado correctamente!")


if __name__ == "__main__":
    main()
