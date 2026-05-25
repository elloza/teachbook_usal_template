(citations_bibliography)=
# Citations and Bibliography

This template includes `sphinxcontrib-bibtex`, which manages bibliographic references using BibTeX files.

## Bibliography file

Bibliography entries are stored in `book/_static/references.bib`. Each entry follows this format:

```bibtex
@book{einstein1920,
  author    = {Albert Einstein},
  title     = {Relativity: The Special and General Theory},
  year      = {1920},
  publisher = {Henry Holt and Company}
}

@article{dirac1930,
  author  = {Paul A. M. Dirac},
  title   = {A Theory of Electrons and Protons},
  journal = {Proceedings of the Royal Society A},
  year    = {1930},
  volume  = {126},
  pages   = {360--365}
}
```

## Textual citation: `{cite:t}`

Inserts the author name followed by the year:

```md
{cite:t}`einstein1920` formulated the theory of relativity.
```

Result: {cite:t}`einstein1920` formulated the theory of relativity.

## Parenthetical citation: `{cite:p}`

Inserts author and year in parentheses:

```md
Quantum mechanics revolutionized physics {cite:p}`dirac1930`.
```

Result: Quantum mechanics revolutionized physics {cite:p}`dirac1930`.

## Multiple citations

Separate multiple keys with commas:

```md
Several authors contributed {cite:p}`einstein1920,dirac1930`.
```

Result: Several authors contributed {cite:p}`einstein1920,dirac1930`.

## Printing the bibliography

The template uses two bibliography levels:

- **Global**: the final `Bibliography` page gathers the entries cited in the book, not every entry from `book/_static/references.bib`.
- **Local**: an individual page can show only its own references in an HTML-only block.

### Global book bibliography

The global bibliography is already prepared on the final `Bibliography` page:

````md
```{bibliography}
:cited:
```
````

Do not add this block to normal pages: it should exist only on the global bibliography page.

```{note}
If you add local bibliographies to web pages, some entries will also appear on the global `Bibliography` page. This is expected: the local bibliography helps with page-level reading, while the global page gathers the whole book bibliography. In PDF, only the final global bibliography is printed.
```

### Local page bibliography

For a local bibliography on the web, cite with `{cite:t}` or `{cite:p}` in the normal page text and add a filtered `{bibliography}` directive inside `{only} html` at the end. This lets HTML show page-level references, while the PDF keeps only the final global bibliography.

`````md
Text with a local citation {cite:p}`citation_key`.

````{only} html
## Bibliography for this page

```{bibliography}
:filter: docname in docnames
```
````
`````

You can also show only selected keys from the document in HTML:

`````md
````{only} html
```{bibliography}
:filter: docname in docnames and key in {"ziman2000", "hodson1996"}
```
````
`````

In this local example, {cite:t}`ziman2000` describes science as a social practice, not just as a collection of results. Laboratory work should be connected to explanation-building, not only to following instructions {cite:p}`hodson1996`.

````{only} html
Local result:

```{bibliography}
:filter: docname in docnames and key in {"ziman2000", "hodson1996"}
```
````

## Workflow

1. Add BibTeX entries to `_static/references.bib`.
2. Cite with `{cite:t}` or `{cite:p}` on any page.
3. If you want a local bibliography visible in HTML, add an `{only} html` block with a filtered `{bibliography}` directive at the end of the page.
4. In PDF, do not generate local bibliographies: the template creates a temporary `.bib` with the used citations and shows them only on the global `Bibliography` page.

```{warning}
Each citation key (e.g., `einstein1920`) must be unique across the entire `.bib` file. Duplicates will cause a build failure.
```
