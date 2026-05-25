# Quadratic Equation

The quadratic equation is a useful example for combining mathematical explanation, formulas, and tables in a page that works in both HTML and PDF.

We start from the general form:

$$
ax^2 + bx + c = 0, \qquad a \neq 0
$$

The behavior of its solutions depends on the discriminant:

$$
\Delta = b^2 - 4ac
$$

When $\Delta \geq 0$, the real solutions are computed with:

$$
x = \frac{-b \pm \sqrt{\Delta}}{2a}
$$

## Interpreting the discriminant

| Value of $\Delta$ | Type of solutions | Geometric interpretation |
|---|---|---|
| $\Delta > 0$ | Two distinct real solutions | The parabola intersects the $x$-axis at two points |
| $\Delta = 0$ | One repeated real solution | The parabola is tangent to the $x$-axis |
| $\Delta < 0$ | Two complex conjugate solutions | The parabola does not intersect the $x$-axis |

## Example

For the equation:

$$
x^2 - 5x + 6 = 0
$$

we have $a = 1$, $b = -5$, and $c = 6$. Therefore:

$$
\Delta = (-5)^2 - 4 \cdot 1 \cdot 6 = 1
$$

Since $\Delta > 0$, there are two real solutions:

$$
x_1 = \frac{5 + 1}{2} = 3,
\qquad
x_2 = \frac{5 - 1}{2} = 2
$$

```{tip}
This static example is intentionally lightweight: it requires no video dependencies and exports reliably to both the website and the PDF.
```
