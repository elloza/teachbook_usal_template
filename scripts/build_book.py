import argparse
import io
import subprocess
import sys
import os
import glob
import shutil
import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from importlib import metadata
from pathlib import Path
from tempfile import TemporaryDirectory


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
from build_cache import (
    BUILD_ROOT, CACHE_ROOT, build_lock, file_hash, fingerprint, read_cache_state,
    remove_build_tree, tree_hashes,
)
from pdf_names import DEFAULT_PDF_FILENAME, epub_filename_for_lang, pdf_filename_for_lang
from project_options import PROJECT_ROOT, SLIDEV_CLI, SLIDES_DIR, node_runtime, slides_enabled

VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv


def write_command_log(cmd, stdout, stderr):
    """Persist full build output so quiet mode never hides errors."""
    log_dir = PROJECT_ROOT / ".build_logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
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
    path = PROJECT_ROOT / ".venv" / ("Scripts/jupyter-book.exe" if os.name == "nt" else "bin/jupyter-book")
    if not path.is_file():
        raise SystemExit("ERROR: falta Jupyter Book en .venv. Ejecuta scripts/setup_env.py --yes.")
    return str(path)


def run_jupyter_book_build(cmd, label, attempts=3):
    """Run a Jupyter Book build with retries for transient network-backed extensions.

    Kroki diagrams are rendered through a remote service during the build. In CI or
    first-use setups, a temporary network timeout should not make the whole setup
    look broken, so retry the exact same build before failing for real.
    """
    for attempt in range(1, attempts + 1):
        print(f"🚀 Ejecutando build {label} ({attempt}/{attempts}): {' '.join(cmd)}")
        result = subprocess.run(
            cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        log_path = write_command_log(cmd, result.stdout, result.stderr)
        if VERBOSE:
            print(result.stdout, end="")
            print(result.stderr, end="")
        if result.returncode == 0:
            print(f"   ✅ Build {label} completado. Log completo: {log_path}")
            return

        print(f"❌ Build {label} falló. Log completo: {log_path}")
        if not VERBOSE:
            print_output_tail(result.stdout, result.stderr)
        output = (result.stderr + result.stdout).lower()
        transient = "kroki" in output and any(
            reason in output for reason in ("timed out", "readtimeout", "connection reset", "temporarily unavailable")
        )
        if not transient or attempt == attempts:
            raise subprocess.CalledProcessError(result.returncode, cmd)
        print("⚠️  Fallo temporal de Kroki. Reintentando...")
        time.sleep(10 * attempt)


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

BOOK_DIR = PROJECT_ROOT / "book"
FINAL_HTML_DIR = BUILD_ROOT / "html"
BOOK_CACHE_DIR = CACHE_ROOT / "book"


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


def generate_languages_json(languages, target_dir, with_slides):
    """Generates a JSON file with available languages for the JS switcher."""
    lang_data = []
    for lang in languages:
        code = get_project_default_language() if lang == "default" else lang
        pdf_name = DEFAULT_PDF_FILENAME if lang == "default" else pdf_filename_for_lang(lang)
        downloads = {}
        for filename in (pdf_name, epub_filename_for_lang(lang)):
            if (Path(target_dir) / filename).is_file():
                downloads[Path(filename).suffix[1:]] = filename
        lang_data.append(
            {"code": code, "name": LANG_DISPLAY_NAMES.get(code, code.upper()),
             "slides": with_slides, "downloads": downloads}
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


def fix_language_page_searchindex_refs(language_dir):
    """Point language pages to per-language search and index files.

    Standalone Sphinx builds reference the build-root searchindex.js from pages
    under /<lang>/. After moving /<lang>/ to the final language root, the
    valid searchindex.js, search.html, and genindex.html live in that same
    language root.
    """
    import re

    language_root_files = {
        "searchindex.js": os.path.join(language_dir, "searchindex.js"),
        "search.html": os.path.join(language_dir, "search.html"),
        "genindex.html": os.path.join(language_dir, "genindex.html"),
    }
    if not os.path.isfile(language_root_files["searchindex.js"]):
        print("   ℹ️ searchindex.js not found; skipping search reference fixes")
        return

    fixed_count = 0
    for root, _dirs, files in os.walk(language_dir):
        for filename in files:
            if not filename.endswith(".html"):
                continue

            html_file = os.path.join(root, filename)
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()

            original = content
            html_dir = os.path.dirname(html_file)

            for target_name, target_path in language_root_files.items():
                if not os.path.isfile(target_path):
                    continue

                relative_target = os.path.relpath(target_path, html_dir).replace(
                    "\\", "/"
                )
                escaped_name = re.escape(target_name)

                if target_name == "searchindex.js":
                    content = re.sub(
                        rf'<script src="(?:\.\./)+{escaped_name}"></script>',
                        f'<script src="{relative_target}"></script>',
                        content,
                    )
                else:
                    content = re.sub(
                        rf'(href|action)="(?:\.\./)+{escaped_name}"',
                        rf'\1="{relative_target}"',
                        content,
                    )

            if content != original:
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(content)
                fixed_count += 1

    print(f"   🔧 Fixed language-local search references in {fixed_count} pages")


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


def sphinx_environment_key():
    packages = sorted(f"{dist.name}=={dist.version}" for dist in metadata.distributions())
    return fingerprint([sys.version, packages, file_hash(Path(__file__))])


def build_sphinx_language(lang, static_key, environment_key, clean):
    """Keep Sphinx's source directory and doctrees stable between text edits."""
    work_dir = BOOK_CACHE_DIR / f"lang-{lang}"
    html_dir = work_dir / "_build" / "html"
    if lang == "default":
        # Legacy books have their sources directly in book/. Keep this path supported.
        remove_build_tree(work_dir)
        validate_bibliography_for_language(lang, BOOK_DIR, BOOK_DIR / "_static" / "references.bib")
        run_jupyter_book_build(
            [get_jupyter_book(), "build", str(BOOK_DIR), "--path-output", str(work_dir), "--all"],
            "DEFAULT",
        )
        return html_dir

    source = BOOK_DIR / lang
    config = BOOK_DIR / f"_config_{lang}.yml"
    toc = BOOK_DIR / f"_toc_{lang}.yml"
    if not source.is_dir() or source.resolve().parent != BOOK_DIR.resolve() or not toc.is_file():
        raise ValueError(f"Falta la carpeta o la tabla de contenidos del idioma {lang}.")
    ignored_dirs = {".ipynb_checkpoints", "__pycache__"}
    files = tree_hashes(source, ignored_dirs=ignored_dirs)
    inputs = fingerprint([environment_key, static_key, file_hash(config), file_hash(toc)])
    state = {"inputs": inputs, "files": files}
    stamp = work_dir / ".teachbook-cache.json"
    old_state = read_cache_state(stamp)
    cache_valid = (
        not clean
        and isinstance(old_state, dict)
        and old_state.get("inputs") == inputs
        and isinstance(old_state.get("files"), dict)
        and (html_dir / "searchindex.js").is_file()
        and (work_dir / "_build" / ".doctrees" / "environment.pickle").is_file()
    )
    if cache_valid and old_state == state:
        print(f"♻️  Libro {lang}: reutilizando HTML.")
        return html_dir

    stamp.unlink(missing_ok=True)
    changed = []
    if cache_valid and old_state["files"].keys() == files.keys():
        changed = [name for name in files if files[name] != old_state["files"][name]]
    incremental = bool(changed) and all(
        Path(name).suffix.lower() in {".md", ".ipynb", ".rst"} for name in changed
    )
    if incremental:
        for name in changed:
            # A fresh mtime also lets Sphinx detect files restored from an older revision.
            shutil.copyfile(source / name, work_dir / lang / name)
    else:
        remove_build_tree(work_dir)
        shutil.copytree(source, work_dir / lang, ignore=shutil.ignore_patterns(*ignored_dirs))
        shutil.copytree(
            BOOK_DIR / "_static", work_dir / "_static",
            ignore=shutil.ignore_patterns("languages.json"),
        )
        shutil.copy2(config, work_dir / "_config.yml")
        shutil.copy2(toc, work_dir / "_toc.yml")
        sanitize_config(work_dir / "_config.yml")

    validate_bibliography_for_language(lang, source, BOOK_DIR / "_static" / "references.bib")
    cmd = [get_jupyter_book(), "build", str(work_dir)]
    if not incremental:
        cmd.append("--all")
    label = f"{lang} incremental ({len(changed)} archivo(s))" if incremental else f"{lang} completo"
    run_jupyter_book_build(cmd, label)
    if not (html_dir / "searchindex.js").is_file():
        raise ValueError(f"Jupyter Book no generó el índice de búsqueda de {lang}.")
    stamp.write_text(json.dumps(state), encoding="utf-8")
    return html_dir


def assemble_language(lang, html_dir, site_dir):
    if lang == "default":
        shutil.copytree(html_dir, site_dir, dirs_exist_ok=True)
        return

    # Keep the public URL scheme used by the book and GitHub Pages.
    final_dest = site_dir / lang
    pages = html_dir / lang
    shutil.copytree(pages if pages.is_dir() else html_dir, final_dest)
    fix_pdf_paths(final_dest, pdf_filename_for_lang(lang))
    for page in final_dest.rglob("*.html"):
        fix_duplicate_thebe_scripts(page)

    for name in ("search.html", "genindex.html", "searchindex.js"):
        source = html_dir / name
        if source.is_file():
            dest = final_dest / name
            shutil.copy2(source, dest)
            if name.endswith(".html"):
                fix_html_asset_paths(dest)
            else:
                fix_searchindex_paths(dest, lang)
    fix_language_page_searchindex_refs(final_dest)

    # Sphinx places these at the build root, shared by the published languages.
    for name in ("_static", "_images", "_downloads"):
        source = html_dir / name
        if source.is_dir():
            shutil.copytree(source, site_dir / name, dirs_exist_ok=True)


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


def create_redirect_index(site_dir, default_lang="es"):
    """Creates a root index.html that redirects to the default language."""
    redirect_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="icon" href="_static/favicon.ico" />
        <meta http-equiv="refresh" content="0; url={default_lang}/intro.html" />
        <script>window.location.href = "{default_lang}/intro.html";</script>
    </head>
    <body>
        <p>Redirecting to <a href="{default_lang}/intro.html">{default_lang} version</a>...</p>
    </body>
    </html>
    """
    with open(site_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(redirect_html)
    print(f"🔀 Redirección raíz creada apuntando a: /{default_lang}/")


def build_site(site_dir, *, clean, with_slides, with_epub, environment_key):
    print("📚 Iniciando proceso de construcción multi-idioma...")
    languages = get_languages()
    if not languages:
        raise ValueError("No se encontraron configuraciones en book/.")
    print(f"🔍 Idiomas detectados: {languages}")

    custom_static = BOOK_DIR / "_static"
    static_key = fingerprint(tree_hashes(custom_static, ignored_files={"languages.json"}))
    with ThreadPoolExecutor(max_workers=min(2, len(languages))) as executor:
        builds = {
            lang: executor.submit(build_sphinx_language, lang, static_key, environment_key, clean)
            for lang in languages
        }

    for lang in languages:
        assemble_language(lang, builds[lang].result(), site_dir)

    final_static = site_dir / "_static"
    if custom_static.is_dir():
        shutil.copytree(custom_static, final_static, dirs_exist_ok=True)
    if with_epub:
        from export_epub import export_books

        export_books(site_dir, BOOK_DIR, languages)
    generate_languages_json(languages, final_static, with_slides)

    # Preserve the language manifest for pages whose Sphinx root is language-local.
    for lang in languages:
        lang_static = site_dir / lang / "_static"
        if lang_static.is_dir():
            shutil.copy2(final_static / "languages.json", lang_static)

    if "default" not in languages:
        default_lang = get_project_default_language()
        if default_lang not in languages:
            default_lang = languages[0]
        create_redirect_index(site_dir, default_lang)

        # Create root search.html that redirects to default language search
        # CRITICAL: preserve query string (?q=...) so search terms survive the redirect
        search_redirect = f"""<!DOCTYPE html>
<html>
<head>
    <link rel="icon" href="_static/favicon.ico" />
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
        (site_dir / "search.html").write_text(search_redirect, encoding="utf-8")
        print(f"🔍 Root search redirect created.")

    (site_dir / ".nojekyll").touch()

    if with_slides:
        from build_slides import build_site_slides, parse_jobs

        print("\n🎞️  Construyendo diapositivas Slidev...")
        build_site_slides(
            site_dir, os.environ.get("TEACHBOOK_SITE_BASE", "/"),
            jobs=parse_jobs(os.environ.get("TEACHBOOK_SLIDEV_JOBS")), clean=clean,
        )
    else:
        (final_static / "slides_manifest.json").unlink(missing_ok=True)
        print("Slidev desactivado en teachbook.json.")


def publish_site(site_dir, backup):
    remove_build_tree(backup)
    if FINAL_HTML_DIR.exists():
        if FINAL_HTML_DIR.is_symlink() or FINAL_HTML_DIR.is_junction():
            raise ValueError(f"La salida de compilación no puede ser un enlace: {FINAL_HTML_DIR}")
        FINAL_HTML_DIR.replace(backup)
    try:
        site_dir.replace(FINAL_HTML_DIR)
    except OSError:
        if backup.exists():
            backup.replace(FINAL_HTML_DIR)
        raise


def site_input_key(environment_key, with_slides, with_epub):
    scripts = ["build_cache.py", "collect_used_bibliography.py", "pdf_names.py", "project_options.py"]
    inputs = [
        environment_key,
        tree_hashes(
            BOOK_DIR, ignored_dirs={"_build", "__pycache__", ".ipynb_checkpoints"},
            ignored_files={"languages.json"},
        ),
        with_slides,
        with_epub,
    ]
    if with_slides:
        from build_slides import IGNORED_SLIDE_DIRS, normalize_site_base

        scripts.append("build_slides.py")
        inputs.extend((
            normalize_site_base(os.environ.get("TEACHBOOK_SITE_BASE")),
            node_runtime(),
            file_hash(SLIDEV_CLI) if SLIDEV_CLI.is_file() else None,
            tree_hashes(SLIDES_DIR, ignored_dirs=IGNORED_SLIDE_DIRS),
        ))
    if with_epub:
        from export_epub import find_pandoc

        scripts.append("export_epub.py")
        pandoc = Path(find_pandoc())
        info = pandoc.stat()
        inputs.extend((str(pandoc), info.st_size, info.st_mtime_ns, os.environ.get("TEACHBOOK_SITE_URL")))
    return fingerprint([inputs, [file_hash(Path(__file__).with_name(name)) for name in scripts]])


def site_output_stamp(site_dir):
    """Detect deleted or edited output without reading all its assets again."""
    if site_dir.is_symlink() or site_dir.is_junction() or not (site_dir / "index.html").is_file():
        return None
    files = {}
    for folder, _, names in os.walk(site_dir):
        for name in names:
            file = Path(folder) / name
            info = file.lstat()
            files[file.relative_to(site_dir).as_posix()] = (info.st_size, info.st_mtime_ns, info.st_mode)
    return fingerprint(files)


def main():
    parser = argparse.ArgumentParser(description="Compila el sitio del TeachBook.")
    parser.add_argument("--clean", action="store_true", help="Reconstruir el libro y Slidev desde cero.")
    parser.add_argument("--epub", action="store_true", help="Generar EPUB de cada idioma junto al sitio.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar los registros de Jupyter Book.")
    args = parser.parse_args()
    with_slides = slides_enabled()
    started = time.perf_counter()

    try:
        with build_lock():
            backup = BUILD_ROOT / ".html-previous"
            if backup.is_dir() and not FINAL_HTML_DIR.exists():
                backup.replace(FINAL_HTML_DIR)
            environment_key = sphinx_environment_key()
            inputs = site_input_key(environment_key, with_slides, args.epub)
            stamp = BUILD_ROOT / ".teachbook-site.json"
            previous = read_cache_state(stamp)
            if (
                not args.clean and isinstance(previous, dict) and previous.get("inputs") == inputs
                and previous.get("output") and previous["output"] == site_output_stamp(FINAL_HTML_DIR)
            ):
                print(f"♻️ Sitio sin cambios. Reutilizado en {time.perf_counter() - started:.2f}s.")
                print(f"🌍 Web disponible en: {FINAL_HTML_DIR}")
                return
            with TemporaryDirectory(prefix=".site-", dir=BUILD_ROOT, ignore_cleanup_errors=True) as stage:
                site = Path(stage) / "html"
                site.mkdir()
                build_site(
                    site, clean=args.clean, with_slides=with_slides,
                    with_epub=args.epub, environment_key=environment_key,
                )
                if not (site / "index.html").is_file():
                    raise ValueError("La compilación no generó index.html.")
                publish_site(site, backup)
            remove_build_tree(backup)
            try:
                state = {"inputs": inputs, "output": site_output_stamp(FINAL_HTML_DIR)}
                stamp.write_text(json.dumps(state), encoding="utf-8")
            except OSError as exc:
                print(f"⚠️ No se pudo guardar la caché del sitio: {exc}")
    except (BibliographyError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"ERROR: compilación incompleta. {exc}") from exc

    print(f"\n✅ ¡Construcción completa en {time.perf_counter() - started:.2f}s!")
    print(f"🌍 Web disponible en: {FINAL_HTML_DIR}")


if __name__ == "__main__":
    main()
