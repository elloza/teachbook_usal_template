# Interactive IR Spectrum

An infrared spectrum links absorption bands with functional groups. The tool below is a teaching simulation: when a functional group is enabled, approximate bands are shown in the regions where they commonly appear.

Real spectra should be checked against evaluated databases. The NIST Chemistry WebBook includes IR spectra for thousands of compounds as well as thermochemical and spectroscopic data {cite:p}`nist_chemistry_webbook_srd69`.

The horizontal axis uses wavenumber:

$$
\tilde{\nu} = \frac{1}{\lambda}
$$

**Interactive figure. Approximate IR bands by functional group.**

```{raw} html
<div class="ir-tool" id="ir-tool-en">
  <div class="ir-checks">
    <label><input type="checkbox" value="oh" checked> O-H alcohol/phenol</label>
    <label><input type="checkbox" value="ch" checked> Aliphatic C-H</label>
    <label><input type="checkbox" value="co"> C=O carbonyl</label>
    <label><input type="checkbox" value="cn"> C≡N nitrile</label>
    <label><input type="checkbox" value="cc"> Aromatic C=C</label>
  </div>
  <svg id="ir-svg-en" viewBox="0 0 900 360" role="img" aria-label="Simulated IR spectrum"></svg>
  <p id="ir-note-en" class="ir-note"></p>
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
    oh: {label:"broad O-H", center:3350, width:230, depth:42},
    ch: {label:"C-H", center:2950, width:90, depth:24},
    co: {label:"C=O", center:1715, width:55, depth:48},
    cn: {label:"C≡N", center:2250, width:45, depth:35},
    cc: {label:"aromatic C=C", center:1600, width:60, depth:25}
  };
  const svg = document.getElementById("ir-svg-en");
  const note = document.getElementById("ir-note-en");
  const checks = Array.from(document.querySelectorAll("#ir-tool-en input"));
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
      <text x="365" y="340" font-size="18">Wavenumber (cm⁻¹)</text>
      <text x="18" y="185" font-size="16" transform="rotate(-90 18 185)">Transmittance</text>
      ${[4000,3500,3000,2500,2000,1500,1000,500].map(nu => `<line x1="${xFromWavenumber(nu)}" y1="300" x2="${xFromWavenumber(nu)}" y2="306" stroke="#24292f"/><text x="${xFromWavenumber(nu)-18}" y="324" font-size="13">${nu}</text>`).join("")}
      <polyline points="${points.join(" ")}" fill="none" stroke="#0969da" stroke-width="3"/>
      ${active.map(key => {
        const b = bands[key], x = xFromWavenumber(b.center);
        return `<line x1="${x}" y1="55" x2="${x}" y2="300" stroke="#cf222e" stroke-dasharray="4 4"/><text x="${x+5}" y="70" font-size="13">${b.label}</text>`;
      }).join("")}
    `;
    note.textContent = active.length ? "Active bands: " + active.map(k => bands[k].label + " (" + bands[k].center + " cm⁻¹)").join(", ") + "." : "Enable at least one functional group to build the spectrum.";
  }
  checks.forEach(c => c.addEventListener("change", render));
  render();
})();
</script>
```

```{raw} latex
\begin{center}
\textbf{Interactive IR spectrum:} see the HTML version to enable functional groups. Typical bands: O--H 3200--3600 cm$^{-1}$, C--H 2850--3000 cm$^{-1}$, C=O 1650--1750 cm$^{-1}$, C$\equiv$N 2210--2260 cm$^{-1}$.
\end{center}
```

The interactive figure helps separate two ideas: band position gives information about the bond, but width and intensity also depend on chemical environment and sample conditions.

```{admonition} Guided activity
:class: dropdown
Enable O-H and C=O at the same time. Then disable O-H and observe how the broad high-frequency band disappears. That width is often as informative as the peak position.
```
