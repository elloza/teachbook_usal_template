import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts import check_encoding


class CheckEncodingTests(unittest.TestCase):
    def make_temp_file(self, name: str, data: bytes) -> Path:
        root = check_encoding.PROJECT_ROOT / ".build_logs"
        root.mkdir(exist_ok=True)
        directory = TemporaryDirectory(dir=root)
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / name
        path.write_bytes(data)
        return path

    def test_detects_invalid_utf8(self):
        path = self.make_temp_file("broken.md", b"\xff")
        issues = check_encoding.scan_file(path)
        self.assertEqual(len(issues), 1)
        self.assertIn("no es UTF-8", issues[0].reason)

    def test_detects_common_mojibake(self):
        path = self.make_temp_file("mojibake.md", ("T" + "\u00c3\u00adtulo").encode("utf-8"))
        issues = check_encoding.scan_file(path)
        self.assertTrue(any("mojibake" in issue.reason for issue in issues))

    def test_detects_non_ascii_notebook_code_cells(self):
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["print('á')\n"],
                }
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        path = self.make_temp_file("notebook.ipynb", json.dumps(notebook).encode("utf-8"))
        issues = check_encoding.scan_file(path)
        self.assertTrue(any("texto no ASCII" in issue.reason for issue in issues))

    def test_text_file_detection_covers_project_formats(self):
        for name in ("CITATION.cff", "diagram.plantuml", "script.sh", "LICENSE"):
            with self.subTest(name=name):
                self.assertTrue(check_encoding.is_text_path(Path(name)))


if __name__ == "__main__":
    unittest.main()
