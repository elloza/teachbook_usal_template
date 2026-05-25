import json
import unittest
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1] / "book"


class SchemDrawNotebookTests(unittest.TestCase):
    def test_schemdraw_cells_render_once(self):
        notebooks = [
            path
            for path in BOOK_ROOT.rglob("*.ipynb")
            if "schemdraw" in path.read_text(encoding="utf-8")
        ]
        self.assertGreater(len(notebooks), 0)

        for path in notebooks:
            with self.subTest(path=path.relative_to(BOOK_ROOT)):
                notebook = json.loads(path.read_text(encoding="utf-8"))
                for cell in notebook.get("cells", []):
                    if cell.get("cell_type") != "code":
                        continue
                    source = cell.get("source", "")
                    source_text = "".join(source) if isinstance(source, list) else str(source)
                    if "schemdraw.Drawing()" not in source_text:
                        continue
                    self.assertNotIn(
                        "d.draw()",
                        source_text,
                        "Use the drawing context manager output only; d.draw() creates a second image.",
                    )
                    self.assertLessEqual(
                        len(cell.get("outputs", [])),
                        1,
                        "SchemDraw notebook cells should store only one rendered diagram.",
                    )


if __name__ == "__main__":
    unittest.main()
