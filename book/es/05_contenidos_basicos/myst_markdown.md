# MyST Markdown: lo básico

**MyST** (Mark up Your Scientific Text) es una extensión de Markdown diseñada para documentos científicos y técnicos. Es el formato que usa Jupyter Book. Si conoces Markdown básico, ya sabes el 80 % de MyST.

## Sintaxis esencial

### Títulos

```md
# Título principal (H1)
## Sección (H2)
### Subsección (H3)
```

### Formato de texto

```md
**Negrita** para énfasis fuerte.
*Cursiva* para términos o títulos de obras.
`código inline` para nombres de archivos o comandos.
```

### Listas

```md
- Elemento de lista no ordenada
- Otro elemento
  - Sub-elemento con sangría

1. Primer paso
2. Segundo paso
3. Tercer paso
```

### Enlaces e imágenes

```md
[Texto del enlace](https://ejemplo.com)
```

```md
![Texto alternativo](ruta/a/imagen.png)
```

Para imágenes que vayas a explicar o citar en el texto, usa la directiva `{figure}` de la sección [Figuras e imágenes](figuras.md). Así podrás añadir caption, texto alternativo y referencias con `{numref}`.

## Directivas

MyST añade **directivas** que no existen en Markdown normal:

```{note}
Esto es una nota. Aparece resaltada en azul.
```

```{warning}
Esto es una advertencia. Aparece resaltada en rojo/naranja.
```

```{tip}
Esto es un consejo. Aparece resaltada en verde.
```

Puedes crear bloques personalizados con `admonition`:

````md
```{admonition} Mi título personalizado
Contenido del bloque.
```
````

## Matemáticas

Inline: la ecuación $E = mc^2$ se escribe como `$E = mc^2$`.

Display:

$$
\int_0^\infty e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
$$

Se escribe como `$$ ... $$` en su propia línea.

## Tablas

```md
La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Tablas.**

| Columna A | Columna B | Columna C |
|-----------|-----------|-----------|
| dato 1    | dato 2    | dato 3    |
| dato 4    | dato 5    | dato 6    |
```

Resultado:

La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Tablas.**

| Columna A | Columna B | Columna C |
|-----------|-----------|-----------|
| dato 1    | dato 2    | dato 3    |
| dato 4    | dato 5    | dato 6    |

## Bloques de código

````md
```python
def saludar(nombre):
    return f"Hola, {nombre}!"
```
````

```{admonition} Consejo
:class: tip
No memorices toda la sintaxis. Usa un asistente de IA para generar el MyST que necesites y aprende sobre la marcha.
```
