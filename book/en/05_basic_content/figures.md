(figures)=
# Figures and Images

Figures are essential in any teaching material. MyST offers two main directives: `{image}` (simple image) and `{figure}` (image with number and caption).

## Centered image with alt text

The `{image}` directive inserts an image without numbering:

````md
```{image} ../../_static/logo.png
:alt: Book logo
:width: 60%
:align: center
```
````

Result:

```{image} ../../_static/logo.png
:alt: Book logo
:width: 60%
:align: center
```

## Numbered figure with caption

The `{figure}` directive adds automatic numbering (`Figure 1`, `Figure 2`…):

````md
```{figure} ../../_static/logo.png
:width: 50%
:align: center
:name: fig-figures-1

Book logo.
```
````

Result:


The {numref}`fig-logo-en` visually summarizes this part of the explanation.

```{figure} ../../_static/logo.png
:width: 50%
:align: center
:name: fig-logo-en

Book logo.
```

## Cross-reference to a figure

Use `{numref}` to reference figures by their number:

```md
The {numref}`fig-logo-en` shows the book logo.
```

Result: The {numref}`fig-logo-en` shows the book logo.

## Margin figure

Add `:figclass: margin` to place an image in the margin (HTML only):

````md
```{figure} ../../_static/logo.png
:figclass: margin
:width: 100%
:name: fig-figures-3

Logo in the margin.
```
````

Result:


The {numref}`fig-figures-4` visually summarizes this part of the explanation.

```{figure} ../../_static/logo.png
:figclass: margin
:width: 100%
:name: fig-figures-4

Logo in the margin.
```

## Useful parameters


The following table summarizes the main elements of this section.

**Table. Useful parameters.**

| Parameter | What it does | Example |
|-----------|--------------|---------|
| `:width:` | Width (`50%`, `200px`) | `:width: 80%` |
| `:align:` | Alignment (`left`, `center`, `right`) | `:align: center` |
| `:alt:` | Alt text (accessibility) | `:alt: Diagram` |
| `:name:` | Label for `{numref}` | `:name: fig-map` |
| `:figclass:` | CSS class (`margin`) | `:figclass: margin` |

```{tip}
Always add `:alt:` for accessibility. It is the text that screen readers see and displays if the image fails to load.
```
