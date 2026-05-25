# Interactive HTML (no frameworks)

You can create interactive elements using **plain HTML and JavaScript**, without React, Vue, or any framework. All code is self-contained on the page itself.

```{warning}
Content in `{raw} html` blocks does **not appear in PDF**. Always add a `{raw} latex` block with alternative text for the printed version.
```

## When to use interactive HTML

Use interactive HTML when you need simple behavior on the web: dropdowns, small controls, styled tables, or self-contained calculators. You do not need React, Vue, or any framework.

The basic directive is:

````md
```{raw} html
<your HTML here>
```
````

Everything you write inside is inserted as-is into the web page. To keep the book working in PDF, pair that block with a `{raw} latex` alternative containing the essential information.

## Asking a chat tool for a self-contained visualization

A practical way to create small interactive resources is to ask a tool such as Gemini, Claude Code, or ChatGPT to generate a **self-contained HTML** visualization. This means that the result must include everything in one block: HTML, CSS, and JavaScript, with no external files and no frameworks.

A useful prompt would be:

```text
Generate a self-contained interactive HTML visualization to explain ordinary least squares (OLS).
It must work inside a Jupyter Book page using a raw html block.
Requirements:
- Do not use React, Vue, Angular, npm, or external libraries.
- Include all CSS and JavaScript in the same block.
- Use unique IDs with the prefix ols-demo-en- to avoid conflicts with other parts of the page.
- Do not include <!DOCTYPE html>, <html>, <head>, or <body>; only the fragment that will be inserted into the page.
- Add controls to change slope and intercept.
- Show the points, regression line, residuals, and sum of squared errors.
- The code must be clear and easy to paste into a ```{raw} html block.
```

Then paste the generated fragment inside a `{raw} html` block and add a `{raw} latex` version with the essential explanation for PDF. For example:

```{raw} html
<style>
  .ols-demo-en-wrap {
    margin: 1.25rem 0;
    padding: 1rem;
    border: 1px solid #d8dee9;
    border-radius: 8px;
    background: #f8fafc;
    max-width: 760px;
  }
  .ols-demo-en-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: end;
    margin: 0.75rem 0;
  }
  .ols-demo-en-control {
    min-width: 180px;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  .ols-demo-en-control input {
    width: 100%;
  }
  .ols-demo-en-button {
    padding: 0.45rem 0.8rem;
    border: 0;
    border-radius: 4px;
    background: #0056b3;
    color: white;
    cursor: pointer;
  }
  .ols-demo-en-button:hover {
    background: #004494;
  }
  .ols-demo-en-metric {
    margin: 0.5rem 0;
    font-weight: 700;
    color: #b91c1c;
  }
  #ols-demo-en-plot {
    width: 100%;
    max-width: 640px;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    background: white;
  }
</style>

<div class="ols-demo-en-wrap">
  <p style="font-weight: 700; margin: 0 0 0.25rem;">Ordinary least squares (OLS)</p>
  <p style="margin: 0;">Adjust the line and watch how the residuals and the sum of squared errors change.</p>

  <div class="ols-demo-en-controls">
    <label class="ols-demo-en-control" for="ols-demo-en-slope">
      Slope m: <span id="ols-demo-en-slope-val">1.00</span>
      <input type="range" id="ols-demo-en-slope" min="-1" max="1.5" step="0.01" value="0.65">
    </label>
    <label class="ols-demo-en-control" for="ols-demo-en-intercept">
      Intercept b: <span id="ols-demo-en-intercept-val">50</span>
      <input type="range" id="ols-demo-en-intercept" min="0" max="220" step="1" value="55">
    </label>
    <button type="button" class="ols-demo-en-button" id="ols-demo-en-fit">Optimal OLS fit</button>
  </div>

  <div class="ols-demo-en-metric">SSE: <span id="ols-demo-en-sse">0</span></div>
  <canvas id="ols-demo-en-plot" width="640" height="400" aria-label="Interactive ordinary least squares visualization"></canvas>
</div>

<script>
(function () {
  const canvas = document.getElementById("ols-demo-en-plot");
  const ctx = canvas.getContext("2d");
  const slopeSlider = document.getElementById("ols-demo-en-slope");
  const interceptSlider = document.getElementById("ols-demo-en-intercept");
  const slopeVal = document.getElementById("ols-demo-en-slope-val");
  const interceptVal = document.getElementById("ols-demo-en-intercept-val");
  const sseVal = document.getElementById("ols-demo-en-sse");
  const fitButton = document.getElementById("ols-demo-en-fit");
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
\textbf{OLS visualization:} In the HTML version, the reader can change the slope and intercept of a line, observe the residuals between the points and the prediction, and see how the sum of squared errors changes. The optimal fit button computes the ordinary least squares line.
```

## Collapsible content with `<details>`

```{raw} html
<details>
  <summary style="cursor: pointer; font-weight: bold; color: #2563eb; padding: 0.5em 0;">
    Click to reveal the hint
  </summary>
  <div style="padding: 1em; border-left: 3px solid #2563eb; margin-top: 0.5em; background: #f0f7ff;">
    Remember that the derivative of $e^x$ is $e^x$.
  </div>
</details>
```

```{raw} latex
\textbf{Hint:} Remember that the derivative of $e^x$ is $e^x$.
```

## Slider with live output

```{raw} html
<div style="margin: 1em 0; padding: 1em; border: 1px solid #e5e7eb; border-radius: 8px; background: #f9fafb;">
  <label for="temp-slider" style="font-weight: bold;">Temperature (°C):</label>
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
\textbf{Temperature converter:} $T_{\text{°F}} = T_{\text{°C}} \times \frac{9}{5} + 32$
```

## Simple calculator

```{raw} html
<div style="margin: 1em 0; padding: 1em; border: 1px solid #e5e7eb; border-radius: 8px; background: #f9fafb;">
  <p style="font-weight: bold; margin-bottom: 0.5em;">Ohm's Law calculator: V = I × R</p>
  <div style="display: flex; gap: 1em; flex-wrap: wrap; align-items: center;">
    <div>
      <label>Current I (A):</label><br>
      <input type="number" id="ohm-i" value="2" step="0.1" min="0" style="width: 100px; padding: 4px;">
    </div>
    <div>
      <label>Resistance R (Ω):</label><br>
      <input type="number" id="ohm-r" value="10" step="1" min="0" style="width: 100px; padding: 4px;">
    </div>
    <div>
      <button onclick="
        var i = parseFloat(document.getElementById('ohm-i').value) || 0;
        var r = parseFloat(document.getElementById('ohm-r').value) || 0;
        document.getElementById('ohm-result').textContent = (i * r).toFixed(2);
      " style="padding: 6px 16px; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer; margin-top: 1.2em;">
        Calculate V
      </button>
    </div>
    <div>
      <label>Voltage (V):</label><br>
      <span id="ohm-result" style="font-size: 1.3em; font-weight: bold; color: #16a34a;">20.00</span> V
    </div>
  </div>
</div>
```

```{raw} latex
\textbf{Ohm's Law calculator:} $V = I \times R$
```

```{admonition} Rules for interactive HTML
:class: important

1. **No JS frameworks**: do not use React, Vue, Angular, or npm.
2. **No external files**: all JS goes inline inside the `{raw} html` block.
3. **Always include LaTeX fallback**: add a `{raw} latex` block with essential content for PDF.
4. **Inline styles**: use `style=""` on tags to avoid depending on external CSS.
```
