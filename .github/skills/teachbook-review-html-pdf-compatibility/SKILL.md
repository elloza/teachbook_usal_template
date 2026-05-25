---
name: teachbook-review-html-pdf-compatibility
description: >
  Revisa el contenido del libro para verificar compatibilidad entre HTML y PDF.
  Detecta elementos que solo funcionan en HTML y verifica que existan alternativas para PDF.
  Trigger phrases: "compatibilidad", "HTML PDF", "revisar PDF", "solo HTML", "fallback",
  "verificar multimedia", "auditar formato".
---

# Skill: Revisar Compatibilidad HTML/PDF

## Objetivo

Auditar el contenido del TeachBook para asegurarse de que todo funciona tanto en la versión web (HTML) como en la versión imprimible (PDF).

## Tabla de compatibilidad

| Elemento | HTML | PDF | Acción si solo HTML |
|---|---|---|---|
| Texto, listas, enlaces | ✅ | ✅ | — |
| Imágenes `{image}` / `{figure}` | ✅ | ✅ | — |
| Ecuaciones LaTeX `$...$` | ✅ | ✅ | — |
| Tablas markdown | ✅ | ✅ | — |
| Admonitions (note, tip, warning) | ✅ | ✅ | — |
| Dropdown `{admonition} :class: dropdown` | ✅ | ✅ expandido | — |
| Tabs `{tab}` | ✅ | ❌ | Añadir alternativa textual |
| Código con syntax highlighting | ✅ | ✅ | — |
| Mermaid `{mermaid}` | ✅ | ❌ | Añadir descripción textual |
| YouTube iframe | ✅ | ❌ | Añadir `{raw} latex` con URL |
| Thebe live code | ✅ | ❌ | Código visible como texto estático |
| JupyterQuiz | ✅ | ❌ | Añadir preguntas en formato admonition |
| HTML personalizado `{raw} html` | ✅ | ❌ | Añadir `{raw} latex` fallback |
| ipywidgets | ✅ | ❌ | Añadir versión sin widgets |
| Citas BibTeX | ✅ | ✅ | — |
| Referencias cruzadas | ✅ | ✅ | — |

## Proceso de revisión

### Paso 1: Escanear archivos

Buscar en todos los `.md` e `.ipynb` de `book/es/` y `book/en/`:

1. `{mermaid}` sin texto alternativo → ⚠️
2. `{raw} html` sin correspondiente `{raw} latex` → ❌
3. `iframe` sin `{raw} latex` → ❌
4. `{tab}` sin alternativa → ⚠️
5. `jupyterquiz` sin alternativa admonition → ⚠️
6. `ipywidgets` sin alternativa → ⚠️
7. `{thebe-button}` sin nota de compatibilidad → ⚠️

### Paso 2: Generar informe

Formato:

```markdown
## Informe de Compatibilidad HTML/PDF

### ❌ Problemas críticos (rompen el PDF)
- [archivo]: [descripción del problema]

### ⚠️ Advertencias (funciona pero pierde contenido)
- [archivo]: [descripción]

### ✅ Todo correcto
- [lista de archivos sin problemas]
```

### Paso 3: Ofrecer correcciones

Para cada problema encontrado, proponer la corrección específica:

- Mermaid sin fallback → añadir `{admonition}` con descripción tras el diagrama
- iframe sin LaTeX → añadir bloque `{raw} latex` con `\url{...}`
- Tabs sin alternativa → añadir sección con el contenido de todas las tabs

## Regla de oro

> **Todo contenido debe ser comprensible tanto en la versión web como en la versión impresa.**

Si algo es imposible en PDF (como un video), la versión impresa debe contener como mínimo:
- Un texto describiendo qué es
- Una URL o referencia para acceder al recurso original
