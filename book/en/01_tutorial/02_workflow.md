# 2. Workflow

This is the recommended workflow for your TeachBook:

1. **Write content** in Markdown files (`.md`) or Notebooks (`.ipynb`). In the case of Notebooks, it is important to execute them beforehand so that the book keeps the cell outputs. The AI agent can help you write the content and execute the Notebooks.
2. **Preview** with `python scripts/launch_preview.py` to see the same build that will be published. In this course, you can ask the AI agent to do it for you, because it has the information it needs.
3. **Save versions** with Git (`commit`). The AI agent will help you save changes in an orderly way.
4. **Publish** to GitHub (`push`) so the website updates automatically through GitHub Pages.

## Book Development Cycle

1. Modify or add content in Markdown files or Notebooks.
2. Build the book and start a local server to preview the changes.
3. Generate the PDF versions of the book when needed. That process first creates LaTeX and then compiles the PDFs linked from the website.
4. If everything is correct, commit the changes with Git.
5. Publish the changes to GitHub to deploy the website.
6. If you find errors or want to improve something, go back to step 1 and repeat the cycle.

{numref}`fig-teachbook-workflow` summarizes the full process: write content, preview it, review the result, version the changes, and publish the website.

```{figure} ../../_static/images/01_tutorial_02_flujo_trabajo_01_en.png
---
name: fig-teachbook-workflow
alt: Infographic of the workflow for editing, previewing, versioning, and publishing a TeachBook.
width: 90%
align: center
---
TeachBook workflow from content editing to web publication.
```

## File Structure

To work with the book, we need to understand the file and folder structure. The content is organized by language, and each language has its own table of contents and configuration. This makes it possible to maintain versions in several languages with the same content or with content adapted to each language. We follow the same philosophy as the original TeachBooks project, with a few adaptations to make it easier to use with AI assistants.

The Spanish content is organized in `book/es/`. The English content is organized in `book/en/`. Each language has its own table of contents (`_toc_*.yml`) and configuration (`_config_*.yml`), but the structure must remain coherent across languages.

Main files and folders:

- `book/es/intro.md`: main page of the Spanish version.
- `book/en/intro.md`: main page of the English version.
- `book/_toc_es.yml` and `book/_toc_en.yml`: book tables of contents; they define the order of chapters and sections.
- `book/_config_es.yml` and `book/_config_en.yml`: language-specific configuration files.
- `book/_static/`: shared images, videos, styles, scripts, PDFs, and references.
- `book/es/01_tutorial/` and `book/en/01_tutorial/`: folders for the initial tutorial.

Good practices for keeping things organized:

- Use numerical prefixes in folders and files (`01_`, `02_`, `03_`) to reflect the sequence.
- Add each new file to the TOC of the corresponding language; if it is not in the TOC, it will not appear in the navigation.
- Keep names clear and consistent, for example `03_experimental_activity.md`.
- When you add or change content in Spanish, also review the equivalent English page.

The build results are generated in `book/_build/html/`, which is the static version of the book published on GitHub Pages. You do not need to edit anything in that folder, because it is generated automatically from the source files.

The `book/_static/` folder is intended for static files such as images, videos, CSS styles, JavaScript scripts, PDFs, and references. You can place your images there and reference them from Markdown files using relative paths. If you do not know how to do that, the AI agent can help you place the images and reference them correctly.

## Directory Tree

```text
teachbook_usal_template/
├── book/
│   ├── _config_es.yml
│   ├── _config_en.yml
│   ├── _toc_es.yml
│   ├── _toc_en.yml
│   ├── _static/
│   ├── _build/
│   ├── es/
│   │   ├── intro.md
│   │   └── 01_tutorial/
│   │       ├── 01_que_es_un_teachbook.md
│   │       └── 02_flujo_trabajo.md
│   └── en/
│       ├── intro.md
│       └── 01_tutorial/
│           ├── 01_what_is_a_teachbook.md
│           └── 02_workflow.md
└── scripts/
    └── launch_preview.py
```
