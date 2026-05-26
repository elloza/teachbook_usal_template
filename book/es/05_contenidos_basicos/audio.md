(audio)=
# Audio

El audio es útil para incluir pronunciaciones, fragmentos de entrevistas, señales, explicaciones grabadas o ejemplos de sonido. En HTML puede reproducirse con el elemento `<audio>`, pero en PDF no existe un reproductor: por eso siempre debe añadirse una alternativa textual.

## Audio local con HTML5

Guarda los archivos de audio en `book/_static/audio/` y enlázalos desde la página con una ruta relativa. El ejemplo siguiente usa un tono de 440 Hz generado localmente para que el libro no dependa de servicios externos.

````md
```{raw} html
<audio controls preload="metadata">
  <source src="../../_static/audio/sample_tone_440hz.wav" type="audio/wav">
  Tu navegador no soporta el elemento de audio HTML5.
</audio>
```

```{raw} latex
\begin{center}
\textbf{Audio: tono de 440 Hz}\\
Recurso local: \texttt{book/\_static/audio/sample\_tone\_440hz.wav}. Consulte la version digital para reproducirlo.
\end{center}
```
````

Resultado:

```{raw} html
<audio controls preload="metadata">
  <source src="../../_static/audio/sample_tone_440hz.wav" type="audio/wav">
  Tu navegador no soporta el elemento de audio HTML5.
</audio>
```

```{raw} latex
\begin{center}
\textbf{Audio: tono de 440 Hz}\\
Recurso local: \texttt{book/\_static/audio/sample\_tone\_440hz.wav}. Consulte la version digital para reproducirlo.
\end{center}
```

**Duración:** 2 s | **Tipo:** tono sinusoidal de 440 Hz | **Uso docente:** ejemplo mínimo de reproductor local.

## Formatos recomendados

La tabla siguiente resume cuándo conviene usar cada formato.

**Tabla. Formatos de audio recomendados.**

| Formato | Cuándo usarlo | Observaciones |
|---|---|---|
| WAV | Ejemplos breves, señales generadas o material que debe conservarse sin compresión | Es compatible y puede generarse sin dependencias, pero ocupa más espacio |
| MP3 | Voz, explicaciones grabadas, música o audios largos ya exportados | Es la opción práctica para archivos largos |
| OGG | Fuente adicional para navegadores compatibles | No debe ser el único formato si se busca máxima compatibilidad |

## Patrón completo recomendado

Para contenido docente real, añade contexto antes del reproductor y una descripción después:

````md
El siguiente audio recoge una pronunciación breve que el estudiante debe comparar con la transcripción fonética.

```{raw} html
<audio controls preload="metadata">
  <source src="../../_static/audio/mi_audio.mp3" type="audio/mpeg">
  Tu navegador no soporta el elemento de audio HTML5.
</audio>
```

```{raw} latex
\begin{center}
\textbf{Audio: pronunciacion de ejemplo}\\
Archivo local: \texttt{book/\_static/audio/mi\_audio.mp3}. Consulte la version digital para reproducirlo.
\end{center}
```

**Duración:** 0:18 | **Tema:** pronunciación | **Fuente:** grabación propia.
````

```{warning}
No uses `autoplay`. El audio debe reproducirse solo cuando el lector pulse el control. Además, si el audio no es propio, indica siempre la fuente y la licencia.
```

## Buenas prácticas

1. Añade siempre un título, duración y contexto docente.
2. Usa `preload="metadata"` para que el navegador cargue solo la información básica.
3. Para clases grabadas o audios largos, incluye un resumen o una transcripción breve.
4. Guarda los audios locales en `book/_static/audio/`.
5. Añade siempre el bloque `{raw} latex` con la alternativa textual para PDF.
