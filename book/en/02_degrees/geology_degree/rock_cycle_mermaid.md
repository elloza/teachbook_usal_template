# The Rock Cycle with Kroki (Mermaid)

The rock cycle describes the transformations between the three main rock types.
With Kroki and `:type: mermaid`, we can represent this cycle as a flowchart that works in both HTML and PDF.

## The cycle

**Code:**

````md
```{kroki}
:type: mermaid
:align: center

flowchart LR
    Magma["Magma"]
    Igneous["Igneous Rock"]
    Sedimentary["Sedimentary Rock"]
    Metamorphic["Metamorphic Rock"]

    Magma -->|"Cooling and solidification"| Igneous
    Igneous -->|"Weathering and erosion"| Sedimentary
    Sedimentary -->|"Heat and pressure"| Metamorphic
    Metamorphic -->|"Melting"| Magma
    Igneous -->|"Heat and pressure"| Metamorphic
    Metamorphic -->|"Weathering and erosion"| Sedimentary
    Sedimentary -->|"Melting"| Magma
```
````

**Result:**


As shown in {numref}`fig-diagram-02-degrees-geology-degree-rock-cycle-mermaid-01`, the diagram is versioned as a static image.

```{figure} ../../../_static/generated/diagrams/en/02_degrees_geology_degree_rock_cycle_mermaid_01.svg
:name: fig-diagram-02-degrees-geology-degree-rock-cycle-mermaid-01
:alt: Diagram: The cycle
:width: 90%
:align: center

Diagram: The cycle.
```
The following table summarizes the main elements of this section.

**Table. Transition explanation.**

| Transition | Geological process |
|------------|--------------------|
| Magma → Igneous | Cooling and solidification at the surface or underground |
| Igneous → Sedimentary | Weathering, erosion, transport, and sedimentation |
| Sedimentary → Metamorphic | Heat and pressure (metamorphism) without melting |
| Metamorphic → Magma | Complete melting at extreme temperatures |
| Igneous → Metamorphic | Direct metamorphism through heat and pressure |
| Metamorphic → Sedimentary | Uplift, weathering, and erosion |

## Key point

Any rock type can transform into any other. It is not a linear cycle, but a **transformation network** operating on geological timescales (millions of years).
