---
name: teachbook-multimedia
description: >
  Guía para insertar contenido multimedia en el libro: imágenes, audio, videos de YouTube,
  ecuaciones LaTeX, tablas, admoniciones, código ejecutable y citas bibliográficas.
  Todos los patrones son compatibles con HTML y PDF simultáneamente.
  Trigger phrases: "insertar imagen", "añadir video", "YouTube", "fórmula", "ecuación",
  "tabla", "nota", "advertencia", "cita bibliográfica", "imagen", "multimedia",
  "insertar multimedia", "video", "audio", "BibTeX", "referencia", "add image", "add video".
---

# Skill: Contenido Multimedia (HTML + PDF)

## Regla fundamental

Todo contenido multimedia debe funcionar en **HTML** (web) y en **PDF** (imprimible). Los patrones de esta skill garantizan compatibilidad con ambos formatos.

---

## 1. Imágenes

**Compatibilidad: HTML ✅ PDF ✅**

```markdown
```{image} _static/mi_imagen.png
:alt: Descripción textual de la imagen
:width: 80%
:align: center
```
```

- Formatos recomendados: **PNG**, **JPG** o **SVG** (SVG solo en HTML; para PDF convertir a PNG).
- Ubicación: `book/_static/` (compartido) o junto al archivo `.md`.
- La ruta es relativa al archivo `.md` donde se inserta.

**Error común**: Usar sintaxis de imagen estándar `![alt](ruta)` — funciona en HTML pero puede dar problemas en PDF. Preferir siempre la directiva `{image}`.

### Formatos y optimización web

- Mantener **PNG** como formato principal cuando la imagen deba funcionar igual en HTML y PDF.
- Usar **JPG/JPEG** para fotografías sin transparencia.
- Usar **SVG** para diagramas vectoriales renderizados, con los fallbacks PDF ya gestionados por el proyecto.
- Usar **WebP** solo como mejora HTML si existe fallback PNG/JPG y se ha probado PDF. No convertir todo el libro a WebP por defecto.
- Tras añadir o sustituir imágenes, ejecutar `python scripts/optimize_static_assets.py --check`.
- Para optimización conservadora sin cambiar rutas ni formatos, ejecutar `python scripts/optimize_static_assets.py --fix`.
- El script usa Pillow dentro de `.venv`, por lo que es repetible en Windows, macOS y Linux.

### GIFs animados con fallback PDF

**Compatibilidad: HTML ✅ PDF ✅ (con `.png` equivalente)**

Para un GIF animado docente, insertar el `.gif` con `{figure}` y guardar al lado un `.png` con el mismo nombre base:

````markdown
```{figure} ../../_static/tutorial_gifs/es/paso_01.gif
---
name: fig-paso-01
alt: Descripción del GIF animado
width: 90%
align: center
---
Descripción breve del paso mostrado.
```
````

- En **HTML**: se muestra el `.gif`.
- En **PDF**: `scripts/export_pdf.py` sustituye la referencia por `paso_01.png` en la copia temporal.
- Si falta el `.png` equivalente, la exportación PDF debe fallar con un mensaje claro.

**Regla práctica**: GIF animado = `.gif` para HTML + `.png` del mismo nombre para PDF.

---

## 2. Videos de YouTube

**Compatibilidad: HTML ✅ PDF ✅ (con patrón dual)**

Usar SIEMPRE este patrón dual. NUNCA usar iframe sin el bloque `{raw} latex` alternativo:

````markdown
```{raw} html
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allowfullscreen></iframe>
```

```{raw} latex
\begin{center}
\textbf{Video:} \url{https://www.youtube.com/watch?v=VIDEO_ID}
\end{center}
```
````

Reemplazar `VIDEO_ID` por el ID real del video (los caracteres después de `v=` en la URL).

- En **HTML**: se ve el video embebido con el reproductor de YouTube.
- En **PDF**: se ve un enlace de texto al video.

**Error crítico**: Usar `{raw} html` sin el bloque `{raw} latex`. Esto causa que el PDF falle o muestre contenido vacío.

Si el contenido HTML necesita una cita bibliográfica en PDF, NO pongas la cita solo dentro de `{raw} html`. Añade la cita en el fallback `{raw} latex` con sintaxis LaTeX, por ejemplo `\cite{smith2023}`. `scripts/export_pdf.py` recoge esas citas LaTeX y las incluye en el `.bib` temporal del PDF.

---

## 3. Audio local HTML5

**Compatibilidad: HTML ✅ PDF ✅ (con patrón dual)**

Usar este patrón para audios alojados en `book/_static/audio/`. NUNCA usar `<audio>` sin el bloque `{raw} latex` alternativo:

````markdown
```{raw} html
<audio controls preload="metadata">
  <source src="../../_static/audio/mi_audio.mp3" type="audio/mpeg">
  Tu navegador no soporta el elemento de audio HTML5.
</audio>
```

```{raw} latex
\begin{center}
\textbf{Audio: titulo del recurso}\\
Archivo local: \texttt{book/\_static/audio/mi\_audio.mp3}. Consulte la version digital para reproducirlo.
\end{center}
```
````

- En **HTML**: se muestra el reproductor nativo del navegador.
- En **PDF**: se muestra una referencia textual al recurso.
- Usar `preload="metadata"` y evitar `autoplay`.
- Para audios largos, añadir resumen o transcripción breve.
- Si el audio no es propio, indicar fuente y licencia.

Formatos recomendados:

| Formato | Uso recomendado |
|---|---|
| WAV | Ejemplos breves o señales generadas sin dependencias |
| MP3 | Voz, explicaciones grabadas o audios largos ya exportados |
| OGG | Fuente adicional, no como único formato |

---

## 4. Ecuaciones LaTeX

**Compatibilidad: HTML ✅ PDF ✅**

Ecuación inline:
```markdown
La energía se define como $E = mc^2$ en la teoría de la relatividad.
```

Ecuación display (bloque centrado):
```markdown
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

Requiere que `dollarmath` esté en `myst_enable_extensions` del `_config.yml` (ya configurado por defecto).

---

## 5. Tablas

**Compatibilidad: HTML ✅ PDF ✅**

```markdown
| Concepto | Fórmula | Unidad |
|---|---|---|
| Velocidad | $v = \dfrac{d}{t}$ | m/s |
| Fuerza | $F = ma$ | N |
| Energía | $E = mc^2$ | J |
```

- Usar al menos 3 guiones `---` en la fila separadora.
- Se pueden combinar con ecuaciones LaTeX inline dentro de las celdas.

---

## 6. Admoniciones (bloques destacados)

**Compatibilidad: HTML ✅ PDF ✅**

````markdown
```{note}
Este es un bloque de nota. Aparece con estilo diferenciado.
```

```{warning}
Este es un bloque de advertencia. Úsalo para avisos importantes.
```

```{tip}
Este es un consejo. Úsalo para recomendaciones útiles.
```

```{admonition} Título personalizado
Este bloque admite un título personalizado.
```
````

**Error común**: Olvidar cerrar el bloque con las tres comillas invertidas `` ``` ``.

---

## 7. Código ejecutable (Notebooks)

**Compatibilidad: HTML ✅ PDF ✅**

Los archivos `.ipynb` (Jupyter notebooks) se pueden colocar junto a los `.md`. Para que el código se ejecute automáticamente durante la compilación, el `_config_<lang>.yml` debe tener:

```yaml
execute:
  execute_notebooks: auto
```

Por defecto está en `off` para velocidad de compilación. Solo activar si el usuario lo pide explícitamente.

**Nota**: Los notebooks ejecutados pueden tardar mucho en compilar. Desaconsejar su uso salvo necesidad real.

**Regla de codificación para código y gráficas**: en celdas `code`, usar texto ASCII en comentarios, `print()`, títulos, ejes y leyendas de Matplotlib. El texto docente con acentos debe ir en Markdown. Esto evita que las figuras exportadas y los bloques de código muestren letras con tilde, eñes o símbolos como `?` en HTML/PDF.

---

## 8. Citas bibliográficas (BibTeX)

**Compatibilidad: HTML ✅ PDF ✅**

Archivo de referencias: `book/_static/references.bib`

### Bibliografía global del libro

Citar en el texto con `{cite:t}` o `{cite:p}`:
```markdown
Según {cite:t}`smith2023`, los resultados confirman la hipótesis.
```

La bibliografía global debe estar en una sola página final `Bibliografía` / `Bibliography` y mostrar solo entradas citadas:
````markdown
```{bibliography}
:cited:
```
````

No añadir este bloque a páginas normales si existe la página global, porque puede provocar avisos `duplicate citation`.

### Bibliografía local de una página

Si el usuario pide que una página tenga bibliografía propia, debe generarse SOLO en HTML. Usar citas normales en el texto y cerrar con `{bibliography}` filtrada dentro de `{only} html`:

`````markdown
Según {cite:t}`smith2023`, los resultados confirman la hipótesis.

````{only} html
## Bibliografía de esta página

```{bibliography}
:filter: docname in docnames
```
````
`````

Para mostrar solo algunas claves, también dentro de `{only} html`:

`````markdown
````{only} html
```{bibliography}
:filter: docname in docnames and key in {"smith2023"}
```
````
`````

Este patrón funciona en HTML. En PDF no se deben generar bibliografías locales: `scripts/export_pdf.py` genera un `.bib` temporal con las citas usadas y las imprime solo en la página final `Bibliografía` / `Bibliography`. Como la web puede mostrar entradas en bibliografías locales y en la página global con `:cited:`, los `_config_<lang>.yml` deben mantener suprimido el aviso esperado `bibtex.duplicate_citation`.

La repetición en HTML entre una bibliografía local y la página global es aceptable: la local ayuda a leer esa página y la global reúne todo el libro. En PDF solo debe quedar la bibliografía global final.

### Citas dentro de HTML interactivo o raw

- Las citas MyST (`{cite:p}` / `{cite:t}`) deben ir en texto Markdown normal cuando deban aparecer tanto en HTML como en PDF.
- Las citas dentro de `{raw} html` no cuentan para el PDF, porque ese bloque no se imprime.
- Si el fallback `{raw} latex` necesita citar una fuente, usar `\cite{clave}` o `\cite{clave1,clave2}`. El exportador PDF añade esas claves a la bibliografía final.
- No pongas una cita únicamente en `{raw} html` si esa fuente debe aparecer en la bibliografía final del PDF.

Para validar claves o generar un `.bib` de inspección con las citas usadas:

```bash
python scripts/collect_used_bibliography.py --lang es --output .build_logs/references_used_es.bib
```

Entrada de ejemplo en `references.bib`:
```bibtex
@article{smith2023,
  author  = {Smith, John},
  title   = {A Study on Something},
  journal = {Journal of Examples},
  year    = {2023},
  volume  = {1},
  pages   = {1--10}
}
```

---

## Resumen de compatibilidad

| Tipo | HTML | PDF | Notas |
|---|---|---|---|
| Imágenes (`{image}`) | ✅ | ✅ | PNG/JPG recomendado; validar con `optimize_static_assets.py --check` |
| YouTube (patrón dual) | ✅ | ✅ | NUNCA sin `{raw} latex` |
| Audio local (patrón dual) | ✅ | ✅ | NUNCA sin `{raw} latex`; guardar en `_static/audio/` |
| Ecuaciones (`$...$`) | ✅ | ✅ | Requiere `dollarmath` en config |
| Tablas | ✅ | ✅ | Sintaxis MyST estándar |
| Admoniciones | ✅ | ✅ | `{note}`, `{warning}`, `{tip}`, `{admonition}` |
| Notebooks (`.ipynb`) | ✅ | ✅ | Desactivado por defecto |
| BibTeX (`{cite}`) | ✅ | ✅ | Archivo: `_static/references.bib` |
