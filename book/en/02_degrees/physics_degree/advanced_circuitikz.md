# Advanced CircuitikZ for Precise Circuits

**CircuitikZ** is the advanced option for drawing circuits with LaTeX-quality output. If you want highly precise schematics, similar to technical notes or scientific papers, this is the right tool.

```{admonition} Practical recommendation
:class: tip
Use **SchemDraw** for most teaching examples. Use **CircuitikZ** when you need a more formal and precise finish.
```

## Recommended workflow in TeachBook

In this project, CircuitikZ is not inserted directly as `raw latex` in the page. Instead:

1. You write the circuit in a `.tex` file
2. You convert it to an image with a script
3. You insert the image with `{figure}`

This makes it work in both HTML and PDF.

## Example source file

File `rc_circuit.tex`:

```tex
\begin{circuitikz}
\draw
  (0,0) to[battery1,l=$V$] (0,3)
  to[R,l=$R$] (3,3)
  to[C,l=$C$] (3,0)
  -- (0,0);
\end{circuitikz}
```

## Command to render it

```bash
python scripts/render_circuitikz.py rc_circuit.tex book/_static/generated/rc_circuit.png
```

## Insert it in a MyST page

```md
```{figure} ../../../_static/generated/rc_circuit.png
:alt: RC circuit generated with CircuitikZ
:width: 70%
:align: center
:name: fig-advanced-circuitikz-1

RC circuit generated with CircuitikZ.
```
```

## Rendered result


The {numref}`fig-advanced-circuitikz-2` visually summarizes this part of the explanation.

```{figure} ../../../_static/generated/rc_circuit_circuitikz.png
:alt: RC circuit generated with CircuitikZ
:width: 70%
:align: center
:name: fig-advanced-circuitikz-2

RC circuit generated from a `.tex` file with CircuitikZ and converted to a PNG image.
```

The advantage of this workflow is that the final circuit behaves like a normal image: it appears on the website, is included in the PDF, and does not require the reader to have LaTeX installed.

## When to use CircuitikZ

- formal electrical schematics
- advanced electronics notes
- material with a technical-paper style finish

## When to use SchemDraw instead

- quick classroom examples
- introductory material
- situations where you want to edit the circuit with less friction

## Prerequisite

If you do not have Tectonic installed yet:

```bash
python scripts/setup_latex.py --yes
```
