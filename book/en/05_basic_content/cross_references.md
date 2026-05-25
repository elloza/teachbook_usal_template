(cross_references)=
# Cross-References

Cross-references allow you to link figures, tables, equations, and sections within the book. This is **essential** for long documents: if you rearrange chapters, links update automatically.

## Label a section

Write `(label)=` just before the heading:

```md
(my-topic)=
## My Important Topic

Content here...
```

## Reference a section

Use `{ref}` to create a link with the heading text:

```md
See the {ref}`my-topic` section for details.
```

Result: See the {ref}`figures` section for details.

## Label and reference figures

Use `:name:` inside the `{figure}` directive and `{numref}` to cite by number:

````md
```{figure} ../../_static/logo.png
:width: 40%
:name:  to cite by number:



Project logo.
```

The {numref}`fig-logo-ref-en` shows the logo.
````

Result:


The {numref}`fig-logo-ref-en` visually summarizes this part of the explanation.

```{figure} ../../_static/logo.png
:width: 40%
:name: fig-logo-ref-en

Project logo.
```

The {numref}`fig-logo-ref-en` shows the logo.

## Label and reference equations

Use `(eq-label)=` after the equation and `{eq}` to cite:

```md
$$
F = ma
$$ (eq-newton-en)

Equation {eq}`eq-newton-en` is Newton's second law.
```

Result:

$$
F = ma
$$ (eq-newton-en)

Equation {eq}`eq-newton-en` is Newton's second law.

## Label and reference tables

Use `:name:` inside `{table}` and `{numref}` to cite:

````md
```{table} Physical constants
:name: tab-constants-en
:align: center

| Constant | Symbol | Value |
|----------|--------|-------|
| Speed of light | $c$ | $3 \times 10^8$ m/s |
| Planck   | $h$     | $6.63 \times 10^{-34}$ J·s |
```

The {numref}`tab-constants-en` lists fundamental constants.
````

Result:

```{table} Physical constants
:name: tab-constants-en
:align: center

| Constant | Symbol | Value |
|----------|--------|-------|
| Speed of light | $c$ | $3 \times 10^8$ m/s |
| Planck   | $h$     | $6.63 \times 10^{-34}$ J·s |
```

The {numref}`tab-constants-en` lists fundamental constants.

## Roles summary


The following table summarizes the main elements of this section.

**Table. Roles summary.**

| Role | What it references | Example |
|------|-------------------|---------|
| `{ref}` | Sections (uses heading text) | `` {ref}`my-topic` `` |
| `{numref}` | Figures and tables (uses number) | `` {numref}`fig-logo-ref-en` `` |
| `{eq}` | Numbered equations | `` {eq}`eq-newton-en` `` |

```{tip}
Use descriptive label names: `fig-chromatogram`, `eq-bernoulli`, `tab-raw-data`. They are easier to remember than `fig1` or `eq2`.
```
