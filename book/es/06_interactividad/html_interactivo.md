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
