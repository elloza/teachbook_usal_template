# Tabla periódica interactiva

La tabla interactiva siguiente resume una selección docente de elementos representativos. No pretende ser una base de datos completa, sino una forma rápida de comparar propiedades y familias químicas durante una explicación.

Los valores y categorías de una tabla periódica docente deben entenderse como una puerta de entrada a datos evaluados. IUPAC mantiene la tabla periódica actualizada con los pesos atómicos abreviados recomendados por CIAAW {cite:p}`iupac_periodic_table_2022`.

Una lectura cualitativa útil es pensar que muchas tendencias aumentan con la carga nuclear efectiva:

$$
Z_{\mathrm{eff}} \uparrow \quad \Longrightarrow \quad E_{\mathrm{ion}} \uparrow \ \text{y}\ r_{\mathrm{at}} \downarrow
$$

**Tabla interactiva. Propiedades básicas de elementos seleccionados.**

```{raw} html
<div class="periodic-tool" id="periodic-tool-es">
  <div class="periodic-controls">
    <label>Familia
      <select id="periodic-family-es">
        <option value="all">Todas</option>
        <option value="alkali">Alcalinos</option>
        <option value="alkaline">Alcalinotérreos</option>
        <option value="nonmetal">No metales</option>
        <option value="metalloid">Metaloides</option>
        <option value="halogen">Halógenos</option>
        <option value="noble">Gases nobles</option>
        <option value="transition">Transición</option>
      </select>
    </label>
    <label>Propiedad
      <select id="periodic-property-es">
        <option value="electronegativity">Electronegatividad</option>
        <option value="atomicRadius">Radio atómico (pm)</option>
        <option value="ionization">Energía de ionización (kJ/mol)</option>
      </select>
    </label>
  </div>
  <div class="periodic-grid" id="periodic-grid-es"></div>
  <div class="periodic-detail" id="periodic-detail-es"></div>
</div>
<style>
.periodic-tool{border:1px solid #d0d7de;border-radius:8px;padding:1rem;margin:1rem 0;background:#fff}
.periodic-controls{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem}
.periodic-controls label{font-weight:600}
.periodic-controls select{margin-left:.4rem;padding:.25rem .4rem}
.periodic-grid{display:grid;grid-template-columns:repeat(8,minmax(4.8rem,1fr));gap:.4rem}
.periodic-card{border:1px solid #c9d1d9;border-radius:6px;padding:.45rem;background:#f6f8fa;cursor:pointer;min-height:4.6rem;text-align:left}
.periodic-card strong{font-size:1.15rem;display:block}
.periodic-card span{font-size:.78rem;display:block}
.periodic-card.active{outline:3px solid #0969da;background:#ddf4ff}
.periodic-card.dimmed{opacity:.32}
.periodic-detail{margin-top:1rem;padding:.8rem;border-left:4px solid #0969da;background:#f6f8fa}
@media (max-width:700px){.periodic-grid{grid-template-columns:repeat(3,1fr)}}
</style>
<script>
(function(){
  const elements = [
    {symbol:"H", name:"Hidrógeno", family:"nonmetal", atomicNumber:1, electronegativity:2.20, atomicRadius:53, ionization:1312},
    {symbol:"Li", name:"Litio", family:"alkali", atomicNumber:3, electronegativity:0.98, atomicRadius:167, ionization:520},
    {symbol:"Be", name:"Berilio", family:"alkaline", atomicNumber:4, electronegativity:1.57, atomicRadius:112, ionization:900},
    {symbol:"C", name:"Carbono", family:"nonmetal", atomicNumber:6, electronegativity:2.55, atomicRadius:67, ionization:1087},
    {symbol:"N", name:"Nitrógeno", family:"nonmetal", atomicNumber:7, electronegativity:3.04, atomicRadius:56, ionization:1402},
    {symbol:"O", name:"Oxígeno", family:"nonmetal", atomicNumber:8, electronegativity:3.44, atomicRadius:48, ionization:1314},
    {symbol:"F", name:"Flúor", family:"halogen", atomicNumber:9, electronegativity:3.98, atomicRadius:42, ionization:1681},
    {symbol:"Ne", name:"Neón", family:"noble", atomicNumber:10, electronegativity:null, atomicRadius:38, ionization:2081},
    {symbol:"Na", name:"Sodio", family:"alkali", atomicNumber:11, electronegativity:0.93, atomicRadius:190, ionization:496},
    {symbol:"Mg", name:"Magnesio", family:"alkaline", atomicNumber:12, electronegativity:1.31, atomicRadius:145, ionization:738},
    {symbol:"Si", name:"Silicio", family:"metalloid", atomicNumber:14, electronegativity:1.90, atomicRadius:111, ionization:787},
    {symbol:"Cl", name:"Cloro", family:"halogen", atomicNumber:17, electronegativity:3.16, atomicRadius:79, ionization:1251},
    {symbol:"Ar", name:"Argón", family:"noble", atomicNumber:18, electronegativity:null, atomicRadius:71, ionization:1521},
    {symbol:"Fe", name:"Hierro", family:"transition", atomicNumber:26, electronegativity:1.83, atomicRadius:156, ionization:762},
    {symbol:"Cu", name:"Cobre", family:"transition", atomicNumber:29, electronegativity:1.90, atomicRadius:145, ionization:746},
    {symbol:"Zn", name:"Zinc", family:"transition", atomicNumber:30, electronegativity:1.65, atomicRadius:142, ionization:906}
  ];
  const familyNames = {alkali:"Alcalinos", alkaline:"Alcalinotérreos", nonmetal:"No metales", metalloid:"Metaloides", halogen:"Halógenos", noble:"Gases nobles", transition:"Transición"};
  const labels = {electronegativity:"Electronegatividad", atomicRadius:"Radio atómico", ionization:"Energía de ionización"};
  const units = {electronegativity:"", atomicRadius:" pm", ionization:" kJ/mol"};
  const grid = document.getElementById("periodic-grid-es");
  const family = document.getElementById("periodic-family-es");
  const property = document.getElementById("periodic-property-es");
  const detail = document.getElementById("periodic-detail-es");
  let selected = elements[0];
  function fmt(value){ return value === null ? "no definida" : value; }
  function render(){
    const fam = family.value;
    const prop = property.value;
    grid.innerHTML = "";
    elements.forEach(el => {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "periodic-card";
      if (fam !== "all" && el.family !== fam) card.classList.add("dimmed");
      if (selected.symbol === el.symbol) card.classList.add("active");
      card.innerHTML = `<strong>${el.symbol}</strong><span>${el.atomicNumber}. ${el.name}</span><span>${fmt(el[prop])}${el[prop] === null ? "" : units[prop]}</span>`;
      card.addEventListener("click", () => { selected = el; render(); });
      grid.appendChild(card);
    });
    detail.innerHTML = `<strong>${selected.name} (${selected.symbol})</strong><br>Familia: ${familyNames[selected.family]}. ${labels[prop]}: ${fmt(selected[prop])}${selected[prop] === null ? "" : units[prop]}.`;
  }
  family.addEventListener("change", render);
  property.addEventListener("change", render);
  render();
})();
</script>
```

```{raw} latex
\begin{center}
\textbf{Tabla periódica interactiva:} consulte la versión HTML para filtrar elementos y comparar propiedades. En esta página se trabaja con una selección docente de elementos representativos.
\end{center}
```

La tabla interactiva permite comparar rápidamente tendencias: los alcalinos muestran baja energía de ionización, los halógenos tienen electronegatividades altas y los gases nobles no suelen tener electronegatividad definida en esta escala.

## Actividad

Selecciona la electronegatividad y compara sodio, cloro y argón. Después explica por qué NaCl se interpreta de forma muy distinta a una molécula covalente como HCl.

```{admonition} Lectura guiada
:class: dropdown
Compara sodio, magnesio y cloro usando energía de ionización y electronegatividad. El objetivo no es memorizar valores, sino reconocer patrones por grupos y periodos.
```
