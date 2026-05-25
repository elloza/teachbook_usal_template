import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.collect_used_bibliography import (
    collect_citations_from_markdown,
    collect_used_bibliography,
)


class BibliographyCollectorTests(unittest.TestCase):
    def test_collects_latex_citations_from_raw_latex(self):
        text = """Visible text.

```{raw} html
<p>HTML-only citation {cite:p}`html_only_key`.</p>
```

```{raw} latex
Texto para PDF con \\cite{latex_key_one, latex_key_two}.
```
"""
        uses = collect_citations_from_markdown(text, Path("page.md"))
        self.assertEqual([use.key for use in uses], ["latex_key_one", "latex_key_two"])
        self.assertTrue(all("raw latex" in use.note for use in uses))

    def test_collects_normal_myst_citations_and_skips_code_examples(self):
        text = """Normal citation {cite:p}`normal_key`.

````md
Example citation {cite:p}`example_key`.
````
"""
        uses = collect_citations_from_markdown(text, Path("page.md"))
        self.assertEqual([use.key for use in uses], ["normal_key"])

    def test_used_bib_includes_raw_latex_citation(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            content = root / "content"
            content.mkdir()
            (content / "page.md").write_text(
                """```{raw} latex
Texto impreso con \\cite{latex_key}.
```
""",
                encoding="utf-8",
            )
            bib_file = root / "references.bib"
            bib_file.write_text(
                """@book{latex_key,
  author = {Doe, Jane},
  title = {Raw LaTeX Citations},
  year = {2026}
}
""",
                encoding="utf-8",
            )
            output = root / "used.bib"

            result = collect_used_bibliography(content, bib_file, output)

            self.assertEqual(result.used_keys, ["latex_key"])
            self.assertIn("@book{latex_key", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
