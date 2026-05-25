# Preguntas de Práctica: Estadística

Pon a prueba tus conocimientos sobre conceptos fundamentales de estadística.
Despliega cada pregunta para ver la respuesta.

---

```{admonition} Pregunta 1 — Valor p
:class: dropdown

**¿Qué significa exactamente un valor p de 0.03 en un contraste de hipótesis?**

Un valor p de 0.03 significa que, **si la hipótesis nula $H_0$ fuera cierta**,
la probabilidad de observar un resultado tan extremo o más que el obtenido sería del 3%.

**Importante:** NO es la probabilidad de que $H_0$ sea cierta. Es la probabilidad
de los datos (o más extremos) dado $H_0$.

Como 0.03 < 0.05 (nivel de significación típico), rechazaríamos $H_0$.
```

```{admonition} Pregunta 2 — Intervalo de confianza
:class: dropdown

**Interpreta un intervalo de confianza del 95% para una media: $[12.3, 15.7]$.**

NO significa que la media poblacional tenga un 95% de probabilidad de estar en ese intervalo.
La interpretación correcta es frecuentista:

> Si repetimos el experimento muchas veces, el 95% de los intervalos construidos
> con el mismo método contendrán el verdadero valor del parámetro.

Para este intervalo particular, la media poblacional está dentro o fuera — no hay
probabilidad intermedia. Lo que tiene un 95% de confianza es el **método de construcción**.
```

```{admonition} Pregunta 3 — Distribución normal
:class: dropdown

**¿Qué proporción de datos se encuentra dentro de ±2 desviaciones estándar de la media
en una distribución normal?**

Usando la regla empírica (regla 68-95-99.7):


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Preguntas de Práctica: Estadística.**

| Rango | Proporción |
|-------|-----------|
| $\mu \pm 1\sigma$ | ≈ 68.27% |
| $\mu \pm 2\sigma$ | ≈ 95.45% |
| $\mu \pm 3\sigma$ | ≈ 99.73% |

Por tanto, aproximadamente el **95.45%** de los datos están dentro de $\mu \pm 2\sigma$.
```

```{admonition} Pregunta 4 — Correlación vs. causalidad
:class: dropdown

**Si dos variables tienen una correlación $r = 0.85$, ¿puede concluirse que una causa la otra?**

**No.** Correlación no implica causalidad. Una correlación fuerte solo indica asociación lineal.
Las posibles explicaciones son:

1. **$X$ causa $Y$** — posible pero no demostrado solo con $r$.
2. **$Y$ causa $X$** — la dirección podría ser inversa.
3. **Una variable confusora $Z$** causa ambas.
4. **Coincidencia** — especialmente con pocos datos.

Para establecer causalidad se necesitan estudios experimentales (control aleatorizado),
no solo observacionales.
```

```{admonition} Pregunta 5 — Error Tipo I y Tipo II
:class: dropdown

**Define error Tipo I y error Tipo II. ¿Cuál se controla directamente con el nivel α?**


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Preguntas de Práctica: Estadística.**

| Tipo | Ocurre cuando... | Se llama |
|------|------------------|----------|
| **Error Tipo I** | Rechazamos $H_0$ siendo cierta | Falso positivo |
| **Error Tipo II** | No rechazamos $H_0$ siendo falsa | Falso negativo |

El **nivel de significación $\alpha$** controla directamente la probabilidad de cometer
un error Tipo I: $P(\text{Error I}) = \alpha$.

La probabilidad de error Tipo II se denomina $\beta$, y la potencia de un test es
$1 - \beta$. Disminuir $\alpha$ generalmente aumenta $\beta$.
```

```{admonition} Pregunta 6 — Teorema del Límite Central
:class: dropdown

**Enuncia el Teorema del Límite Central y explica su importancia práctica.**

El **Teorema del Límite Central (TLC)** establece que, para muestras suficientemente
grandes ($n \geq 30$, aproximadamente), la distribución de la media muestral $\bar{X}$
se aproxima a una distribución normal:

$$\bar{X} \sim N\left(\mu, \frac{\sigma^2}{n}\right)$$

independientemente de la distribución de la población original.

**Importancia práctica:** Justifica el uso de la distribución normal para construir
intervalos de confianza y realizar contrastes de hipótesis sobre la media, incluso
cuando la población no es normal. Es la base de gran parte de la estadística inferencial.
```
