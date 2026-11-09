"""Regression test for links and reading order in the offline book."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from export_epub import prepare_chapter, read_chapters


class ExportEpubTest(unittest.TestCase):
    def test_chapters_keep_their_cross_references_and_visible_order(self):
        site = Path(self.enterContext(tempfile.TemporaryDirectory()))
        (site / "es").mkdir()
        (site / "es/intro.html").write_text(
            '<article class="bd-article"><section id="introduccion"><h1>Introducción</h1>'
            '<a href="tema.html#detalle">Detalle</a><a href="borrador.html">Borrador</a>'
            '<script>runWidget()</script></section></article>',
            encoding="utf-8",
        )
        (site / "es/tema.html").write_text(
            '<article class="bd-article"><section id="tema"><h1>Tema</h1>'
            '<section id="detalle"><h2>Detalle</h2></section></section></article>',
            encoding="utf-8",
        )
        toc = {
            "root": "es/intro",
            "chapters": [
                {"file": "es/borrador", "publish": False},
                {"file": "es/tema"},
            ],
        }
        chapters = read_chapters(site, toc)
        self.assertEqual(list(chapters), ["es/intro.html", "es/tema.html"])
        target = chapters["es/tema.html"].anchors["detalle"]
        html = prepare_chapter(chapters["es/intro.html"], chapters, site, site / "media", "https://book.test/", "es")
        self.assertIn(f'href="#{target}"', html)
        self.assertNotIn("borrador.html", html)
        self.assertNotIn("runWidget", html)
        self.assertIn('href="https://book.test/es/intro.html"', html)


if __name__ == "__main__":
    unittest.main()
