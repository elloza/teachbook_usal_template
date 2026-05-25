# 1. What is a TeachBook?

A [**TeachBook**](https://teachbooks.io/) is a digital teaching book, built from text files, code, and multimedia resources, which are then compiled into a **navigable website** and, in the case of this course, also a **PDF version**.

In simple terms:

- you edit the **source content**
- the system **builds** it
- you get an **attractive, functional, publishable** book

````{only} html
```{raw} html
<figure class="align-center">
  <picture>
    <source srcset="../../_static/images/1_Que_es_un_teachbook_en.webp" type="image/webp">
    <img src="../../_static/images/1_Que_es_un_teachbook_en.png" alt="Visual overview of what a TeachBook is" style="width: 85%;">
  </picture>
  <figcaption>A TeachBook starts from editable content and produces a publishable teaching website.</figcaption>
</figure>
```
````

````{only} latex
```{figure} ../../_static/images/1_Que_es_un_teachbook_en.png
---
name: fig-what-is-a-teachbook
alt: Visual overview of what a TeachBook is
width: 85%
align: center
---
A TeachBook starts from editable content and produces a publishable teaching website.
```
````

## Attribution and origin

This template is built on the original ecosystem of:

- [TeachBooks](https://teachbooks.io/)
- [Jupyter Book](https://jupyterbook.org/)

To situate the template, it is useful to cite both the TeachBooks project documentation {cite:p}`teachbooksmanual2025` and the reference work for Jupyter Book {cite:p}`jupyterbook2025`: the former provides the teaching-oriented approach, while the latter provides the underlying system for building publishable computational books.

This specific adaptation has been prepared for the course entitled "Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial", taught at the **Faculties of Sciences and Chemical Sciences at the University of Salamanca (USAL)**.

This matters: **we are not starting from scratch**. We are starting from existing tools and previous projects, and building on top of them a template adapted to a specific real teaching use (adapted to the needs of each course, but with reuse potential).

## What goes in and what comes out

The core idea is this:


The following table summarizes the main elements of this section.

**Table. What goes in and what comes out.**

| You start with... | And you get... |
|---|---|
| `.md` and `.ipynb` files | book web pages |
| images, bibliography, and static assets | enriched content |
| book configuration (`_config_*.yml`) | navigation, theme, language, extensions |
| table of contents (`_toc_*.yml`) | visible book structure |

## Why this is useful for teaching

1. **Accessibility**: the book can be read on the web from any device.
2. **Reproducibility**: the content comes from source files that can be versioned.
3. **Maintainability**: updating a page is much easier (thanks to AI agents) than rebuilding a whole set of notes.
4. **Scalability**: you can start with one page or chapter and grow gradually.
5. **Compatibility**: the same project can serve as both a website and a classic PDF book.

## What this template adds on top of the original base

On top of TeachBooks and Jupyter Book, this project adds several practical improvements for teachers and students:

### 1. Multilingual structure

The book is prepared to work in:

- Spanish
- English

with synchronized indexes and content. More languages could be added easily.

### 2. PDF export

Besides the website, this template prepares a PDF output designed for printing or offline distribution. Not all multimedia and interactive content can be exported, but the rest of the valuable content can, making it possible to have a traditional version of the book.

### 3. Simple automation scripts

You do not need to learn a complicated workflow on day one. The project includes SKILLS to:

- prepare the environment (install dependencies, configure variables, etc.)
- build the website (generate the navigable book locally so you can review it)
- open live preview
- export PDF
- convert PDF to Markdown (to reuse content you already have in PDF from other subjects or courses)
- etc.

### 4. AI agent integration

The template is prepared so an agent can help you:

- create content
- reorganize chapters
- add multimedia
- maintain the structure of the book
- etc.

## What a TeachBook is NOT

It is not:

- a PowerPoint presentation
- a React-style web app with heavy JS frameworks
- a custom-designed website (although the theme can be customized, that is not the main goal)

The main idea is that the content remains **editable, structured, and reusable**.

## Practical advice to start

Do not try to build a huge book on the first day.

Start small:

- a cover page
- one short chapter
- one image
- one equation
- one section with two or three pages

Once that works well and you have been able to publish it, expand.

````{only} html
## Bibliography for this page

```{bibliography}
:filter: docname in docnames and key in {"teachbooksmanual2025", "jupyterbook2025"}
```
````
