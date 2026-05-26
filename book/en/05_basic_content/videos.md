(videos)=
# Videos

Videos greatly enrich teaching materials. However, videos **cannot be embedded in PDF**, so you must always provide a text alternative.

## YouTube video (HTML + PDF)

ALWAYS use this dual pattern with `{raw} html` and `{raw} latex`:

````md
```{raw} html
<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>
```

```{raw} latex
\begin{center}
\textbf{Video:} \url{https://www.youtube.com/watch?v=dQw4w9WgXcQ}
\end{center}
```
````

Result:

```{raw} html
<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>
```

```{raw} latex
\begin{center}
\textbf{Video:} \url{https://www.youtube.com/watch?v=dQw4w9WgXcQ}
\end{center}
```

## How to get a YouTube video ID

1. Open the video in your browser.
2. The URL has this format: `https://www.youtube.com/watch?v=VIDEO_ID`
3. Use `VIDEO_ID` in the embed URL: `https://www.youtube.com/embed/VIDEO_ID`

For example, if the URL is `https://www.youtube.com/watch?v=abc123`, the iframe uses `https://www.youtube.com/embed/abc123`.

## Local video (HTML5)

For videos hosted in `_static/`:

````md
```{raw} html
<video width="720" controls preload="metadata" style="max-width: 100%; height: auto;">
  <source src="../../_static/videos/mi_primer_libro_desde_cero.mp4" type="video/mp4">
  Your browser does not support HTML5 video.
</video>
```

```{raw} latex
\begin{center}
\textbf{Local video: My first book from scratch}\\
Local file: \texttt{book/\_static/videos/mi\_primer\_libro\_desde\_cero.mp4}. See the digital version to play it.
\end{center}
```
````

Result:

```{raw} html
<video width="720" controls preload="metadata" style="max-width: 100%; height: auto;">
  <source src="../../_static/videos/mi_primer_libro_desde_cero.mp4" type="video/mp4">
  Your browser does not support HTML5 video.
</video>
```

```{raw} latex
\begin{center}
\textbf{Local video: My first book from scratch}\\
Local file: \texttt{book/\_static/videos/mi\_primer\_libro\_desde\_cero.mp4}. See the digital version to play it.\\
Duration: 6:32.
\end{center}
```

**Duration:** 6:32 | **Topic:** creating a first TeachBook from scratch.

Recommended path for local book videos:

- `book/_static/videos/mi_primer_libro_desde_cero.mp4`

## Externally generated videos

The base installation of this template avoids heavy video-generation dependencies. If you need an animation, a screen recording, or a recorded explanation, generate the `.mp4` with the external tool of your choice and save the result in `book/_static/videos/`.

Then insert it with the local video pattern above and always add the `{raw} latex` block so the PDF keeps a textual reference.

## Video with description

It is good practice to add context before the video:

```md
The following video shows the crystallization process of copper sulfate:

[insert video block here]

Duration: 4:32 | Topic: Crystallization
```

## Recommended complete pattern

````md
The following video shows the experimental setup:

```{raw} html
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allowfullscreen></iframe>
```

```{raw} latex
\begin{center}
\textbf{Video: Experimental setup}\\
\url{https://www.youtube.com/watch?v=VIDEO_ID}
\end{center}
```

**Duration:** 5:15 | **Topic:** Chemical kinetics
````

```{warning}
NEVER use only `{raw} html` without the `{raw} latex` block. The PDF will contain no reference to the video and the reader will lose information.
```
