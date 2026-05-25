(compatibilidad_html_pdf)=
# Compatibilidad HTML y PDF

Tu TeachBook se publica en dos formatos: **HTML** (web interactiva) y **PDF** (versión imprimible). No todo funciona igual en ambos. Esta página te ayuda a escribir contenido que funcione siempre.

## Tabla de compatibilidad


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Tabla de compatibilidad.**

| Elemento | HTML | PDF | Estrategia |
|----------|------|-----|-----------|
| Texto, listas, enlaces | ✅ | ✅ | Usar libremente |
| Imágenes (`{image}`, `{figure}`) | ✅ | ✅ | Usar libremente |
| Ecuaciones LaTeX (`$...$`, `$$...$$`) | ✅ | ✅ | Usar libremente |
| Tablas | ✅ | ✅ | Usar libremente |
| Admoniciones (`{note}`, `{tip}`…) | ✅ | ✅ | Usar libremente |
| Dropdowns (`:class: dropdown`) | ✅ | ✅ expandido | En PDF se muestra expandido |
| Código con resaltado | ✅ | ✅ | Usar libremente |
| Citas BibTeX | ✅ | ✅ | Usar libremente |
| Referencias cruzadas | ✅ | ✅ | Usar libremente |
| Diagramas Kroki (Mermaid, PlantUML, etc.) | ✅ | ✅ | Usar `{kroki}` con `:type: mermaid` |
| Vídeos (iframe/YouTube) | ✅ | ❌ | Usar `{raw} latex` con URL |
| Pestañas (`{tabbed}`, `{tab-set}`) | ✅ | ❌ | En PDF: contenido secuencial |
| HTML interactivo (`<details>`) | ✅ | ❌ | Usar `{raw} latex` alternativo |
| Thebe (código en vivo) | ✅ | ❌ | Código visible como texto en PDF |

## Patrón universal: HTML + LaTeX fallback

Para cualquier contenido que solo funcione en HTML, usa este patrón:

````md
```{raw} html
<!-- Contenido interactivo aquí -->
<div>...</div>
```

```{raw} latex
\begin{center}
Texto alternativo para el PDF.
\end{center}
```
````

## Ejemplo: vídeo con fallback

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

## Ejemplo: diagrama con Kroki

````md
```{kroki}
:type: mermaid
:align: center

flowchart LR
    A --> B --> C
```
````

## Reglas prácticas

1. **Si es texto, imagen, ecuación o tabla**: no te preocupes, funciona en ambos.
2. **Si es interactivo (vídeo, HTML personalizado)**: añade SIEMPRE una alternativa textual.
3. **Si es un diagrama**: usa Kroki. Funciona en HTML y PDF.
4. **Si es un dropdown**: en PDF se muestra expandido (no hay problema).
5. **Si son pestañas**: en PDF se muestra todo seguido (verifica que tenga sentido).

```{tip}
Antes de publicar, compila siempre ambos formatos (`build_book.py` para HTML y `export_pdf.py` para PDF) y revisa que el contenido es coherente en ambos.
```
