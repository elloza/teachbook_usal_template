---
name: teachbook-generate-interactive-html
description: >
  Añade elementos HTML interactivos a las páginas del libro sin frameworks JS.
  Incluye secciones colapsables, pestañas CSS-only, cajas de colores y tablas estiladas.
  Siempre con fallback LaTeX para compatibilidad con PDF.
  Trigger phrases: "HTML interactivo", "interactivo", "widget", "details", "acordeón",
  "pestañas", "tabs", "colapsable", "caja de color", "tabla con estilo".
---

# Skill: HTML Interactivo (sin frameworks)

## Regla fundamental

Todo HTML personalizado va dentro de ` ```{raw} html` y **DEBE** llevar un bloque ` ```{raw} latex` como alternativa para PDF. Sin el fallback LaTeX, el PDF muestra contenido vacío o falla.

## Patrones disponibles

### 1. Secciones colapsables (acordeón)

Funciona en HTML (interactivo) y PDF (se muestra expandido).

````markdown
```{raw} html
<details>
<summary><strong>Click para ver la solución</strong></summary>

La respuesta correcta es **42**. Esto se debe a que...

</details>
```

```{raw} latex
\textbf{Solución:} La respuesta correcta es \textbf{42}. Esto se debe a que...
```
````

### 2. Caja de color con texto destacado

````markdown
```{raw} html
<div style="background-color: #e8f4f8; border-left: 4px solid #2196F3; padding: 15px; margin: 10px 0; border-radius: 4px;">
<strong>💡 Dato importante:</strong> La velocidad de la luz en el vacío es aproximadamente 299.792 km/s.
</div>
```

```{raw} latex
\begin{center}
\fbox{\parbox{0.9\textwidth}{\textbf{Dato importante:} La velocidad de la luz en el vacío es aproximadamente 299.792 km/s.}}
\end{center}
```
````

### 3. Pestañas con CSS (sin JavaScript)

````markdown
```{raw} html
<style>
.tab-container { margin: 10px 0; }
.tab-radio { display: none; }
.tab-label { display: inline-block; padding: 8px 16px; background: #f0f0f0; cursor: pointer; border: 1px solid #ddd; border-bottom: none; margin-right: 2px; }
.tab-content { display: none; padding: 15px; border: 1px solid #ddd; margin-top: 0; }
#tab1:checked ~ #content1, #tab2:checked ~ #content2 { display: block; }
#tab1:checked ~ label[for="tab1"], #tab2:checked ~ label[for="tab2"] { background: white; border-bottom: 1px solid white; }
</style>
<div class="tab-container">
<input type="radio" name="tabs" id="tab1" class="tab-radio" checked>
<input type="radio" name="tabs" id="tab2" class="tab-radio">
<label for="tab1" class="tab-label">Opción A</label>
<label for="tab2" class="tab-label">Opción B</label>
<div id="content1" class="tab-content">Contenido de la pestaña A.</div>
<div id="content2" class="tab-content">Contenido de la pestaña B.</div>
</div>
```

```{raw} latex
\textbf{Opción A:} Contenido de la pestaña A.

\textbf{Opción B:} Contenido de la pestaña B.
```
````

### 4. Tabla con estilo inline

````markdown
```{raw} html
<table style="width:100%; border-collapse: collapse; margin: 10px 0;">
<thead>
<tr style="background-color: #2196F3; color: white;">
<th style="padding: 10px; text-align: left;">Concepto</th>
<th style="padding: 10px; text-align: left;">Valor</th>
</tr>
</thead>
<tbody>
<tr style="background-color: #f5f5f5;"><td style="padding: 10px;">Velocidad</td><td style="padding: 10px;">$v = 3 \times 10^8$ m/s</td></tr>
<tr><td style="padding: 10px;">Energía</td><td style="padding: 10px;">$E = mc^2$</td></tr>
</tbody>
</table>
```
````

### 5. Cuadro de advertencia estilado

````markdown
```{raw} html
<div style="background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; margin: 10px 0; border-radius: 4px;">
<strong>⚠️ Atención:</strong> Este experimento requiere equipos de protección individual (EPI).
</div>
```

```{raw} latex
\begin{center}
\fbox{\parbox{0.9\textwidth}{\textbf{Atención:} Este experimento requiere equipos de protección individual (EPI).}}
\end{center}
```
````

## Reglas

| Regla | Detalle |
|---|---|
| Sin frameworks | **NO** usar React, Vue, Angular, ni archivos `.js` externos. |
| Sin Node | No se usa npm/yarn. Solo HTML + CSS inline. |
| Fallback LaTeX | **SIEMPRE** añadir ` ```{raw} latex` después de ` ```{raw} html`. |
| CSS inline | Todo el CSS debe ir en atributos `style="..."` o en bloques `<style>` dentro del mismo bloque. |
| IDs únicos | Si se usan IDs (pestañas), deben ser únicos en toda la página. |
| Multi-idioma | El contenido HTML debe existir en todos los idiomas. |

## Colores recomendados

| Uso | Fondo | Borde |
|---|---|---|
| Info | `#e8f4f8` | `#2196F3` |
| Éxito | `#e8f5e9` | `#4CAF50` |
| Advertencia | `#fff3e0` | `#ff9800` |
| Error | `#fbe9e7` | `#f44336` |
