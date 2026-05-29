import io
import subprocess
import sys
import os
import glob
import shutil
import json
import time
from datetime import datetime
from pathlib import Path


# Fix: Windows cp1252 can't encode emojis — force UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import yaml
except ModuleNotFoundError as exc:
    if exc.name != "yaml":
        raise
    print("ERROR: falta PyYAML, necesario para leer book/_config_<lang>.yml.")
    print("Instala/actualiza el entorno con:")
    if os.name == "nt":
        print(r"   .venv\Scripts\python.exe scripts\setup_env.py --yes")
    else:
        print("   .venv/bin/python scripts/setup_env.py --yes")
    raise SystemExit(1)

from collect_used_bibliography import BibliographyError, collect_used_bibliography
from pdf_names import DEFAULT_PDF_FILENAME, pdf_filename_for_lang

VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv


def write_command_log(cmd, stdout, stderr):
    """Persist full build output so quiet mode never hides errors."""
    log_dir = os.path.join(os.getcwd(), ".build_logs")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = os.path.join(log_dir, f"html-{timestamp}.log")
    with open(log_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("$ " + " ".join(cmd) + "\n\n")
        if stdout:
            f.write("--- STDOUT ---\n")
            f.write(stdout)
            if not stdout.endswith("\n"):
                f.write("\n")
        if stderr:
            f.write("--- STDERR ---\n")
            f.write(stderr)
            if not stderr.endswith("\n"):
                f.write("\n")
    return log_path


def print_output_tail(stdout, stderr, lines=80):
    """Show useful failure context without flooding the terminal."""
    combined = "\n".join(part for part in (stdout, stderr) if part)
    tail = combined.splitlines()[-lines:]
    if tail:
        print("\n".join(tail))


def get_jupyter_book():
    """Returns the path to jupyter-book executable. Prefers venv, falls back to system."""
    if os.name == "nt":
        venv_jb = os.path.join(".venv", "Scripts", "jupyter-book.exe")
    else:
        venv_jb = os.path.join(".venv", "bin", "jupyter-book")
    if os.path.isfile(venv_jb):
        return venv_jb
    # Fallback: system-wide jupyter-book (e.g. CI environments)
    return "jupyter-book"


def run_jupyter_book_build(cmd, label, attempts=3):
    """Run a Jupyter Book build with retries for transient network-backed extensions.

    Kroki diagrams are rendered through a remote service during the build. In CI or
    first-use setups, a temporary network timeout should not make the whole setup
    look broken, so retry the exact same build before failing for real.
    """
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            print(f"🚀 Ejecutando build {label} ({attempt}/{attempts}): {' '.join(cmd)}")
            if VERBOSE:
                subprocess.check_call(cmd, shell=(os.name == "nt"))
            else:
                result = subprocess.run(
                    cmd,
                    shell=(os.name == "nt"),
                    check=False,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                log_path = write_command_log(cmd, result.stdout, result.stderr)
                if result.returncode != 0:
                    print(f"❌ Build {label} falló. Log completo: {log_path}")
                    print("Últimas líneas relevantes:")
                    print_output_tail(result.stdout, result.stderr)
                    raise subprocess.CalledProcessError(result.returncode, cmd)
                print(f"   ✅ Build {label} completado. Log completo: {log_path}")
            return
        except subprocess.CalledProcessError as exc:
            last_error = exc
            if attempt == attempts:
                break
            wait_seconds = 10 * attempt
            print(
                f"⚠️  Build {label} falló en el intento {attempt}. "
                f"Reintentando en {wait_seconds}s..."
            )
            time.sleep(wait_seconds)
    raise last_error


# Mapping of language codes to display names (ISO 639-1)
LANG_DISPLAY_NAMES = {
    "ar": "العربية",
    "bg": "Български",
    "ca": "Català",
    "cs": "Čeština",
    "da": "Dansk",
    "de": "Deutsch",
    "el": "Ελληνικά",
    "en": "English",
    "es": "Español",
    "et": "Eesti",
    "eu": "Euskara",
    "fi": "Suomi",
    "fr": "Français",
    "ga": "Gaeilge",
    "gl": "Galego",
    "he": "עברית",
    "hi": "हिन्दी",
    "hr": "Hrvatski",
    "hu": "Magyar",
    "id": "Bahasa Indonesia",
    "it": "Italiano",
    "ja": "日本語",
    "ko": "한국어",
    "lt": "Lietuvių",
    "lv": "Latviešu",
    "ms": "Bahasa Melayu",
    "nl": "Nederlands",
    "no": "Norsk",
    "pl": "Polski",
    "pt": "Português",
    "ro": "Română",
    "ru": "Русский",
    "sk": "Slovenčina",
    "sl": "Slovenščina",
    "sq": "Shqip",
    "sr": "Српски",
    "sv": "Svenska",
    "th": "ไทย",
    "tr": "Türkçe",
    "uk": "Українська",
    "vi": "Tiếng Việt",
    "zh": "中文",
}

BOOK_DIR = "book"
BUILD_ROOT = os.path.join(BOOK_DIR, "_build")
FINAL_HTML_DIR = os.path.join(BUILD_ROOT, "html")


def get_project_default_language():
    """Reads the default/primary language from _config.yml's 'language' field."""
    config_path = os.path.join(BOOK_DIR, "_config.yml")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            if config and "language" in config:
                return config["language"]
    return "es"  # Fallback


def get_languages():
    """Detects languages based on _config_<lang>.yml files."""
    configs = glob.glob(os.path.join(BOOK_DIR, "_config_*.yml"))
    languages = []

    for conf in configs:
        filename = os.path.basename(conf)
        # Extract 'es' from '_config_es.yml'
        lang_code = filename.replace("_config_", "").replace(".yml", "")
        languages.append(lang_code)

    if not languages and os.path.exists(os.path.join(BOOK_DIR, "_config.yml")):
        return ["default"]  # Single language mode

    return sorted(languages)


def generate_languages_json(languages, output_static_dir=None):
    """Generates a JSON file with available languages for the JS switcher."""
    lang_data = []
    for lang in languages:
        if lang == "default":
            continue
        lang_data.append(
            {"code": lang, "name": LANG_DISPLAY_NAMES.get(lang, lang.upper())}
        )

    # Target directory: either source or specified build dir
    target_dir = (
        output_static_dir if output_static_dir else os.path.join(BOOK_DIR, "_static")
    )

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    json_path = os.path.join(target_dir, "languages.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(lang_data, f, indent=2, ensure_ascii=False)

    print(f"🌍 Archivo de idiomas generado en: {json_path}")


def validate_bibliography_for_language(lang, content_dir, bib_file):
    """Validate citation keys before Sphinx starts building the language."""
    try:
        result = collect_used_bibliography(
            content_dir=Path(content_dir),
            bib_file=Path(bib_file),
        )
    except BibliographyError as exc:
        print(f"❌ Error de bibliografía en '{lang}':")
        print(exc)
        raise

    print(
        f"📚 Bibliografía {lang}: "
        f"{result.citation_count} cita(s), "
        f"{len(result.used_keys)} clave(s) usadas."
    )


def fix_pdf_paths(build_dir, pdf_filename):
    """Fixes relative paths for the PDF download button in HTML files within a specific build dir."""
    print(f"🔧 Corrigiendo rutas del botón PDF en {build_dir}...")

    for html_file in glob.glob(os.path.join(build_dir, "**", "*.html"), recursive=True):
        rel_to_root = os.path.relpath(build_dir, os.path.dirname(html_file))

        if rel_to_root == ".":
            correct_path = f"_static/{pdf_filename}"
        else:
            correct_path = f"{rel_to_root}/_static/{pdf_filename}".replace("\\", "/")

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        target_string = f"_static/{pdf_filename}"

        if target_string in content:
            new_content = content.replace(
                f'href="{target_string}"', f'href="{correct_path}"'
            )

            if new_content != content:
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(new_content)


def fix_html_asset_paths(html_file):
    """Fix asset paths in HTML files moved from build root to language subdirectory.

    Sphinx generates search.html/genindex.html at the build root where _static/
    is a sibling directory. When we move these files into /es/ or /en/,
    all _static/ references must be prefixed with ../ to point to the root _static/.

    Also fixes _sources/ paths and data-content_root attribute.
    """
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Fix data-content_root: "./" → "../" (points from /es/ to root)
    content = content.replace('data-content_root="./"', 'data-content_root="../"')

    # Fix all relative _static/ references: href="_static/..." → href="../_static/..."
    # and src="_static/..." → src="../_static/..."
    # Be careful not to double-fix: don't match already-correct ../_static/
    import re

    content = re.sub(r'(href|src)="(_static/)', r'\1="../\2', content)
    content = re.sub(r'(href|src)="(\./_static/)', r'\1="../\2', content)

    # Fix _sources/ paths similarly
    content = re.sub(r'(href|src)="(_sources/)', r'\1="../\2', content)

    # Fix _downloads/ paths
    content = re.sub(r'(href|src)="(_downloads/)', r'\1="../\2', content)

    if content != original:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   🔧 Fixed asset paths in {os.path.basename(html_file)}")
    else:
        print(f"   ℹ️ No path fixes needed in {os.path.basename(html_file)}")


def fix_searchindex_paths(searchindex_file, lang):
    """Fix docnames in searchindex.js to remove the language prefix.

    Sphinx builds the standalone project with content inside a lang/ subfolder.
    So docnames look like 'es/01_tutorial/page'. When search results render
    on /es/search.html, Sphinx constructs the URL as 'es/01_tutorial/page.html'
    which resolves to /es/es/01_tutorial/page.html (DOUBLE es/ → 404).

    Fix: replace all occurrences of 'es/' or 'en/' prefix in docnames with ''.
    """
    import re as _re

    with open(searchindex_file, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Pattern: in the JSON, docnames are quoted strings like "es/01_tutorial/page"
    # We need to strip the "es/" or "en/" prefix from all of them
    # The prefix appears in docnames, filenames, and possibly objects/terms references
    prefix = f"{lang}/"

    # Replace "es/ or 'es/ at the start of a JSON string value
    # Be careful: only replace when it's a path prefix, not mid-string
    content = _re.sub(f'"{_re.escape(prefix)}', '"', content)

    if content != original:
        with open(searchindex_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   🔧 Fixed searchindex.js: stripped '{prefix}' prefix from all paths")
    else:
        print(
            f"   ℹ️ searchindex.js: no '{prefix}' prefix found (may already be correct)"
        )


def fix_duplicate_thebe_scripts(html_file):
    """Remove duplicated inline Thebe config script declarations.

    Some generated pages include duplicate inline script blocks declaring
    THEBE_JS_URL / selectors twice, which triggers a browser SyntaxError.
    Keep only the first occurrence.
    """
    import re

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    pattern = re.compile(
        r'<script>const THEBE_JS_URL = ".*?"; const thebe_selector = ".*?"; const thebe_selector_input = ".*?"; const thebe_selector_output = ".*?"</script>',
        re.DOTALL,
    )
    matches = pattern.findall(content)
    if len(matches) > 1:
        first = matches[0]
        content = pattern.sub("", content)
        insert_after = '<script src="../_static/design-tabs.js?v=f930bc37"></script>'
        if insert_after in content:
            content = content.replace(insert_after, insert_after + "\n    " + first, 1)
        else:
            content = first + "\n" + content

    if content != original:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   🔧 Removed duplicated Thebe script in {os.path.basename(html_file)}")


def build_language(lang):
    """Builds the book for a specific language using a standalone temporary directory."""
    print(f"\n🔨 Construyendo versión STANDALONE: {lang.upper()}...")

    if lang == "default":
        # Default behavior: build the root book (usually Spanish)
        config_file = "_config.yml"
        toc_file = "_toc.yml"
        build_cache_dir = os.path.join(BOOK_DIR, "_build")
        final_dest = FINAL_HTML_DIR
        pdf_name = DEFAULT_PDF_FILENAME

        # Standard build logic for default
        if os.path.exists(build_cache_dir):
            shutil.rmtree(build_cache_dir)

        cmd = [
            get_jupyter_book(),
            "build",
            os.path.abspath(BOOK_DIR),
            "--config",
            os.path.abspath(os.path.join(BOOK_DIR, config_file)),
            "--toc",
            os.path.abspath(os.path.join(BOOK_DIR, toc_file)),
            "--all",
        ]
        try:
            validate_bibliography_for_language(
                lang,
                os.path.abspath(BOOK_DIR),
                os.path.abspath(os.path.join(BOOK_DIR, "_static", "references.bib")),
            )
            run_jupyter_book_build(cmd, "DEFAULT")
            print(f"✅ Versión default lista en: {final_dest}")
        except BibliographyError:
            print(f"❌ Error validando bibliografía del idioma: {lang}")
            sys.exit(1)
        except subprocess.CalledProcessError:
            print(f"❌ Error compilando idioma: {lang}")
            sys.exit(1)
        return

    # LOCALIZED STANDALONE BUILD (en, fr, etc.)
    config_file = f"_config_{lang}.yml"
    toc_file = f"_toc_{lang}.yml"
    pdf_name = pdf_filename_for_lang(lang)

    # 1. Create temporary standalone project AT ROOT to avoid recursion/path issues
    # Use _temp_build_{lang}
    temp_build_root = os.path.abspath(os.path.join(os.getcwd(), f"_temp_build_{lang}"))
    if os.path.exists(temp_build_root):
        shutil.rmtree(temp_build_root)
    os.makedirs(temp_build_root)

    # 2. Copy localized content AS A SUBFOLDER to keep paths valid (e.g., temp_en/en/intro.md)
    lang_src_dir = os.path.join(BOOK_DIR, lang)
    lang_dst_dir = os.path.join(temp_build_root, lang)
    if not os.path.exists(lang_src_dir):
        print(
            f"❌ Error: No existe la carpeta de contenido para '{lang}': {lang_src_dir}"
        )
        return

    print(f"📂 Preparando entorno standalone en: {temp_build_root}")
    print(f"📂 Copiando contenido de '{lang}' a carpeta interna para mantener rutas...")
    shutil.copytree(lang_src_dir, lang_dst_dir)

    # 3. Copy _static folder (required for logo, css, js)
    static_src = os.path.join(BOOK_DIR, "_static")
    static_dst = os.path.join(temp_build_root, "_static")
    if os.path.exists(static_src):
        shutil.copytree(static_src, static_dst)

    # 4. Copy and rename config/toc
    dest_config = os.path.join(temp_build_root, "_config.yml")
    shutil.copy2(os.path.join(BOOK_DIR, config_file), dest_config)
    shutil.copy2(
        os.path.join(BOOK_DIR, toc_file), os.path.join(temp_build_root, "_toc.yml")
    )

    # Sanitize config to prevent self-exclusion
    sanitize_config(dest_config)

    # 5. Build from the temp directory (Explicit config)
    cmd = [
        get_jupyter_book(),
        "build",
        temp_build_root,
        "--config",
        dest_config,
        "--all",
        "-v",
    ]

    try:
        validate_bibliography_for_language(
            lang,
            lang_dst_dir,
            os.path.join(static_dst, "references.bib"),
        )
        run_jupyter_book_build(cmd, f"STANDALONE ({lang})")

        # DEBUG: See what was created
        debug_directory(temp_build_root)

        # The output will be in temp_build_root/_build/html/en/ (since en is a subfolder)
        built_html_path_nested = os.path.join(temp_build_root, "_build", "html", lang)
        final_dest = os.path.join(FINAL_HTML_DIR, lang)

        if not os.path.exists(built_html_path_nested):
            built_html_path_nested = os.path.join(temp_build_root, "_build", "html")

        # Fix PDF paths BEFORE moving
        if os.path.exists(built_html_path_nested):
            fix_pdf_paths(built_html_path_nested, pdf_name)

        print(f"🚚 Moviendo de {built_html_path_nested} a {final_dest}")
        if os.path.exists(final_dest):
            shutil.rmtree(final_dest)

        # Ensure parent dir exists
        os.makedirs(os.path.dirname(final_dest), exist_ok=True)

        shutil.copytree(built_html_path_nested, final_dest)
        print(f"✅ Versión {lang} movida correctamente.")

        # Fix duplicated inline Thebe config blocks on all generated pages
        for root, _dirs, files in os.walk(final_dest):
            for filename in files:
                if filename.endswith(".html"):
                    fix_duplicate_thebe_scripts(os.path.join(root, filename))

        # CRITICAL FIX: Copy search files from temp build root to language dir
        # Sphinx generates search.html, genindex.html, and searchindex.js at the HTML root,
        # but pages reference them with relative paths like "../search.html"
        temp_html_root = os.path.join(temp_build_root, "_build", "html")
        search_files = ["search.html", "genindex.html", "searchindex.js"]
        for search_file in search_files:
            src = os.path.join(temp_html_root, search_file)
            if os.path.isfile(src):
                dst = os.path.join(final_dest, search_file)
                shutil.copy2(src, dst)
                print(f"📋 Copied {search_file} to {final_dest}")

                # CRITICAL: Fix asset paths in HTML files
                # Sphinx generated these files at the build root where _static/ is
                # a sibling. Now they're inside /es/ so _static/ is at ../_static/
                if search_file.endswith(".html"):
                    fix_html_asset_paths(dst)

                # CRITICAL: Fix searchindex.js docnames (strip "es/" prefix)
                # Without this, search results link to /es/es/page.html (double prefix → 404)
                if search_file == "searchindex.js":
                    fix_searchindex_paths(dst, lang)

        # CRITICAL FIX: Merge the generated _static folder (containing theme assets)
        # from the temp build to the final root _static folder.
        temp_static_dir = os.path.join(temp_build_root, "_build", "html", "_static")
        final_static_dir = os.path.join(FINAL_HTML_DIR, "_static")

        if os.path.exists(temp_static_dir):
            print(
                f"📦 Merging theme assets from temp build ({lang}) to global _static..."
            )

            # DEBUG: List source files to verify we actually have something to copy
            print(f"   🔍 Source _static content ({temp_static_dir}):")
            try:
                for item in os.listdir(temp_static_dir):
                    print(f"      - {item}")
            except Exception as e:
                print(f"      ⚠️ Error listing source: {e}")

            if not os.path.exists(final_static_dir):
                os.makedirs(final_static_dir)

            # Use the robust merge_dir_into (now global)
            merge_dir_into(temp_static_dir, final_static_dir)

            # DEBUG: Verify copy
            print(
                f"   ✅ Merge complete. Final _static count: {len(os.listdir(final_static_dir))}"
            )

        # CRITICAL FIX: Sphinx stores document images in a root-level _images/
        # directory, while localized pages live under /es/ and /en/ and link to
        # ../../_images/.... A clean multi-language build must therefore merge
        # each temp build's _images directory into the final root _images.
        temp_images_dir = os.path.join(temp_build_root, "_build", "html", "_images")
        final_images_dir = os.path.join(FINAL_HTML_DIR, "_images")
        if os.path.exists(temp_images_dir):
            print(f"🖼️  Merging document images from temp build ({lang}) to global _images...")
            if not os.path.exists(final_images_dir):
                os.makedirs(final_images_dir)
            merge_dir_into(temp_images_dir, final_images_dir)

        # Sphinx stores files referenced as downloads in a root-level _downloads/
        # directory. Localized pages point to ../_downloads/..., so merge it too.
        temp_downloads_dir = os.path.join(temp_build_root, "_build", "html", "_downloads")
        final_downloads_dir = os.path.join(FINAL_HTML_DIR, "_downloads")
        if os.path.exists(temp_downloads_dir):
            print(f"   Merging downloads from temp build ({lang}) to global _downloads...")
            if not os.path.exists(final_downloads_dir):
                os.makedirs(final_downloads_dir)
            merge_dir_into(temp_downloads_dir, final_downloads_dir)

    except subprocess.CalledProcessError:
        print(f"❌ Error compilando idioma standalone: {lang}")
        sys.exit(1)
    except BibliographyError:
        print(f"❌ Error validando bibliografía del idioma standalone: {lang}")
        sys.exit(1)
    finally:
        # Cleanup temp directory
        if os.path.exists(temp_build_root):
            shutil.rmtree(temp_build_root)


def merge_dir_into(src_dir, dst_dir):
    """Merge src_dir into dst_dir without deleting dst_dir first.
    Overwrites files that already exist. Skips locked files gracefully."""
    print(f"   🔄 Merging '{src_dir}' -> '{dst_dir}'")
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        target_dir = os.path.join(dst_dir, rel_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            try:
                shutil.copy2(src_file, dst_file)
            except PermissionError:
                print(f"      ⚠️  Skipped locked file: {dst_file}")
            except Exception as e:
                print(f"      ⚠️  Copy error: {e}")


def debug_directory(path):
    """Prints the directory structure for debugging."""
    if not VERBOSE:
        return
    print(f"📂 [DEBUG] Listing contents of: {path}")
    for root, dirs, files in os.walk(path):
        level = root.replace(path, "").count(os.sep)
        indent = " " * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")


def sanitize_config(config_path):
    """
    Removes exclusion patterns entirely to prevent EISDIR errors in temp environment.
    Since we are in a clean temp dir, we don't need complex excludes.
    """
    try:
        debug_directory(os.path.dirname(config_path))
        if VERBOSE:
            print(f"📄 [DEBUG] Reading config from: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
            if VERBOSE:
                print(content)
                print("-" * 20)
            lines = content.splitlines(keepends=True)

        new_lines = []
        exclude_written = False
        for line in lines:
            if "exclude_patterns:" in line:
                # Force a safe, minimal exclusion list
                # This ensures _build is ignored (no EISDIR) and nothing else is accidentally ignored
                new_lines.append(
                    'exclude_patterns: ["_build", "**.ipynb_checkpoints", ".git", ".github"]\n'
                )
                exclude_written = True
                continue
            new_lines.append(line)

        if not exclude_written:
            new_lines.append(
                'exclude_patterns: ["_build", "**.ipynb_checkpoints", ".git", ".github"]\n'
            )

        with open(config_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"🔧 Configuración saneada (excludes minimos seguros) en: {config_path}")
    except Exception as e:
        print(f"⚠️ Error saneando configuración: {e}")


def create_redirect_index(default_lang="es"):
    """Creates a root index.html that redirects to the default language."""
    redirect_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url={default_lang}/intro.html" />
        <script>window.location.href = "{default_lang}/intro.html";</script>
    </head>
    <body>
        <p>Redirecting to <a href="{default_lang}/intro.html">{default_lang} version</a>...</p>
    </body>
    </html>
    """
    with open(os.path.join(FINAL_HTML_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(redirect_html)
    print(f"🔀 Redirección raíz creada apuntando a: /{default_lang}/")


def main():
    print("📚 Iniciando proceso de construcción multi-idioma...")
    languages = get_languages()
    print(f"🔍 Idiomas detectados: {languages}")

    # Start from a clean HTML output tree so deleted assets do not survive
    # between builds. The source assets remain in book/_static.
    if os.path.exists(FINAL_HTML_DIR):
        shutil.rmtree(FINAL_HTML_DIR)
    os.makedirs(FINAL_HTML_DIR)

    # Pre-create root _static to avoid race conditions or missing dirs
    final_static = os.path.join(FINAL_HTML_DIR, "_static")
    if not os.path.exists(final_static):
        os.makedirs(final_static)

    generate_languages_json(languages)

    for lang in languages:
        build_language(lang)

    # 1. Merge our custom static files into the root _static
    custom_static = os.path.join(BOOK_DIR, "_static")
    if os.path.exists(custom_static):
        merge_dir_into(custom_static, final_static)
        print(f"📦 Custom static assets merged into: {final_static}")

    # 2. Regenerate languages.json in ALL _static directories (Just in case)
    generate_languages_json(languages, final_static)

    # 3. Copy languages.json into each per-language _static directory
    # Each standalone build has its own _static/ and the JS resolves relative to URL_ROOT
    # which points to the per-language root (e.g., /es/), not the site root.
    for lang in languages:
        if lang == "default":
            continue
        lang_static = os.path.join(FINAL_HTML_DIR, lang, "_static")
        if os.path.exists(lang_static):
            lang_json_src = os.path.join(final_static, "languages.json")
            lang_json_dst = os.path.join(lang_static, "languages.json")
            shutil.copy2(lang_json_src, lang_json_dst)
            print(f"📋 Copied languages.json to {lang_static}")

    if "default" not in languages and len(languages) > 0:
        default_lang = get_project_default_language()
        if default_lang not in languages:
            default_lang = languages[0]
        create_redirect_index(default_lang)

        # Create root search.html that redirects to default language search
        # CRITICAL: preserve query string (?q=...) so search terms survive the redirect
        search_redirect = f"""<!DOCTYPE html>
<html>
<head>
    <script>
      var query = window.location.search;
      window.location.href = "{default_lang}/search.html" + query;
    </script>
    <meta http-equiv="refresh" content="0; url={default_lang}/search.html" />
</head>
<body>
    <p>Redirecting to <a href="{default_lang}/search.html">search</a>...</p>
</body>
</html>"""
        with open(
            os.path.join(FINAL_HTML_DIR, "search.html"), "w", encoding="utf-8"
        ) as f:
            f.write(search_redirect)
        print(f"🔍 Root search redirect created.")

    print("\n✅ ¡Construcción completa!")
    print(f"🌍 Web disponible en: {os.path.abspath(FINAL_HTML_DIR)}")

    # Ensure .nojekyll exists to prevent GitHub Pages from ignoring _static
    nojekyll_path = os.path.join(FINAL_HTML_DIR, ".nojekyll")
    if not os.path.exists(nojekyll_path):
        with open(nojekyll_path, "w") as f:
            pass
        print("✅ Archivo .nojekyll creado para GitHub Pages.")


if __name__ == "__main__":
    main()
