(admonitions_dropdowns)=
# Admonitions and Dropdowns

Admonitions are **highlighted boxes** that draw the reader's attention. They are perfect for hints, warnings, key definitions, and exercise solutions.

## Note (`{note}`)

````md
```{note}
The exam will be held on June 15th in room 3.2.
```
````

Result:

```{note}
The exam will be held on June 15th in room 3.2.
```

## Warning (`{warning}`)

````md
```{warning}
Do not mix hydrochloric acid with bleach. It produces toxic gas.
```
````

Result:

```{warning}
Do not mix hydrochloric acid with bleach. It produces toxic gas.
```

## Tip (`{tip}`)

````md
```{tip}
To memorize the periodic table, use a color association technique.
```
````

Result:

```{tip}
To memorize the periodic table, use a color association technique.
```

## Important (`{important}`)

````md
```{important}
The submission deadline is Friday at 23:59. Late submissions are not accepted.
```
````

Result:

```{important}
The submission deadline is Friday at 23:59. Late submissions are not accepted.
```

## Caution (`{caution}`)

````md
```{caution}
This reagent is corrosive. Wear gloves and safety goggles.
```
````

Result:

```{caution}
This reagent is corrosive. Wear gloves and safety goggles.
```

## Custom admonition

Use `{admonition}` with your own title:

````md
```{admonition} Definition: covalent bond
A covalent bond is the union between two atoms that share one or more pairs of electrons.
```
````

Result:

```{admonition} Definition: covalent bond
A covalent bond is the union between two atoms that share one or more pairs of electrons.
```

## Dropdown (collapsible content)

Add `:class: dropdown` to hide content until the reader clicks:

````md
```{admonition} Solution to exercise 3
:class: dropdown

The molar mass of water (H₂O) is:

$$M = 2 \times 1.008 + 16.00 = 18.016 \text{ g/mol}$$
```
````

Result:

```{admonition} Solution to exercise 3
:class: dropdown

The molar mass of water (H₂O) is:

$$M = 2 \times 1.008 + 16.00 = 18.016 \text{ g/mol}$$
```

## Teaching use cases


The following table summarizes the main elements of this section.

**Table. Teaching use cases.**

| Type | Common use |
|------|-----------|
| `{note}` | Complementary information, reminders |
| `{warning}` | Hazards, common errors |
| `{tip}` | Study tips, tricks |
| `{important}` | Deadlines, mandatory requirements |
| `{caution}` | Lab safety precautions |
| `dropdown` | Exercise solutions, lengthy steps |

```{tip}
Combine admonitions with math, code, or images inside the block. All MyST content works inside an admonition.
```
