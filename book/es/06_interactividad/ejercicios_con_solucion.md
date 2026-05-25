# Ejercicios con Solución

Patrones para crear ejercicios con soluciones ocultas que el estudiante puede desplegar cuando esté listo. Este enfoque funciona tanto en **HTML** como en **PDF**.

## Patrón básico

Usa `{admonition}` para el enunciado y `{admonition}` con `:class: dropdown` para la solución:

````md
```{admonition} Ejercicio 1 — Derivada básica
:class: important

Calcula la derivada de $f(x) = 3x^4 - 2x^2 + 7x - 1$.
```

```{admonition} Solución
:class: dropdown

Aplicamos las reglas de derivación término a término:

$$f'(x) = 12x^3 - 4x + 7$$
```
````

```{admonition} Ejercicio 1 — Derivada básica
:class: important

Calcula la derivada de $f(x) = 3x^4 - 2x^2 + 7x - 1$.
```

```{admonition} Solución
:class: dropdown

Aplicamos las reglas de derivación término a término:

$$f'(x) = 12x^3 - 4x + 7$$
```

---

## Ejercicios con nivel de dificultad

Añade indicaciones de dificultad para guiar al estudiante:

```{admonition} Ejercicio 2 — Integral (nivel: básico)
:class: important

Calcula $\int_0^3 (2x + 1) \, dx$.
```

```{admonition} Solución
:class: dropdown

$$\int_0^3 (2x + 1) \, dx = \left[x^2 + x\right]_0^3 = (9 + 3) - 0 = 12$$
```

```{admonition} Ejercicio 3 — Integral (nivel: intermedio)
:class: important

Calcula $\int_0^{\pi} x \sin(x) \, dx$. *Pista: integración por partes.*
```

```{admonition} Solución
:class: dropdown

Usamos integración por partes con $u = x$ y $dv = \sin(x)\,dx$:

$$\int_0^{\pi} x \sin(x) \, dx = \left[-x\cos(x)\right]_0^{\pi} + \int_0^{\pi} \cos(x)\,dx = \pi + 0 = \pi$$
```

```{admonition} Ejercicio 4 — Integral (nivel: avanzado)
:class: important

Calcula $\int_{-\infty}^{\infty} e^{-x^2} \, dx$. *Pista: usa coordenadas polares.*
```

```{admonition} Solución
:class: dropdown

Sea $I = \int_{-\infty}^{\infty} e^{-x^2} dx$. Entonces:

$$I^2 = \int_{-\infty}^{\infty}\int_{-\infty}^{\infty} e^{-(x^2+y^2)} dx\,dy$$

Pasando a polares: $I^2 = \int_0^{2\pi}\int_0^{\infty} e^{-r^2} r\,dr\,d\theta = 2\pi \cdot \frac{1}{2} = \pi$

Por tanto: $I = \sqrt{\pi}$
```

```{admonition} Consejo
:class: tip
Los `dropdown` aparecen expandidos en la exportación PDF, lo cual es deseable para la versión impresa. En la web, el estudiante debe hacer clic para ver la solución.
```
