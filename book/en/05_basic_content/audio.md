(audio)=
# Audio

Audio is useful for pronunciations, interview excerpts, signals, recorded explanations, or sound examples. In HTML it can be played with the `<audio>` element, but PDF cannot contain an audio player, so every audio block must include a text alternative.

## Local audio with HTML5

Save audio files in `book/_static/audio/` and reference them from the page with a relative path. The following example uses a locally generated 440 Hz tone so the book does not depend on external services.

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

Result:

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

**Duration:** 2 s | **Type:** 440 Hz sine tone | **Teaching use:** minimal example of a local audio player.

## Recommended formats

The following table summarizes when each format is useful.

**Table. Recommended audio formats.**

| Format | When to use it | Notes |
|---|---|---|
| WAV | Short examples, generated signals, or material that should remain uncompressed | Compatible and dependency-free to generate, but larger |
| MP3 | Voice, recorded explanations, music, or longer audio already exported from another tool | Practical option for long files |
| OGG | Additional source for compatible browsers | Do not use it as the only format if maximum compatibility matters |

## Recommended complete pattern

For real teaching content, add context before the player and a short description after it:

````md
The following audio contains a short pronunciation that students should compare with the phonetic transcription.

```{raw} html
<audio controls preload="metadata">
  <source src="../../_static/audio/my_audio.mp3" type="audio/mpeg">
  Your browser does not support the HTML5 audio element.
</audio>
```

```{raw} latex
\begin{center}
\textbf{Audio: pronunciation example}\\
Local file: \texttt{book/\_static/audio/my\_audio.mp3}. See the digital version to play it.
\end{center}
```

**Duration:** 0:18 | **Topic:** pronunciation | **Source:** own recording.
````

```{warning}
Do not use `autoplay`. Audio should play only when the reader presses the control. Also, if the audio is not yours, always include the source and license.
```

## Good practices

1. Always add a title, duration, and teaching context.
2. Use `preload="metadata"` so the browser loads only basic information.
3. For recorded lectures or long audio files, include a short summary or transcript.
4. Store local audio in `book/_static/audio/`.
5. Always add the `{raw} latex` block with the text alternative for PDF.
