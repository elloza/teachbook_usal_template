# Interactive Periodic Table

The interactive table below summarizes a teaching selection of representative elements. It is not intended to be a complete database; it is a fast way to compare properties and chemical families during an explanation.

The values and categories in a teaching periodic table should be treated as a gateway to evaluated data. IUPAC keeps its periodic table updated with abridged standard atomic weights recommended by CIAAW {cite:p}`iupac_periodic_table_2022`.

A useful qualitative reading is that many trends increase with effective nuclear charge:

$$
Z_{\mathrm{eff}} \uparrow \quad \Longrightarrow \quad E_{\mathrm{ion}} \uparrow \ \text{and}\ r_{\mathrm{at}} \downarrow
$$

**Interactive table. Basic properties of selected elements.**

```{raw} html
<div class="periodic-tool" id="periodic-tool-en">
  <div class="periodic-controls">
    <label>Family
      <select id="periodic-family-en">
        <option value="all">All</option>
        <option value="alkali">Alkali metals</option>
        <option value="alkaline">Alkaline earth metals</option>
        <option value="nonmetal">Nonmetals</option>
        <option value="metalloid">Metalloids</option>
        <option value="halogen">Halogens</option>
        <option value="noble">Noble gases</option>
        <option value="transition">Transition metals</option>
      </select>
    </label>
    <label>Property
      <select id="periodic-property-en">
        <option value="electronegativity">Electronegativity</option>
        <option value="atomicRadius">Atomic radius (pm)</option>
        <option value="ionization">Ionization energy (kJ/mol)</option>
      </select>
    </label>
  </div>
  <div class="periodic-grid" id="periodic-grid-en"></div>
  <div class="periodic-detail" id="periodic-detail-en"></div>
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
    {symbol:"H", name:"Hydrogen", family:"nonmetal", atomicNumber:1, electronegativity:2.20, atomicRadius:53, ionization:1312},
    {symbol:"Li", name:"Lithium", family:"alkali", atomicNumber:3, electronegativity:0.98, atomicRadius:167, ionization:520},
    {symbol:"Be", name:"Beryllium", family:"alkaline", atomicNumber:4, electronegativity:1.57, atomicRadius:112, ionization:900},
    {symbol:"C", name:"Carbon", family:"nonmetal", atomicNumber:6, electronegativity:2.55, atomicRadius:67, ionization:1087},
    {symbol:"N", name:"Nitrogen", family:"nonmetal", atomicNumber:7, electronegativity:3.04, atomicRadius:56, ionization:1402},
    {symbol:"O", name:"Oxygen", family:"nonmetal", atomicNumber:8, electronegativity:3.44, atomicRadius:48, ionization:1314},
    {symbol:"F", name:"Fluorine", family:"halogen", atomicNumber:9, electronegativity:3.98, atomicRadius:42, ionization:1681},
    {symbol:"Ne", name:"Neon", family:"noble", atomicNumber:10, electronegativity:null, atomicRadius:38, ionization:2081},
    {symbol:"Na", name:"Sodium", family:"alkali", atomicNumber:11, electronegativity:0.93, atomicRadius:190, ionization:496},
    {symbol:"Mg", name:"Magnesium", family:"alkaline", atomicNumber:12, electronegativity:1.31, atomicRadius:145, ionization:738},
    {symbol:"Si", name:"Silicon", family:"metalloid", atomicNumber:14, electronegativity:1.90, atomicRadius:111, ionization:787},
    {symbol:"Cl", name:"Chlorine", family:"halogen", atomicNumber:17, electronegativity:3.16, atomicRadius:79, ionization:1251},
    {symbol:"Ar", name:"Argon", family:"noble", atomicNumber:18, electronegativity:null, atomicRadius:71, ionization:1521},
    {symbol:"Fe", name:"Iron", family:"transition", atomicNumber:26, electronegativity:1.83, atomicRadius:156, ionization:762},
    {symbol:"Cu", name:"Copper", family:"transition", atomicNumber:29, electronegativity:1.90, atomicRadius:145, ionization:746},
    {symbol:"Zn", name:"Zinc", family:"transition", atomicNumber:30, electronegativity:1.65, atomicRadius:142, ionization:906}
  ];
  const familyNames = {alkali:"Alkali metals", alkaline:"Alkaline earth metals", nonmetal:"Nonmetals", metalloid:"Metalloids", halogen:"Halogens", noble:"Noble gases", transition:"Transition metals"};
  const labels = {electronegativity:"Electronegativity", atomicRadius:"Atomic radius", ionization:"Ionization energy"};
  const units = {electronegativity:"", atomicRadius:" pm", ionization:" kJ/mol"};
  const grid = document.getElementById("periodic-grid-en");
  const family = document.getElementById("periodic-family-en");
  const property = document.getElementById("periodic-property-en");
  const detail = document.getElementById("periodic-detail-en");
  let selected = elements[0];
  function fmt(value){ return value === null ? "not defined" : value; }
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
    detail.innerHTML = `<strong>${selected.name} (${selected.symbol})</strong><br>Family: ${familyNames[selected.family]}. ${labels[prop]}: ${fmt(selected[prop])}${selected[prop] === null ? "" : units[prop]}.`;
  }
  family.addEventListener("change", render);
  property.addEventListener("change", render);
  render();
})();
</script>
```

```{raw} latex
\begin{center}
\textbf{Interactive periodic table:} see the HTML version to filter elements and compare properties. This page uses a teaching selection of representative elements.
\end{center}
```

The interactive table makes trends quick to compare: alkali metals have low ionization energies, halogens have high electronegativities, and noble gases usually have no defined electronegativity on this scale.

## Activity

Select electronegativity and compare sodium, chlorine, and argon. Then explain why NaCl is interpreted very differently from a covalent molecule such as HCl.

```{admonition} Guided reading
:class: dropdown
Compare sodium, magnesium, and chlorine using ionization energy and electronegativity. The goal is not to memorize values, but to recognize patterns across groups and periods.
```
