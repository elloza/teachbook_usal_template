# HTML Interactivo (sin frameworks)

Puedes crear elementos interactivos usando **HTML y JavaScript puro**, sin necesidad de React, Vue ni ningún framework. Todo el código va autocontenido en la propia página.

```{warning}
El contenido `{raw} html` **no aparece en PDF**. Añade siempre un bloque `{raw} latex` con texto alternativo para la versión impresa.
```

## Cuándo usar HTML interactivo

Usa HTML interactivo cuando necesites un comportamiento sencillo en la web: desplegables, pequeños controles, tablas con estilo o calculadoras autocontenidas. No hace falta añadir React, Vue ni ningún framework.

La directiva básica es:

````md
```{raw} html
<tu HTML aquí>
```
````

Todo lo que escribas dentro se inserta tal cual en la página web. Para que el libro siga funcionando en PDF, acompaña ese bloque de una alternativa `{raw} latex` con la información esencial.

## Pedir una visualización autocontenida a un chat

Una forma práctica de crear pequeños recursos interactivos es pedir a una herramienta como Gemini, Claude Code o ChatGPT que genere una visualización en **HTML autocontenido**. Esto significa que el resultado debe incluir en un único bloque todo lo necesario: HTML, CSS y JavaScript, sin archivos externos y sin frameworks.

Un prompt útil sería:

```text
Genera una visualización interactiva en HTML autocontenido para explicar mínimos cuadrados ordinarios (OLS).
Debe funcionar dentro de una página de Jupyter Book usando un bloque raw html.
Requisitos:
- No uses React, Vue, Angular, npm ni librerías externas.
- Incluye todo el CSS y JavaScript en el mismo bloque.
- Usa IDs únicos con el prefijo ols-demo- para evitar conflictos con otras partes de la página.
- No incluyas <!DOCTYPE html>, <html>, <head> ni <body>; solo el fragmento que se insertará dentro de la página.
- Añade controles para modificar pendiente e intercepto.
- Muestra los puntos, la recta de regresión, los residuos y la suma de errores al cuadrado.
- El código debe ser claro y fácil de pegar en un bloque ```{raw} html.
```

Después se pega el fragmento generado dentro de un bloque `{raw} html` y se añade una versión `{raw} latex` con la explicación esencial para el PDF. Por ejemplo:

```{raw} html
<style>
  .ols-demo-wrap {
    margin: 1.25rem 0;
    padding: 1rem;
    border: 1px solid #d8dee9;
    border-radius: 8px;
    background: #f8fafc;
    max-width: 760px;
  }
  .ols-demo-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: end;
    margin: 0.75rem 0;
  }
  .ols-demo-control {
    min-width: 180px;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  .ols-demo-control input {
    width: 100%;
  }
  .ols-demo-button {
    padding: 0.45rem 0.8rem;
    border: 0;
    border-radius: 4px;
    background: #0056b3;
    color: white;
    cursor: pointer;
  }
  .ols-demo-button:hover {
    background: #004494;
  }
  .ols-demo-metric {
    margin: 0.5rem 0;
    font-weight: 700;
    color: #b91c1c;
  }
  #ols-demo-plot {
    width: 100%;
    max-width: 640px;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    background: white;
  }
</style>

<div class="ols-demo-wrap">
  <p style="font-weight: 700; margin: 0 0 0.25rem;">Mínimos cuadrados ordinarios (OLS)</p>
  <p style="margin: 0;">Ajusta la recta y observa cómo cambian los residuos y la suma de errores al cuadrado.</p>

  <div class="ols-demo-controls">
    <label class="ols-demo-control" for="ols-demo-slope">
      Pendiente m: <span id="ols-demo-slope-val">1.00</span>
      <input type="range" id="ols-demo-slope" min="-1" max="1.5" step="0.01" value="0.65">
    </label>
    <label class="ols-demo-control" for="ols-demo-intercept">
      Intercepto b: <span id="ols-demo-intercept-val">50</span>
      <input type="range" id="ols-demo-intercept" min="0" max="220" step="1" value="55">
    </label>
    <button type="button" class="ols-demo-button" id="ols-demo-fit">Ajuste óptimo OLS</button>
  </div>

  <div class="ols-demo-metric">SSE: <span id="ols-demo-sse">0</span></div>
  <canvas id="ols-demo-plot" width="640" height="400" aria-label="Visualización interactiva de mínimos cuadrados ordinarios"></canvas>
</div>

<script>
(function () {
  const canvas = document.getElementById("ols-demo-plot");
  const ctx = canvas.getContext("2d");
  const slopeSlider = document.getElementById("ols-demo-slope");
  const interceptSlider = document.getElementById("ols-demo-intercept");
  const slopeVal = document.getElementById("ols-demo-slope-val");
  const interceptVal = document.getElementById("ols-demo-intercept-val");
  const sseVal = document.getElementById("ols-demo-sse");
  const fitButton = document.getElementById("ols-demo-fit");
  const data = [
    {x: 60, y: 110}, {x: 110, y: 150}, {x: 170, y: 160},
    {x: 220, y: 210}, {x: 290, y: 230}, {x: 350, y: 255},
    {x: 420, y: 300}, {x: 500, y: 315}, {x: 570, y: 350}
  ];

  function drawAxes() {
    ctx.strokeStyle = "#94a3b8";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(40, 20);
    ctx.lineTo(40, 370);
    ctx.lineTo(620, 370);
    ctx.stroke();
  }

  function draw() {
    const m = parseFloat(slopeSlider.value);
    const b = parseFloat(interceptSlider.value);
    let sse = 0;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawAxes();
    slopeVal.textContent = m.toFixed(2);
    interceptVal.textContent = b.toFixed(0);

    data.forEach(function (point) {
      const predicted = m * point.x + b;
      const actualY = canvas.height - point.y;
      const predictedY = canvas.height - predicted;
      const error = point.y - predicted;
      sse += error * error;

      ctx.setLineDash([5, 5]);
      ctx.strokeStyle = "rgba(185, 28, 28, 0.8)";
      ctx.beginPath();
      ctx.moveTo(point.x, actualY);
      ctx.lineTo(point.x, predictedY);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = "rgba(185, 28, 28, 0.12)";
      ctx.fillRect(point.x, Math.min(actualY, predictedY), Math.min(Math.abs(error), 70), Math.min(Math.abs(error), 70));
    });

    ctx.strokeStyle = "#0056b3";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(40, canvas.height - (m * 40 + b));
    ctx.lineTo(620, canvas.height - (m * 620 + b));
    ctx.stroke();

    data.forEach(function (point) {
      ctx.fillStyle = "#111827";
      ctx.beginPath();
      ctx.arc(point.x, canvas.height - point.y, 5, 0, Math.PI * 2);
      ctx.fill();
    });

    sseVal.textContent = sse.toFixed(0);
  }

  function calculateOLS() {
    const n = data.length;
    let sumX = 0, sumY = 0, sumXY = 0, sumXX = 0;
    data.forEach(function (p) {
      sumX += p.x;
      sumY += p.y;
      sumXY += p.x * p.y;
      sumXX += p.x * p.x;
    });
    const m = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const b = (sumY - m * sumX) / n;
    slopeSlider.value = m;
    interceptSlider.value = b;
    draw();
  }

  slopeSlider.addEventListener("input", draw);
  interceptSlider.addEventListener("input", draw);
  fitButton.addEventListener("click", calculateOLS);
  draw();
}());
</script>
```

```{raw} latex
\textbf{Visualización OLS:} En la versión HTML, el lector puede modificar la pendiente y el intercepto de una recta, observar los residuos entre los puntos y la predicción, y ver cómo cambia la suma de errores al cuadrado. El botón de ajuste óptimo calcula la recta de mínimos cuadrados ordinarios.
```

## Contenido colapsable con `<details>`

```{raw} html
<details>
  <summary style="cursor: pointer; font-weight: bold; color: #2563eb; padding: 0.5em 0;">
    Haz clic para ver la pista
  </summary>
  <div style="padding: 1em; border-left: 3px solid #2563eb; margin-top: 0.5em; background: #f0f7ff;">
    Recuerda que la derivada de $e^x$ es $e^x$.
  </div>
</details>
```

```{raw} latex
\textbf{Pista:} Recuerda que la derivada de $e^x$ es $e^x$.
```

## Slider con valor en tiempo real

```{raw} html
<div style="margin: 1em 0; padding: 1em; border: 1px solid #e5e7eb; border-radius: 8px; background: #f9fafb;">
  <label for="temp-slider" style="font-weight: bold;">Temperatura (°C):</label>
  <input type="range" id="temp-slider" min="-50" max="50" value="20"
    style="width: 60%; margin: 0.5em 0;"
    oninput="document.getElementById('temp-val').textContent = this.value;
             document.getElementById('temp-fahr').textContent = (this.value * 9/5 + 32).toFixed(1);">
  <div style="font-size: 1.2em; margin-top: 0.5em;">
    <span id="temp-val" style="font-weight: bold; color: #2563eb;">20</span> °C =
    <span id="temp-fahr" style="font-weight: bold; color: #dc2626;">68.0</span> °F
  </div>
</div>
```

```{raw} latex
\textbf{Conversor de temperatura:} $T_{\text{°F}} = T_{\text{°C}} \times \frac{9}{5} + 32$
```

## Calculadora simple

```{raw} html
<div style="margin: 1em 0; padding: 1em; border: 1px solid #e5e7eb; border-radius: 8px; background: #f9fafb;">
  <p style="font-weight: bold; margin-bottom: 0.5em;">Calculadora de ley de Ohm: V = I × R</p>
  <div style="display: flex; gap: 1em; flex-wrap: wrap; align-items: center;">
    <div>
      <label>Corriente I (A):</label><br>
      <input type="number" id="ohm-i" value="2" step="0.1" min="0" style="width: 100px; padding: 4px;">
    </div>
    <div>
      <label>Resistencia R (Ω):</label><br>
      <input type="number" id="ohm-r" value="10" step="1" min="0" style="width: 100px; padding: 4px;">
    </div>
    <div>
      <button onclick="
        var i = parseFloat(document.getElementById('ohm-i').value) || 0;
        var r = parseFloat(document.getElementById('ohm-r').value) || 0;
        document.getElementById('ohm-result').textContent = (i * r).toFixed(2);
      " style="padding: 6px 16px; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer; margin-top: 1.2em;">
        Calcular V
      </button>
    </div>
    <div>
      <label>Voltaje (V):</label><br>
      <span id="ohm-result" style="font-size: 1.3em; font-weight: bold; color: #16a34a;">20.00</span> V
    </div>
  </div>
</div>
```

```{raw} latex
\textbf{Calculadora de ley de Ohm:} $V = I \times R$
```

```{admonition} Reglas para HTML interactivo
:class: important

1. **Sin frameworks JS**: no uses React, Vue, Angular ni npm.
2. **Sin archivos externos**: todo el JS va inline dentro del bloque `{raw} html`.
3. **Siempre con fallback LaTeX**: añade un bloque `{raw} latex` con el contenido esencial para el PDF.
4. **Estilos inline**: usa `style=""` en las etiquetas para no depender de CSS externo.
```
