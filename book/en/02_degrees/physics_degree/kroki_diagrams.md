# Technical Diagrams with Kroki for Physics

Kroki is useful for **block diagrams, signal flow, timing diagrams, and conceptual schematics**. For **electrical circuits with standard symbols**, the recommended tool is **CircuitikZ rendered as an image**.

## When to use each tool

- **Use Kroki** for conceptual explanations, functional blocks, timing, instrumentation, and signal flow.
- **Use WaveDrom through Kroki** for digital signals, buses, clocks, and timing protocols.
- **Use CircuitikZ** for resistors, capacitors, sources, switches, and formal electrical schematics.
- **Use SchemDraw** when you want to build simple circuits from Python inside a notebook.

## 1. Mermaid: instrumentation chain


As shown in {numref}`fig-diagram-02-degrees-physics-degree-kroki-diagrams-01`, the diagram is versioned as a static image.

```{figure} ../../../_static/generated/diagrams/en/02_degrees_physics_degree_kroki_diagrams_01.svg
:name: fig-diagram-02-degrees-physics-degree-kroki-diagrams-01
:alt: Diagram: Mermaid: instrumentation chain
:width: 90%
:align: center

Diagram: Mermaid: instrumentation chain.
```
As shown in {numref}`fig-diagram-02-degrees-physics-degree-kroki-diagrams-02`, the diagram is versioned as a static image.

```{figure} ../../../_static/generated/diagrams/en/02_degrees_physics_degree_kroki_diagrams_02.svg
:name: fig-diagram-02-degrees-physics-degree-kroki-diagrams-02
:alt: Diagram: GraphViz: signal flow in an experimental setup
:width: 90%
:align: center

Diagram: GraphViz: signal flow in an experimental setup.
```


The {numref}`fig-kroki-diagrams-3` visually summarizes this part of the explanation.

```{figure} ../../../_static/generated/rc_circuit_circuitikz.png
:alt: RC circuit generated with CircuitikZ
:width: 70%
:align: center
:name: fig-kroki-diagrams-3

RC circuit generated from CircuitikZ code.
```

```tex
\begin{circuitikz}
\draw
  (0,0) to[V, l=$5\,\mathrm{V}$] (0,3)
  to[R, l=$R_1$] (3,3)
  to[C, l=$20\,\mu\mathrm{F}$] (3,0)
  -- (0,0);
\end{circuitikz}
```

```{admonition} Important
:class: warning
Kroki supports TikZ, but the public Kroki service does not guarantee that the `circuitikz` package is available. For robust teaching circuits, this project renders CircuitikZ locally as an image.
```

## 4. Wavedrom: input and output signals


As shown in {numref}`fig-diagram-02-degrees-physics-degree-kroki-diagrams-03`, the diagram is versioned as a static image.

```{figure} ../../../_static/generated/diagrams/en/02_degrees_physics_degree_kroki_diagrams_03.svg
:name: fig-diagram-02-degrees-physics-degree-kroki-diagrams-03
:alt: Diagram: Wavedrom: input and output signals
:width: 90%
:align: center

Diagram: Wavedrom: input and output signals.
```
As shown in {numref}`fig-diagram-02-degrees-physics-degree-kroki-diagrams-04`, the diagram is versioned as a static image.

```{figure} ../../../_static/generated/diagrams/en/02_degrees_physics_degree_kroki_diagrams_04.svg
:name: fig-diagram-02-degrees-physics-degree-kroki-diagrams-04
:alt: Diagram: Ditaa: quick experimental bench sketch
:width: 90%
:align: center

Diagram: Ditaa: quick experimental bench sketch.
```

- **Kroki** = system-level visual explanation, blocks, flows, and timing diagrams.
- **CircuitikZ** = formal circuit with standard symbols and LaTeX-quality output.
- **SchemDraw** = programmable circuit from Python, ideal for teaching notebooks.
