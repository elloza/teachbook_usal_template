(figuras)=
# Figuras e imágenes

Las figuras son esenciales en cualquier material docente. MyST ofrece dos directivas principales: `{image}` (imagen simple) y `{figure}` (imagen con número y pie de foto).

## Imagen centrada con texto alternativo

La directiva `{image}` inserta una imagen sin numeración:

````md
```{image} ../../_static/logo.png
:alt: Logo del libro
:width: 60%
:align: center
```
````

Resultado:

```{image} ../../_static/logo.png
:alt: Logo del libro
:width: 60%
:align: center
```

## Figura numerada con pie de foto

La directiva `{figure}` añade numeración automática (`Figura 1`, `Figura 2`…):

````md
```{figure} ../../_static/logo.png
:width: 50%
:align: center
:name: fig-figuras-1

Logo del libro.
```
````

Resultado:


El {numref}`fig-logo` resume visualmente esta parte de la explicación.

```{figure} ../../_static/logo.png
:width: 50%
:align: center
:name: fig-logo

Logo del libro.
```

## Referencia cruzada a una figura

Usa `{numref}` para referenciar figuras por su número:

```md
En la {numref}`fig-logo` se muestra el logo del libro.
```

Resultado: En la {numref}`fig-logo` se muestra el logo del libro.

## Figura en el margen

Añade `:figclass: margin` para colocar una imagen en el margen (solo HTML):

````md
```{figure} ../../_static/logo.png
:figclass: margin
:width: 100%
:name: fig-figuras-3

Logo en el margen.
```
````

Resultado:


El {numref}`fig-figuras-4` resume visualmente esta parte de la explicación.

```{figure} ../../_static/logo.png
:figclass: margin
:width: 100%
:name: fig-figuras-4

Logo en el margen.
```

## Parámetros útiles


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Parámetros útiles.**

| Parámetro | Qué hace | Ejemplo |
|-----------|----------|---------|
| `:width:` | Ancho (`50%`, `200px`) | `:width: 80%` |
| `:align:` | Alineación (`left`, `center`, `right`) | `:align: center` |
| `:alt:` | Texto alternativo (accesibilidad) | `:alt: Diagrama` |
| `:name:` | Etiqueta para `{numref}` | `:name: fig-mapa` |
| `:figclass:` | Clase CSS (`margin`) | `:figclass: margin` |

```{tip}
Siempre añade `:alt:` para accesibilidad. Es el texto que ven los lectores de pantalla y se muestra si la imagen no carga.
```
