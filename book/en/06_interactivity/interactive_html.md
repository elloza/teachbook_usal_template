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
