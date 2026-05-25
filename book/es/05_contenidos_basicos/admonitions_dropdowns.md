(admonitions_dropdowns)=
# Admoniciones y desplegables

Las admoniciones son **cajas resaltadas** que llaman la atención del lector. Son perfectas para pistas, avisos, definiciones clave y soluciones de ejercicios.

## Nota (`{note}`)

````md
```{note}
El examen será el 15 de junio en el aula 3.2.
```
````

Resultado:

```{note}
El examen será el 15 de junio en el aula 3.2.
```

## Advertencia (`{warning}`)

````md
```{warning}
No mezcles ácido clorhídrico con lejía. Produce gas tóxico.
```
````

Resultado:

```{warning}
No mezcles ácido clorhídrico con lejía. Produce gas tóxico.
```

## Consejo (`{tip}`)

````md
```{tip}
Para memorizar la tabla periódica, usa la técnica de asociación con colores.
```
````

Resultado:

```{tip}
Para memorizar la tabla periódica, usa la técnica de asociación con colores.
```

## Importante (`{important}`)

````md
```{important}
La fecha límite de entrega es el viernes a las 23:59. No se admiten entregas fuera de plazo.
```
````

Resultado:

```{important}
La fecha límite de entrega es el viernes a las 23:59. No se admiten entregas fuera de plazo.
```

## Precaución (`{caution}`)

````md
```{caution}
Este reactivo es corrosivo. Usa guantes y gafas de protección.
```
````

Resultado:

```{caution}
Este reactivo es corrosivo. Usa guantes y gafas de protección.
```

## Admonición personalizada

Usa `{admonition}` con título propio:

````md
```{admonition} Definición: enlace covalente
Un enlace covalente es la unión entre dos átomos que comparten uno o más pares de electrones.
```
````

Resultado:

```{admonition} Definición: enlace covalente
Un enlace covalente es la unión entre dos átomos que comparten uno o más pares de electrones.
```

## Desplegable (contenido colapsable)

Añade `:class: dropdown` para que el contenido se oculte hasta que el lector haga clic:

````md
```{admonition} Solución del ejercicio 3
:class: dropdown

La masa molar del agua (H₂O) es:

$$M = 2 \times 1.008 + 16.00 = 18.016 \text{ g/mol}$$
```
````

Resultado:

```{admonition} Solución del ejercicio 3
:class: dropdown

La masa molar del agua (H₂O) es:

$$M = 2 \times 1.008 + 16.00 = 18.016 \text{ g/mol}$$
```

## Usos docentes


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Usos docentes.**

| Tipo | Uso habitual |
|------|-------------|
| `{note}` | Información complementaria, recordatorios |
| `{warning}` | Peligros, errores frecuentes |
| `{tip}` | Consejos de estudio, trucos |
| `{important}` | Plazos, requisitos obligatorios |
| `{caution}` | Precauciones de laboratorio |
| `dropdown` | Soluciones de ejercicios, pasos largos |

```{tip}
Combina admoniciones con matemáticas, código o imágenes dentro del bloque. Todo el contenido MyST funciona dentro de una admonición.
```
