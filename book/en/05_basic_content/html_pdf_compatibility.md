(html_pdf_compatibility)=
# HTML and PDF Compatibility

Your TeachBook is published in two formats: **HTML** (interactive web) and **PDF** (printable version). Not everything works the same in both. This page helps you write content that always works.

## Compatibility table


The following table summarizes the main elements of this section.

**Table. Compatibility table.**

| Element | HTML | PDF | Strategy |
|---------|------|-----|----------|
| Text, lists, links | ✅ | ✅ | Use freely |
| Images (`{image}`, `{figure}`) | ✅ | ✅ | Use freely |
| LaTeX math (`$...$`, `$$...$$`) | ✅ | ✅ | Use freely |
| Tables | ✅ | ✅ | Use freely |
| Admonitions (`{note}`, `{tip}`…) | ✅ | ✅ | Use freely |
| Dropdowns (`:class: dropdown`) | ✅ | ✅ expanded | In PDF it appears expanded |
| Syntax-highlighted code | ✅ | ✅ | Use freely |
| BibTeX citations | ✅ | ✅ | Use freely |
| Cross-references | ✅ | ✅ | Use freely |
| Kroki diagrams (Mermaid, PlantUML, etc.) | ✅ | ✅ | Use `{kroki}` with `:type: mermaid` |
| Videos (iframe/YouTube) | ✅ | ❌ | Use `{raw} latex` with URL |
| Audio (`<audio>`) | ✅ | ❌ | Use `{raw} latex` with description and path |
| Tabs (`{tabbed}`, `{tab-set}`) | ✅ | ❌ | In PDF: sequential content |
| Interactive HTML (`<details>`) | ✅ | ❌ | Use `{raw} latex` alternative |
| Thebe (live code) | ✅ | ❌ | Code visible as text in PDF |

## Universal pattern: HTML + LaTeX fallback

For any content that only works in HTML, use this pattern:

````md
```{raw} html
<!-- Interactive content here -->
<div>...</div>
```

```{raw} latex
\begin{center}
Alternative text for the PDF.
\end{center}
```
````

## Example: video with fallback

````md
```{raw} html
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allowfullscreen></iframe>
```

```{raw} latex
\begin{center}
\textbf{Video:} \url{https://www.youtube.com/watch?v=VIDEO_ID}
\end{center}
```
````

## Example: audio with fallback

````md
```{raw} html
<audio controls preload="metadata">
  <source src="../../_static/audio/sample_tone_440hz.wav" type="audio/wav">
  Your browser does not support the HTML5 audio element.
</audio>
```

```{raw} latex
\begin{center}
\textbf{Audio: 440 Hz tone}\\
Local resource: \texttt{book/\_static/audio/sample\_tone\_440hz.wav}. See the digital version to play it.
\end{center}
```
````

## Example: diagram with Kroki

````md
```{kroki}
:type: mermaid
:align: center

flowchart LR
    A --> B --> C
```
````

## Practical rules

1. **If it is text, image, equation, or table**: do not worry, it works in both.
2. **If it is interactive (video, audio, custom HTML)**: ALWAYS add a text alternative.
3. **If it is a diagram**: use Kroki. It works in both HTML and PDF.
4. **If it is a dropdown**: in PDF it appears expanded (no problem).
5. **If it uses tabs**: in PDF everything appears sequentially (verify it still makes sense).

```{tip}
Before publishing, always build both formats (`build_book.py` for HTML and `export_pdf.py` for PDF) and verify the content is coherent in both.
```
