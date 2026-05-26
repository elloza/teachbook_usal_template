(videos)=
# Vídeos

Los vídeos enriquecen enormemente el material docente. Sin embargo, los vídeos **no se pueden incrustar en PDF**, así que es obligatorio proporcionar siempre una alternativa en texto.

## Vídeo de YouTube (HTML + PDF)

Usa SIEMPRE este patrón dual con `{raw} html` y `{raw} latex`:

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

Resultado:

```{raw} html
<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>
```

```{raw} latex
\begin{center}
\textbf{Video:} \url{https://www.youtube.com/watch?v=dQw4w9WgXcQ}
\end{center}
```

## Cómo obtener el ID de un vídeo de YouTube

1. Abre el vídeo en tu navegador.
2. La URL tiene este formato: `https://www.youtube.com/watch?v=VIDEO_ID`
3. Usa `VIDEO_ID` en la URL de incrustación: `https://www.youtube.com/embed/VIDEO_ID`

Por ejemplo, si la URL es `https://www.youtube.com/watch?v=abc123`, el iframe usa `https://www.youtube.com/embed/abc123`.

## Vídeo local (HTML5)

Para vídeos alojados en `_static/`:

````md
```{raw} html
<video width="720" controls preload="metadata" style="max-width: 100%; height: auto;">
  <source src="../../_static/videos/mi_primer_libro_desde_cero.mp4" type="video/mp4">
  Tu navegador no soporta vídeo HTML5.
</video>
```

```{raw} latex
\begin{center}
\textbf{Video local: Mi primer libro desde cero}\\
Archivo local: \texttt{book/\_static/videos/mi\_primer\_libro\_desde\_cero.mp4}. Consulte la version digital para reproducirlo.
\end{center}
```
````

Resultado:

```{raw} html
<video width="720" controls preload="metadata" style="max-width: 100%; height: auto;">
  <source src="../../_static/videos/mi_primer_libro_desde_cero.mp4" type="video/mp4">
  Tu navegador no soporta vídeo HTML5.
</video>
```

```{raw} latex
\begin{center}
\textbf{Video local: Mi primer libro desde cero}\\
Archivo local: \texttt{book/\_static/videos/mi\_primer\_libro\_desde\_cero.mp4}. Consulte la version digital para reproducirlo.\\
Duracion: 6:32.
\end{center}
```

**Duración:** 6:32 | **Tema:** creación de un primer TeachBook desde cero.

Ruta recomendada para los vídeos locales del libro:

- `book/_static/videos/mi_primer_libro_desde_cero.mp4`

## Vídeos generados externamente

La instalación base de esta plantilla evita dependencias pesadas de generación de vídeo. Si necesitas una animación, una captura o una explicación grabada, genera el `.mp4` con la herramienta externa que prefieras y guarda el resultado en `book/_static/videos/`.

Después insértalo con el patrón de vídeo local anterior y añade siempre el bloque `{raw} latex` para que el PDF conserve una referencia textual.

## Vídeo con descripción

Es buena práctica añadir contexto antes del vídeo:

```md
El siguiente vídeo muestra el proceso de cristalización del sulfato de cobre:

[insertar bloque de vídeo aquí]

Duración: 4:32 | Tema: Cristalización
```

## Patrón completo recomendado

````md
El siguiente vídeo muestra el montaje experimental:

```{raw} html
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allowfullscreen></iframe>
```

```{raw} latex
\begin{center}
\textbf{Video: Montaje experimental}\\
\url{https://www.youtube.com/watch?v=VIDEO_ID}
\end{center}
```

**Duración:** 5:15 | **Tema:** Cinética química
````

```{warning}
NUNCA uses solo `{raw} html` sin el bloque `{raw} latex`. El PDF no contendrá ninguna referencia al vídeo y el lector perderá información.
```
