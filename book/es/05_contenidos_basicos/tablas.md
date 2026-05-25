(tablas)=
# Tablas

Las tablas son la forma más directa de presentar datos estructurados. MyST soporta tablas Markdown estándar y la directiva `{table}` para añadir numeración.

## Tabla simple en Markdown

```md

La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Tabla simple en Markdown.**

| Elemento | Símbolo | Número atómico |
|----------|---------|----------------|
| Hidrógeno | H      | 1              |
| Helio     | He     | 2              |
| Litio     | Li     | 3              |
```

Resultado:


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Tabla simple en Markdown.**

| Elemento | Símbolo | Número atómico |
|----------|---------|----------------|
| Hidrógeno | H      | 1              |
| Helio     | He     | 2              |
| Litio     | Li     | 3              |

## Tabla con número y pie de foto

Usa `{table}` para obtener numeración automática y poder referenciarla:

````md
```{table} Disolventes comunes en el laboratorio
:name: tab-disolventes
:align: center

| Disolvente | Fórmula | Punto de ebullición (°C) |
|------------|---------|--------------------------|
| Agua       | H₂O     | 100                      |
| Etanol     | C₂H₅OH  | 78                       |
| Acetona    | CH₃COCH₃| 56                       |
| Éter       | C₄H₁₀O  | 35                       |
```
````

Resultado:

```{table} Disolventes comunes en el laboratorio
:name: tab-disolventes
:align: center

| Disolvente | Fórmula | Punto de ebullición (°C) |
|------------|---------|--------------------------|
| Agua       | H₂O     | 100                      |
| Etanol     | C₂H₅OH  | 78                       |
| Acetona    | CH₃COCH₃| 56                       |
| Éter       | C₄H₁₀O  | 35                       |
```

## Alineación de columnas

MyST no soporta alineación por columna en tablas Markdown. Si necesitas alineación específica, usa la directiva `{list-table}`:

````md
```{list-table} Datos experimentales
:header-rows: 1
:name: tab-lista
:align: center

* - Muestra
  - pH
  - Conductividad (mS/cm)
* - A
  - 7.2
  - 1.45
* - B
  - 6.8
  - 2.10
* - C
  - 8.1
  - 0.95
```
````

Resultado:

```{list-table} Datos experimentales
:header-rows: 1
:name: tab-lista
:align: center

* - Muestra
  - pH
  - Conductividad (mS/cm)
* - A
  - 7.2
  - 1.45
* - B
  - 6.8
  - 2.10
* - C
  - 8.1
  - 0.95
```

## Consejos para tablas legibles

- **Menos de 6 columnas**: tablas anchas son difíciles de leer en pantalla.
- **Datos numéricos alineados**: facilita la comparación visual.
- **Unidades en la cabecera**: no repitas unidades en cada celda.
- **Tablas largas**: si superas 15 filas, considera usar un gráfico.

```{tip}
En la {numref}`tab-disolventes` se muestra un ejemplo con unidades en la cabecera. Observa que las columnas numéricas facilitan la comparación.
```
