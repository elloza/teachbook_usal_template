"""Regression tests for feature flags and cached output assembly."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import build_book
import build_cache
import build_slides
import preview_book
import project_options


class BuildModesTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def test_slides_opt_in_and_validation(self):
        config = self.root / "teachbook.json"
        with patch.object(project_options, "PROJECT_OPTIONS", config):
            self.assertFalse(project_options.slides_enabled())
            config.write_text('{"slides": true}', encoding="utf-8")
            self.assertTrue(project_options.slides_enabled())
            config.write_text('{"slides": false}', encoding="utf-8")
            self.assertFalse(project_options.slides_enabled())
            config.write_text('{"slides": "false"}', encoding="utf-8")
            with self.assertRaises(SystemExit):
                project_options.slides_enabled()

    def test_failed_publish_restores_previous_site(self):
        public = self.root / "html"
        public.mkdir()
        (public / "index.html").write_text("last successful build", encoding="utf-8")
        with (
            patch.object(build_book, "FINAL_HTML_DIR", public),
            patch.object(build_cache, "BUILD_ROOT", self.root),
            self.assertRaises(OSError),
        ):
            build_book.publish_site(self.root / "missing", self.root / "previous")
        self.assertEqual((public / "index.html").read_text(encoding="utf-8"), "last successful build")

    def test_slide_cache_uses_deck_inputs_shared_assets_and_public_base(self):
        slides = self.root / "slides"
        cli = slides / "node_modules" / "slidev.mjs"
        cli.parent.mkdir(parents=True)
        cli.touch()
        style = slides / "style.css"
        style.write_text("/* shared */", encoding="utf-8")
        decks = []
        for name in ("a", "b"):
            source = slides / "es" / name / "slides.md"
            source.parent.mkdir(parents=True)
            source.write_text(f"# Deck {name}", encoding="utf-8")
            decks.append(build_slides.Deck("es", name, f"es/{name}", source, f"slides/es/{name}/index.html", name))

        def fake_compile(deck, base, output, node):
            (output / "assets").mkdir(parents=True)
            (output / "index.html").write_text(base + deck.source.read_text(encoding="utf-8"), encoding="utf-8")

        with (
            patch.object(build_slides, "SLIDES_DIR", slides),
            patch.object(build_slides, "SLIDEV_CLI", cli),
            patch.object(build_slides, "SLIDE_CACHE_DIR", self.root / "cache"),
            patch.object(build_cache, "BUILD_ROOT", self.root),
            patch.object(build_slides, "node_runtime", return_value=("node", "v22.18.0")),
            patch.object(build_slides, "build_deck", side_effect=fake_compile) as compile_deck,
        ):
            build_slides.build_decks(decks, "/", self.root / "first", jobs=1, clean=False)
            self.assertEqual(compile_deck.call_count, 2)
            build_slides.build_decks(decks, "/", self.root / "warm", jobs=1, clean=False)
            self.assertEqual(compile_deck.call_count, 2)
            decks[0].source.write_text("# New title", encoding="utf-8")
            build_slides.build_decks(decks, "/", self.root / "edited", jobs=1, clean=False)
            self.assertEqual(compile_deck.call_count, 3)
            self.assertEqual(compile_deck.call_args.args[0], decks[0])
            style.write_text("/* shared edit */", encoding="utf-8")
            build_slides.build_decks(decks, "/", self.root / "style-edit", jobs=1, clean=False)
            self.assertEqual(compile_deck.call_count, 5)
            build_slides.build_decks(decks, "/repo/", self.root / "pages", jobs=1, clean=False)
            self.assertEqual(compile_deck.call_count, 7)
            self.assertTrue(
                (self.root / "pages/slides/es/a/index.html").read_text(encoding="utf-8").startswith("/repo/")
            )

    def test_preview_prunes_build_and_dependency_directories(self):
        book = self.root / "book"
        slides = self.root / "slides"
        sources = [book / "intro.md", book / "_build" / "index.html", slides / "slides.md", slides / "node_modules" / "node.js"]
        for source in sources:
            source.parent.mkdir(parents=True, exist_ok=True)
            source.touch()
        with (
            patch.object(preview_book, "PROJECT_OPTIONS", self.root / "teachbook.json"),
            patch.object(preview_book, "BOOK_DIR", book),
            patch.object(preview_book, "SLIDES_DIR", slides),
            patch.object(preview_book, "slides_enabled", return_value=True) as slides_enabled,
        ):
            self.assertEqual(set(preview_book.snapshot_sources()), {sources[0], sources[2]})
            slides_enabled.return_value = False
            self.assertEqual(set(preview_book.snapshot_sources()), {sources[0]})


if __name__ == "__main__":
    unittest.main()
