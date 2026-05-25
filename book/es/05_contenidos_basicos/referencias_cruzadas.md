(referencias_cruzadas)=
# Referencias cruzadas

Las referencias cruzadas permiten enlazar figuras, tablas, ecuaciones y secciones dentro del libro. Esto es **esencial** para documentos largos: si reorganizas capítulos, los enlaces se actualizan automáticamente.

## Etiquetar una sección

Escribe `(etiqueta)=` justo antes del título:

```md
(mi-tema)=
## Mi tema importante

Contenido aquí...
```

## Referenciar una sección

Usa `{ref}` para crear un enlace con el texto del título:

```md
Ver la sección {ref}`mi-tema` para más detalles.
```

Resultado: Ver la sección {ref}`figuras` para más detalles.

## Etiquetar y referenciar figuras

Usa `:name:` dentro de la directiva `{figure}` y `{numref}` para citar por número:

````md
```{figure} ../../_static/logo.png
:width: 40%
:name:  para citar por número:



Logo del proyecto.
```

La {numref}`fig-logo-ref` muestra el logo.
````

Resultado:


El {numref}`fig-logo-ref` resume visualmente esta parte de la explicación.

```{figure} ../../_static/logo.png
:width: 40%
:name: fig-logo-ref

Logo del proyecto.
```

La {numref}`fig-logo-ref` muestra el logo.

## Etiquetar y referenciar ecuaciones

Usa `(eq-etiqueta)=` después de la ecuación y `{eq}` para citar:

```md
$$
F = ma
$$ (eq-newton)

La ecuación {eq}`eq-newton` es la segunda ley de Newton.
```

Resultado:

$$
F = ma
$$ (eq-newton)

La ecuación {eq}`eq-newton` es la segunda ley de Newton.

## Etiquetar y referenciar tablas

Usa `:name:` dentro de `{table}` y `{numref}` para citar:

````md
```{table} Constantes físicas
:name: tab-constantes
:align: center

| Constante | Símbolo | Valor |
|-----------|---------|-------|
| Vel. luz  | $c$     | $3 \times 10^8$ m/s |
| Planck    | $h$     | $6.63 \times 10^{-34}$ J·s |
```

La {numref}`tab-constantes` lista constantes fundamentales.
````

Resultado:

```{table} Constantes físicas
:name: tab-constantes
:align: center

| Constante | Símbolo | Valor |
|-----------|---------|-------|
| Vel. luz  | $c$     | $3 \times 10^8$ m/s |
| Planck    | $h$     | $6.63 \times 10^{-34}$ J·s |
```

La {numref}`tab-constantes` lista constantes fundamentales.

## Resumen de roles


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Resumen de roles.**

| Rol | Qué referencia | Ejemplo |
|-----|---------------|---------|
| `{ref}` | Secciones (usa el texto del título) | `` {ref}`mi-tema` `` |
| `{numref}` | Figuras y tablas (usa el número) | `` {numref}`fig-logo-ref` `` |
| `{eq}` | Ecuaciones numeradas | `` {eq}`eq-newton` `` |

```{tip}
Usa nombres descriptivos para las etiquetas: `fig-cromatograma`, `eq-bernoulli`, `tab-datos-brutos`. Son más fáciles de recordar que `fig1` o `eq2`.
```
