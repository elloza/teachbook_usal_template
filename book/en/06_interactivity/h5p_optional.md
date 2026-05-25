# H5P (Optional)

**H5P** is an interactive content platform that offers quizzes, drag-and-drop activities, video interactions, and much more.

```{warning}
H5P is **optional** and **not a dependency** of this template. It requires an external server to host the content (H5P.com, Moodle, WordPress with H5P plugin, etc.). It is not self-contained.
```

## What does H5P offer?


The following table summarizes the main elements of this section.

**Table. What does H5P offer?.**

| Activity type | Description |
|---------------|-------------|
| Quizzes | Multiple choice, fill in the blanks |
| Drag & Drop | Drag elements to correct zones |
| Interactive video | Add pauses with questions on a video |
| Interactive presentation | Slides with integrated questions |
| Summary | Text with interspersed questions |

## How to embed H5P in your TeachBook

Create your content on the H5P platform and use an `iframe` to display it:

````md
```{raw} html
<iframe src="https://H5P_URL_HERE" width="800" height="600" frameborder="0" allowfullscreen="allowfullscreen" style="border: 1px solid #e5e7eb; border-radius: 8px;"></iframe>
```

```{raw} latex
\textbf{Interactive H5P activity:} Available in the web version of the book.
Link: \url{https://H5P_URL_HERE}
```
````

## Compatible platforms

- **H5P.com**: Official service (paid for advanced use).
- **Moodle**: Free plugin, ideal if your university already uses Moodle.
- **WordPress**: Free H5P plugin.
- **Lumi**: Desktop application to create H5P without a server.

```{admonition} Recommended alternative
:class: tip
If you don't need the complexity of H5P, **exercises with solutions** (using `{admonition}` with `dropdown`) cover most assessment needs and work in both HTML and PDF, with no external server required.
```
