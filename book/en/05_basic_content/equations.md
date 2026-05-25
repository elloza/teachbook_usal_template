(equations)=
# Equations and Mathematics

MyST supports LaTeX math via the `dollarmath` extension, already enabled in this template. Works in **HTML and PDF**.

## Inline math

Use `$...$` within a line of text:

```md
Energy is calculated as $E = mc^2$, where $m$ is mass.
```

Result: Energy is calculated as $E = mc^2$, where $m$ is mass.

## Display equation (unnumbered)

Use `$$...$$` on its own line:

```md
$$
\int_0^\infty e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
$$
```

Result:

$$
\int_0^\infty e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
$$

## Numbered equation with label

Add a label `(label)=` before the equation to reference it:

```md
$$
\frac{\partial u}{\partial t} = \alpha \nabla^2 u
$$ (eq-heat)
```

Result:

$$
\frac{\partial u}{\partial t} = \alpha \nabla^2 u
$$ (eq-heat)

## Cross-reference to an equation

Use `{eq}` to cite an equation by its number:

```md
Equation {eq}`eq-heat` describes heat diffusion.
```

Result: Equation {eq}`eq-heat` describes heat diffusion.

## Common math symbols


The following table summarizes the main elements of this section.

**Table. Common math symbols.**

| Symbol | LaTeX code | Symbol | LaTeX code |
|--------|-----------|--------|-----------|
| $\alpha$ | `\alpha` | $\beta$ | `\beta` |
| $\gamma$ | `\gamma` | $\delta$ | `\delta` |
| $\pi$ | `\pi` | $\theta$ | `\theta` |
| $\lambda$ | `\lambda` | $\sigma$ | `\sigma` |
| $\sum$ | `\sum` | $\prod$ | `\prod` |
| $\int$ | `\int` | $\oint$ | `\oint` |
| $\infty$ | `\infty` | $\nabla$ | `\nabla` |
| $\frac{a}{b}$ | `\frac{a}{b}` | $\sqrt{x}$ | `\sqrt{x}` |
| $\leq$ | `\leq` | $\geq$ | `\geq` |
| $\approx$ | `\approx` | $\neq$ | `\neq` |
| $\vec{v}$ | `\vec{v}` | $\hat{x}$ | `\hat{x}` |

```{tip}
For complex math, ask your AI assistant to generate LaTeX code from a natural language description: "generate the Gauss integral formula in LaTeX."
```
