# Ecuación de segundo grado

La ecuación de segundo grado es uno de los ejemplos más útiles para combinar explicación matemática, fórmulas y tablas en una página compatible con HTML y PDF.

Partimos de la forma general:

$$
ax^2 + bx + c = 0, \qquad a \neq 0
$$

El comportamiento de sus soluciones depende del discriminante:

$$
\Delta = b^2 - 4ac
$$

Cuando $\Delta \geq 0$, las soluciones reales se calculan con:

$$
x = \frac{-b \pm \sqrt{\Delta}}{2a}
$$

## Interpretación del discriminante

| Valor de $\Delta$ | Tipo de soluciones | Interpretación geométrica |
|---|---|---|
| $\Delta > 0$ | Dos soluciones reales distintas | La parábola corta al eje $x$ en dos puntos |
| $\Delta = 0$ | Una solución real doble | La parábola es tangente al eje $x$ |
| $\Delta < 0$ | Dos soluciones complejas conjugadas | La parábola no corta al eje $x$ |

## Ejemplo

Para la ecuación:

$$
x^2 - 5x + 6 = 0
$$

tenemos $a = 1$, $b = -5$ y $c = 6$. Por tanto:

$$
\Delta = (-5)^2 - 4 \cdot 1 \cdot 6 = 1
$$

Como $\Delta > 0$, existen dos soluciones reales:

$$
x_1 = \frac{5 + 1}{2} = 3,
\qquad
x_2 = \frac{5 - 1}{2} = 2
$$

```{tip}
Este ejemplo estático es deliberadamente ligero: no requiere dependencias de vídeo y se exporta de forma estable tanto a la web como al PDF.
```
