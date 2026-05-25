# Espectro IR interactivo

Un espectro infrarrojo permite relacionar bandas de absorción con grupos funcionales. La herramienta siguiente es una simulación didáctica: al activar un grupo funcional se muestran bandas aproximadas en las regiones donde suelen aparecer.

Para contrastar espectros reales conviene usar bases de datos evaluadas. El NIST Chemistry WebBook incluye espectros IR de miles de compuestos y otros datos termoquímicos y espectroscópicos {cite:p}`nist_chemistry_webbook_srd69`.

El eje horizontal usa número de onda:

$$
\tilde{\nu} = \frac{1}{\lambda}
$$

**Figura interactiva. Bandas IR aproximadas por grupo funcional.**

```{raw} html
<div class="ir-tool" id="ir-tool-es">
  <div class="ir-checks">
    <label><input type="checkbox" value="oh" checked> O-H alcohol/fenol</label>
    <label><input type="checkbox" value="ch" checked> C-H alifático</label>
    <label><input type="checkbox" value="co"> C=O carbonilo</label>
    <label><input type="checkbox" value="cn"> C≡N nitrilo</label>
    <label><input type="checkbox" value="cc"> C=C aromático</label>
  </div>
  <svg id="ir-svg-es" viewBox="0 0 900 360" role="img" aria-label="Espectro IR simulado"></svg>
  <p id="ir-note-es" class="ir-note"></p>
</div>
<style>
.ir-tool{border:1px solid #d0d7de;border-radius:8px;padding:1rem;background:#fff;margin:1rem 0}
.ir-checks{display:flex;flex-wrap:wrap;gap:.9rem;margin-bottom:.7rem}
.ir-checks label{font-weight:600}
.ir-tool svg{width:100%;height:auto;border:1px solid #d8dee4;background:#fff}
.ir-note{background:#f6f8fa;border-left:4px solid #8250df;padding:.7rem;margin-bottom:0}
</style>
<script>
(function(){
  const bands = {
    oh: {label:"O-H ancho", center:3350, width:230, depth:42},
    ch: {label:"C-H", center:2950, width:90, depth:24},
    co: {label:"C=O", center:1715, width:55, depth:48},
    cn: {label:"C≡N", center:2250, width:45, depth:35},
    cc: {label:"C=C aromático", center:1600, width:60, depth:25}
  };
  const svg = document.getElementById("ir-svg-es");
  const note = document.getElementById("ir-note-es");
  const checks = Array.from(document.querySelectorAll("#ir-tool-es input"));
  function xFromWavenumber(nu){ return 60 + (4000 - nu) / (4000 - 500) * 780; }
  function yAt(nu, active){
    let trans = 92;
    active.forEach(key => {
      const b = bands[key];
      trans -= b.depth * Math.exp(-0.5 * Math.pow((nu - b.center) / b.width, 2));
    });
    return 40 + (100 - trans) * 2.6;
  }
  function render(){
    const active = checks.filter(c => c.checked).map(c => c.value);
    let points = [];
    for(let i=0;i<=360;i++){
      const nu = 4000 - i * (3500/360);
      points.push(`${xFromWavenumber(nu).toFixed(1)},${yAt(nu, active).toFixed(1)}`);
    }
    svg.innerHTML = `
      <line x1="60" y1="300" x2="840" y2="300" stroke="#24292f"/>
      <line x1="60" y1="40" x2="60" y2="300" stroke="#24292f"/>
      <text x="370" y="340" font-size="18">Número de onda (cm⁻¹)</text>
      <text x="18" y="185" font-size="16" transform="rotate(-90 18 185)">Transmitancia</text>
      ${[4000,3500,3000,2500,2000,1500,1000,500].map(nu => `<line x1="${xFromWavenumber(nu)}" y1="300" x2="${xFromWavenumber(nu)}" y2="306" stroke="#24292f"/><text x="${xFromWavenumber(nu)-18}" y="324" font-size="13">${nu}</text>`).join("")}
      <polyline points="${points.join(" ")}" fill="none" stroke="#0969da" stroke-width="3"/>
      ${active.map(key => {
        const b = bands[key], x = xFromWavenumber(b.center);
        return `<line x1="${x}" y1="55" x2="${x}" y2="300" stroke="#cf222e" stroke-dasharray="4 4"/><text x="${x+5}" y="70" font-size="13">${b.label}</text>`;
      }).join("")}
    `;
    note.textContent = active.length ? "Bandas activas: " + active.map(k => bands[k].label + " (" + bands[k].center + " cm⁻¹)").join(", ") + "." : "Activa al menos un grupo funcional para construir el espectro.";
  }
  checks.forEach(c => c.addEventListener("change", render));
  render();
})();
</script>
```

```{raw} latex
\begin{center}
\textbf{Espectro IR interactivo:} consulte la versión HTML para activar grupos funcionales. Bandas orientativas: O--H 3200--3600 cm$^{-1}$, C--H 2850--3000 cm$^{-1}$, C=O 1650--1750 cm$^{-1}$, C$\equiv$N 2210--2260 cm$^{-1}$.
\end{center}
```

La figura interactiva ayuda a separar dos ideas: la posición de una banda orienta sobre el enlace, pero la anchura e intensidad también dependen del entorno químico y de la muestra.

```{admonition} Actividad guiada
:class: dropdown
Activa O-H y C=O a la vez. Después desactiva O-H y observa cómo desaparece la banda ancha de alta frecuencia. Esa anchura suele ser tan informativa como la posición del máximo.
```
