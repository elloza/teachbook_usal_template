import io
import os
import sys
import argparse
import subprocess
import shutil

# Fix: Windows cp1252 can't encode emojis — force UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_DIR = os.path.join(PROJECT_ROOT, ".venv")

AUTO_HEADER = "<!-- Convertido automáticamente desde PDF. Revisar y corregir formato si es necesario. -->\n\n"


def get_venv_python():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")


def get_venv_pip():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    return os.path.join(VENV_DIR, "bin", "pip")


def ensure_dependency():
    try:
        import pymupdf4llm

        return True
    except ImportError:
        pass

    print("📦 pymupdf4llm no encontrado. Instalando...")

    pip_cmd = get_venv_pip()
    python_cmd = get_venv_python()

    if not os.path.exists(pip_cmd):
        print(f"❌ No se encontró el entorno virtual en '{VENV_DIR}'.")
        print("   Ejecuta primero: python scripts/setup_env.py")
        sys.exit(1)

    use_uv = shutil.which("uv") is not None

    try:
        if use_uv:
            subprocess.check_call(
                ["uv", "pip", "install", "--python", python_cmd, "pymupdf4llm"],
                cwd=PROJECT_ROOT,
            )
        else:
            subprocess.check_call(
                [python_cmd, "-m", "pip", "install", "pymupdf4llm"],
                cwd=PROJECT_ROOT,
            )
        print("✅ pymupdf4llm instalado correctamente.")
    except subprocess.CalledProcessError:
        print("❌ Error instalando pymupdf4llm.")
        print("   Instálalo manualmente: pip install pymupdf4llm")
        sys.exit(1)

    return True


def collect_pdfs(input_path):
    input_path = os.path.abspath(input_path)

    if not os.path.exists(input_path):
        print(f"❌ No existe: {input_path}")
        sys.exit(1)

    if os.path.isfile(input_path):
        if not input_path.lower().endswith(".pdf"):
            print(f"❌ El archivo no es un PDF: {input_path}")
            sys.exit(1)
        return [input_path]

    if os.path.isdir(input_path):
        pdfs = []
        for root, _dirs, files in os.walk(input_path):
            for f in sorted(files):
                if f.lower().endswith(".pdf"):
                    pdfs.append(os.path.join(root, f))
        if not pdfs:
            print(f"⚠️ No se encontraron PDFs en: {input_path}")
            sys.exit(0)
        return pdfs

    print(f"❌ Ruta no válida: {input_path}")
    sys.exit(1)


def resolve_output_dir(pdf_path, output_arg):
    if output_arg:
        out = os.path.abspath(output_arg)
    else:
        out = os.path.dirname(pdf_path)
    os.makedirs(out, exist_ok=True)
    return out


def convert_pdf(pdf_path, output_dir, extract_images):
    import pymupdf4llm
    import pymupdf

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    md_path = os.path.join(output_dir, f"{pdf_name}.md")

    print(f"📄 Convirtiendo: {os.path.basename(pdf_path)}", end="", flush=True)

    try:
        if extract_images:
            images_dir = os.path.join(output_dir, f"{pdf_name}_images")
            os.makedirs(images_dir, exist_ok=True)

            doc = pymupdf.open(pdf_path)
            image_refs = {}

            for page_num in range(len(doc)):
                page = doc[page_num]
                images = page.get_images(full=True)

                for img_idx, img_info in enumerate(images):
                    xref = img_info[0]
                    try:
                        base_image = doc.extract_image(xref)
                        if not base_image:
                            continue
                    except Exception:
                        continue

                    img_bytes = base_image["image"]
                    img_ext = base_image.get("ext", "png")
                    img_filename = f"page{page_num + 1}_img{img_idx + 1}.{img_ext}"
                    img_path = os.path.join(images_dir, img_filename)

                    with open(img_path, "wb") as f:
                        f.write(img_bytes)

                    image_refs.setdefault(page_num, []).append(
                        {
                            "filename": img_filename,
                            "dir_name": f"{pdf_name}_images",
                        }
                    )

            doc.close()

            md_text = pymupdf4llm.to_markdown(pdf_path, page_chunks=False)

            if image_refs:
                image_blocks = []
                seen = set()
                for _page_num in sorted(image_refs.keys()):
                    for img in image_refs[_page_num]:
                        if img["filename"] not in seen:
                            seen.add(img["filename"])
                            rel_path = f"{img['dir_name']}/{img['filename']}"
                            image_blocks.append(
                                f"\n```{{image}} {rel_path}\n"
                                f":alt: Imagen extraída del PDF\n"
                                f":width: 80%\n"
                                f":align: center\n"
                                f"```\n"
                            )
                if image_blocks:
                    md_text += "\n\n---\n\n## Imágenes extraídas\n\n" + "\n".join(
                        image_blocks
                    )
        else:
            md_text = pymupdf4llm.to_markdown(pdf_path, page_chunks=False)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(AUTO_HEADER)
            f.write(md_text)

        print(f" → ✅ {md_path}")
        return True

    except Exception as e:
        print(f" → ❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Convierte archivos PDF a Markdown para TeachBook",
    )
    parser.add_argument(
        "input",
        help="Archivo PDF o directorio con PDFs (búsqueda recursiva)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Directorio de salida (por defecto: mismo directorio que el PDF)",
    )
    parser.add_argument(
        "--images",
        action="store_true",
        help="Extraer imágenes del PDF y referenciarlas con directivas MyST",
    )
    args = parser.parse_args()

    print("📄 TeachBook — PDF a Markdown")
    print("============================")

    ensure_dependency()

    pdfs = collect_pdfs(args.input)
    print(f"🔍 Encontrados {len(pdfs)} archivo(s) PDF\n")

    if len(pdfs) > 1 and args.output:
        out_dir = os.path.abspath(args.output)
        os.makedirs(out_dir, exist_ok=True)
    else:
        out_dir = None

    success = 0
    for pdf_path in pdfs:
        target = out_dir if (out_dir and len(pdfs) > 1) else args.output
        output = resolve_output_dir(pdf_path, target)
        if convert_pdf(pdf_path, output, args.images):
            success += 1

    total = len(pdfs)
    print(
        f"\n{'✅' if success == total else '⚠️'} {success}/{total} archivo(s) convertidos."
    )

    if success < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
