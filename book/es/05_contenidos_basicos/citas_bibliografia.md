(citas_bibliografia)=
# Citas y bibliografía

Esta plantilla incluye `sphinxcontrib-bibtex`, que permite gestionar referencias bibliográficas con archivos BibTeX.

## Archivo de referencias

Las referencias se guardan en `book/_static/references.bib`. Cada entrada tiene este formato:

```bibtex
@book{einstein1920,
  author    = {Albert Einstein},
  title     = {Relativity: The Special and General Theory},
  year      = {1920},
  publisher = {Henry Holt and Company}
}

@article{dirac1930,
  author  = {Paul A. M. Dirac},
  title   = {A Theory of Electrons and Protons},
  journal = {Proceedings of the Royal Society A},
  year    = {1930},
  volume  = {126},
  pages   = {360--365}
}
```

## Cita textual: `{cite:t}`

Inserta el nombre del autor seguido del año:

```md
{cite:t}`einstein1920` formuló la teoría de la relatividad.
```

Resultado: {cite:t}`einstein1920` formuló la teoría de la relatividad.

## Cita entre paréntesis: `{cite:p}`

Inserta autor y año entre paréntesis:

```md
La mecánica cuántica revolucionó la física {cite:p}`dirac1930`.
```

Resultado: La mecánica cuántica revolucionó la física {cite:p}`dirac1930`.

## Múltiples citas

Separa varias claves con comas:

```md
Varios autores contribuyeron {cite:p}`einstein1920,dirac1930`.
```

Resultado: Varios autores contribuyeron {cite:p}`einstein1920,dirac1930`.

## Imprimir la bibliografía

La plantilla usa dos niveles de bibliografía:

- **Global**: la página final `Bibliografía` recoge las entradas citadas en el libro, no todo el archivo `book/_static/references.bib`.
- **Local**: una página concreta puede mostrar solo sus propias referencias en un bloque visible solo en HTML.

### Bibliografía global del libro

La bibliografía global ya está preparada en la página `Bibliografía` del final del libro:

````md
```{bibliography}
:cited:
```
````

No añadas este bloque en páginas normales: debe existir solo en la página global de bibliografía.

```{note}
Si añades bibliografías locales en varias páginas web, algunas entradas también aparecerán en la página global `Bibliografía`. Es normal: la bibliografía local ayuda a leer una página concreta y la página global reúne el conjunto del libro. En PDF solo se imprime la bibliografía global final.
```

### Bibliografía local de una página

Para una bibliografía local en la web, cita con `{cite:t}` o `{cite:p}` en el texto normal de la página y añade al final una directiva `{bibliography}` filtrada dentro de `{only} html`. Así el HTML puede mostrar referencias de página, pero el PDF conserva solo la bibliografía general final.

`````md
Texto con una cita local {cite:p}`clave_cita`.

````{only} html
## Bibliografía de esta página

```{bibliography}
:filter: docname in docnames
```
````
`````

También puedes mostrar solo algunas claves concretas del documento en HTML:

`````md
````{only} html
```{bibliography}
:filter: docname in docnames and key in {"ziman2000", "hodson1996"}
```
````
`````

En este ejemplo local, {cite:t}`ziman2000` describe la ciencia como una práctica social, no solo como una colección de resultados. El trabajo de laboratorio conviene conectarlo con la construcción de explicaciones, no solo con seguir instrucciones {cite:p}`hodson1996`.

````{only} html
Resultado local:

```{bibliography}
:filter: docname in docnames and key in {"ziman2000", "hodson1996"}
```
````

## Flujo de trabajo

1. Añade las entradas BibTeX a `_static/references.bib`.
2. Cita con `{cite:t}` o `{cite:p}` en cualquier página.
3. Si quieres una bibliografía local visible en HTML, añade al final de la página un bloque `{only} html` con `{bibliography}` filtrada.
4. En PDF, no generes bibliografías locales: la plantilla crea un `.bib` temporal con las citas usadas y las muestra solo en la página global `Bibliografía`.

```{warning}
Cada clave de cita (ej: `einstein1920`) debe ser única en todo el archivo `.bib`. Si se duplica, la compilación fallará.
```
