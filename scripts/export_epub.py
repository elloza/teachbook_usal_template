"""Export the published TeachBook pages as reflowable EPUB 3 with Pandoc."""

import os
import posixpath
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from importlib.util import find_spec
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from urllib.parse import quote, unquote, urljoin, urlsplit
from xml.etree import ElementTree
from zipfile import ZipFile

import yaml

from pdf_names import epub_filename_for_lang


def find_pandoc():
    package = find_spec("pypandoc")
    if package and package.origin:
        bundled = Path(package.origin).parent / "files" / ("pandoc.exe" if os.name == "nt" else "pandoc")
        if bundled.is_file():
            return str(bundled)

    pandoc = shutil.which("pandoc")
    if pandoc:
        result = subprocess.run([pandoc, "--version"], check=True, capture_output=True, text=True, encoding="utf-8")
        match = re.match(r"pandoc(?:\.exe)? (\d+)\.(\d+)", result.stdout)
        if match and tuple(map(int, match.groups())) >= (3, 2):
            return pandoc
    raise ValueError(
        "EPUB requiere Pandoc 3.2 o posterior. Ejecuta scripts/setup_env.py --yes --extras epub. "
        "En Windows ARM64, instala Pandoc x64 desde https://pandoc.org/installing.html y añádelo al PATH."
    )


def toc_pages(toc):
    """Yield the root and the visible chapters in reading order."""
    def walk(entries, depth):
        for entry in entries or []:
            if entry.get("publish") is False:
                continue
            if "file" in entry:
                yield entry["file"], depth
            yield from walk(entry.get("sections"), depth + 1)

    yield toc["root"], 0
    for part in toc.get("parts", []):
        if part.get("publish") is not False:
            yield from walk(part.get("chapters"), 0)
    yield from walk(toc.get("chapters") or toc.get("sections"), 0)


def local_path(page, path):
    if not path:
        return page
    path = unquote(path).replace("\\", "/")
    if path.startswith("/") or ":" in path.split("/", 1)[0]:
        return None
    result = posixpath.normpath(posixpath.join(posixpath.dirname(page), path))
    if result == ".." or result.startswith("../"):
        return None
    return result


@dataclass
class Chapter:
    path: str
    article: object
    start: str
    anchors: dict[str, str]


def read_chapters(site_dir, toc):
    from bs4 import BeautifulSoup, SoupStrainer

    chapters = {}
    for index, (doc, depth) in enumerate(toc_pages(toc), start=1):
        path = PurePosixPath(doc)
        if path.suffix in {".md", ".rst", ".ipynb"}:
            path = path.with_suffix("")
        page = local_path("", f"{path}.html")
        if not page or page in chapters:
            raise ValueError(f"Ruta de capítulo inválida o repetida para EPUB: {doc}")
        soup = BeautifulSoup(
            (site_dir / page).read_text(encoding="utf-8"), "html.parser",
            parse_only=SoupStrainer("article", class_="bd-article"),
        )
        article = soup.find("article")
        heading = article.find("h1") if article else None
        if not heading:
            raise ValueError(f"No se encontró el título del capítulo EPUB en {page}.")

        # Put the section anchors on headings so Pandoc can split the book into chapters.
        for section in article.find_all("section"):
            title = section.find(re.compile(r"^h[1-6]$"), recursive=False)
            if section.get("id") and title and not title.get("id"):
                title["id"] = section["id"]
            elif section.get("id"):
                anchor = soup.new_tag("span", id=section["id"])
                section.insert_before(anchor)
            section.unwrap()

        start = f"cap-{index}"
        anchors = {}
        for number, tag in enumerate(article.find_all(id=True), start=1):
            identifier = start if tag is heading else f"{start}-{number}"
            anchors.setdefault(tag["id"], identifier)
            tag["id"] = identifier
        heading["id"] = start
        for title in article.find_all(re.compile(r"^h[1-6]$")):
            title.name = f"h{min(6, int(title.name[1]) + depth)}"
        chapters[page] = Chapter(page, article, start, anchors)
    return chapters


def epub_svg(path, site_dir, media_dir, language):
    """Use the pre-rendered PNG for diagrams that contain HTML labels."""
    source = site_dir / path
    data = source.read_bytes()
    if b"foreignObject" in data:
        png = source.with_suffix(".png").name
        fallback = site_dir / "_static" / "generated" / "diagrams_pdf" / language / png
        if not fallback.is_file():
            raise ValueError(f"Falta la variante PNG para el SVG con etiquetas HTML: {path}")
        return fallback.relative_to(site_dir).as_posix()

    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError as exc:
        raise ValueError(f"SVG no válido para EPUB: {path}. {exc}") from exc
    ids = {element.get("id") for element in root.iter() if element.get("id")}
    replacements = {}
    for index, identifier in enumerate(sorted(ids), start=1):
        if not re.fullmatch(r"[^\W\d][\w.-]*", identifier):
            new_id = f"diagram-id-{index}"
            while new_id in ids:
                new_id += "-"
            replacements[identifier] = new_id
    if not replacements:
        return path

    # EPUB requires XML IDs. Some diagram generators emit IDs with spaces or digits first.
    def replace_url(match):
        return f"url(#{replacements.get(match[1], match[1])})"

    for element in root.iter():
        if element.get("id") in replacements:
            element.set("id", replacements[element.get("id")])
        for key, value in element.attrib.items():
            if key.rsplit("}", 1)[-1] == "href" and value.startswith("#"):
                value = "#" + replacements.get(value[1:], value[1:])
            element.set(key, re.sub(r"url\(#([^)]+)\)", replace_url, value))
        if element.text and element.tag.endswith("}style"):
            element.text = re.sub(r"url\(#([^)]+)\)", replace_url, element.text)

    target = media_dir / path
    target.parent.mkdir(parents=True, exist_ok=True)
    ElementTree.register_namespace("", "http://www.w3.org/2000/svg")
    ElementTree.ElementTree(root).write(target, encoding="utf-8")
    return target.relative_to(media_dir.parent).as_posix()


def prepare_chapter(chapter, chapters, site_dir, media_dir, site_url, language):
    article = chapter.article
    interactive = article.select_one("script, iframe, canvas, audio, video, object, embed") is not None
    for tag in article.select(
        "script, style, iframe, canvas, audio, video, object, embed, input, button, select, textarea, svg, .headerlink"
    ):
        tag.decompose()
    for entry in article.select('[role="doc-biblioentry"]'):
        del entry["role"]
    for summary in article.find_all("summary"):
        summary.name = "p"
    for details in article.find_all("details"):
        details.unwrap()

    for image in article.find_all("img"):
        url = urlsplit(image.get("src", ""))
        path = local_path(chapter.path, url.path) if url.path and not (url.scheme or url.netloc) else None
        if not path or not (site_dir / path).is_file():
            image.replace_with(image.get("alt", ""))
            continue
        if PurePosixPath(path).suffix.lower() == ".svg":
            path = epub_svg(path, site_dir, media_dir, language)
        image.attrs = {"src": quote(path), "alt": image.get("alt", "")}
    for picture in article.find_all("picture"):
        for source in picture.find_all("source"):
            source.decompose()
        picture.unwrap()

    for link in article.find_all("a", href=True):
        url = urlsplit(link["href"])
        if url.scheme in {"http", "https", "mailto"}:
            continue
        if url.netloc and not url.scheme:
            link["href"] = "https:" + link["href"]
            continue
        target = local_path(chapter.path, url.path) if not url.scheme else None
        if target in chapters:
            destination = chapters[target]
            link["href"] = "#" + destination.anchors.get(unquote(url.fragment), destination.start)
        elif target and site_url and not link.find("img") and (site_dir / target).is_file():
            link["href"] = urljoin(site_url, quote(target))
        else:
            link.unwrap()

    html = article.decode_contents()
    if interactive and site_url:
        label = "Actividades y multimedia en la web" if language == "es" else "Activities and media on the web"
        html += f'<p><a href="{urljoin(site_url, quote(chapter.path))}">{label}</a></p>'
    return html


def export_books(site_dir, book_dir, languages):
    pandoc = find_pandoc()
    for lang in languages:
        started = time.perf_counter()
        suffix = "" if lang == "default" else f"_{lang}"
        toc = yaml.safe_load((book_dir / f"_toc{suffix}.yml").read_text(encoding="utf-8"))
        config = yaml.safe_load((book_dir / f"_config{suffix}.yml").read_text(encoding="utf-8"))
        language = config.get("language", "es") if lang == "default" else lang
        title = " ".join(config["title"].split())
        site_url = os.environ.get("TEACHBOOK_SITE_URL") or config.get("html", {}).get("baseurl", "")
        if site_url:
            site_url = site_url.rstrip("/") + "/"
            parsed = urlsplit(site_url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError("TEACHBOOK_SITE_URL debe ser una URL web absoluta.")
        chapters = read_chapters(site_dir, toc)
        output = site_dir / "_static" / epub_filename_for_lang(lang)
        with TemporaryDirectory(prefix=".epub-", dir=site_dir.parent) as temp:
            media_dir = Path(temp) / "media"
            html = "\n".join(
                prepare_chapter(chapter, chapters, site_dir, media_dir, site_url, language)
                for chapter in chapters.values()
            )
            subprocess.run(
                [pandoc, "--from=html+tex_math_single_backslash", "--to=epub3", "--mathml",
                 "--toc", "--toc-depth=2", "--split-level=1", "--fail-if-warnings",
                 "--resource-path", os.pathsep.join((str(site_dir), temp)),
                 "-M", f"title={title}", "-M", f"lang={language}",
                 "-M", f"author={config.get('author', '')}", "--output", str(output)],
                input=html, encoding="utf-8", cwd=site_dir, check=True,
            )
        with ZipFile(output) as ebook:
            if ebook.read("mimetype") != b"application/epub+zip" or "META-INF/container.xml" not in ebook.namelist():
                raise ValueError(f"Pandoc no generó un EPUB válido para {lang}.")
        print(f"📖 EPUB {lang}: {len(chapters)} páginas fuente, {output.stat().st_size / 1024**2:.1f} MiB, "
              f"{time.perf_counter() - started:.2f}s.")
