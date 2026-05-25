(ecuaciones)=
# Ecuaciones y matemáticas

MyST soporta matemáticas en formato LaTeX gracias a la extensión `dollarmath`, ya activada en esta plantilla. Funciona en **HTML y PDF**.

## Matemáticas inline

Se usa `$...$` dentro de una línea de texto:

```md
La energía se calcula como $E = mc^2$, donde $m$ es la masa.
```

Resultado: La energía se calcula como $E = mc^2$, donde $m$ es la masa.

## Ecuación display (sin número)

Se usa `$$...$$` en su propia línea:

```md
$$
\int_0^\infty e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
$$
```

Resultado:

$$
\int_0^\infty e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
$$

## Ecuación numerada con etiqueta

Añade una etiqueta `(label)=` antes de la ecuación para poder referenciarla:

```md
$$
\frac{\partial u}{\partial t} = \alpha \nabla^2 u
$$ (eq-calor)
```

Resultado:

$$
\frac{\partial u}{\partial t} = \alpha \nabla^2 u
$$ (eq-calor)

## Referencia cruzada a una ecuación

Usa `{eq}` para citar una ecuación por su número:

```md
La ecuación {eq}`eq-calor` describe la difusión de calor.
```

Resultado: La ecuación {eq}`eq-calor` describe la difusión de calor.

## Símbolos matemáticos comunes


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Símbolos matemáticos comunes.**

| Símbolo | Código LaTeX | Símbolo | Código LaTeX |
|---------|-------------|---------|-------------|
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
Para escribir matemáticas complejas, pide a tu asistente de IA que genere el código LaTeX a partir de una descripción en lenguaje natural: «genera la fórmula de la integral de Gauss en LaTeX».
```
