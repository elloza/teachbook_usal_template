# Exercises with Solutions

Patterns for creating exercises with hidden solutions that students can reveal when ready. This approach works in both **HTML** and **PDF**.

## Basic pattern

Use `{admonition}` for the exercise statement and `{admonition}` with `:class: dropdown` for the solution:

````md
```{admonition} Exercise 1 — Basic derivative
:class: important

Calculate the derivative of $f(x) = 3x^4 - 2x^2 + 7x - 1$.
```

```{admonition} Solution
:class: dropdown

Apply differentiation rules term by term:

$$f'(x) = 12x^3 - 4x + 7$$
```
````

```{admonition} Exercise 1 — Basic derivative
:class: important

Calculate the derivative of $f(x) = 3x^4 - 2x^2 + 7x - 1$.
```

```{admonition} Solution
:class: dropdown

Apply differentiation rules term by term:

$$f'(x) = 12x^3 - 4x + 7$$
```

---

## Exercises with difficulty levels

Add difficulty hints to guide the student:

```{admonition} Exercise 2 — Integral (level: basic)
:class: important

Calculate $\int_0^3 (2x + 1) \, dx$.
```

```{admonition} Solution
:class: dropdown

$$\int_0^3 (2x + 1) \, dx = \left[x^2 + x\right]_0^3 = (9 + 3) - 0 = 12$$
```

```{admonition} Exercise 3 — Integral (level: intermediate)
:class: important

Calculate $\int_0^{\pi} x \sin(x) \, dx$. *Hint: integration by parts.*
```

```{admonition} Solution
:class: dropdown

Use integration by parts with $u = x$ and $dv = \sin(x)\,dx$:

$$\int_0^{\pi} x \sin(x) \, dx = \left[-x\cos(x)\right]_0^{\pi} + \int_0^{\pi} \cos(x)\,dx = \pi + 0 = \pi$$
```

```{admonition} Exercise 4 — Integral (level: advanced)
:class: important

Calculate $\int_{-\infty}^{\infty} e^{-x^2} \, dx$. *Hint: use polar coordinates.*
```

```{admonition} Solution
:class: dropdown

Let $I = \int_{-\infty}^{\infty} e^{-x^2} dx$. Then:

$$I^2 = \int_{-\infty}^{\infty}\int_{-\infty}^{\infty} e^{-(x^2+y^2)} dx\,dy$$

Converting to polar: $I^2 = \int_0^{2\pi}\int_0^{\infty} e^{-r^2} r\,dr\,d\theta = 2\pi \cdot \frac{1}{2} = \pi$

Therefore: $I = \sqrt{\pi}$
```

```{admonition} Tip
:class: tip
Dropdowns appear expanded in PDF export, which is desirable for the printed version. On the web, the student must click to reveal the solution.
```
