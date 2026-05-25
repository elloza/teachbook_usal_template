(tabs_cards)=
# Pestañas y tarjetas

La extensión **sphinx-design** (ya instalada) permite organizar contenido en pestañas y tarjetas. Ideal para comparar opciones, mostrar código en varios lenguajes o presentar pasos alternativos.

## Pestañas simples (`{tab-set}` / `{tab-item}`)

`````md
::::{tab-set}
:::{tab-item} Python
```python
print("Hola, mundo")
```
:::

:::{tab-item} R
```r
print("Hola, mundo")
```
:::

:::{tab-item} MATLAB
```matlab
disp('Hola, mundo')
```
:::
::::
`````

Resultado:

::::{tab-set}
:::{tab-item} Python
```python
print("Hola, mundo")
```
:::

:::{tab-item} R
```r
print("Hola, mundo")
```
:::

:::{tab-item} MATLAB
```matlab
disp('Hola, mundo')
```
:::
::::

## Pestañas con grupo (`{tab-set}` / `{tab-item}`)

Los grupos de pestañas permiten sincronización:

````md
::::{tab-set}
:::{tab-item} Método analítico
Resolviendo la ecuación diferencial directamente.
:::

:::{tab-item} Método numérico
Aproximando la solución paso a paso con un ordenador.
:::
::::
````

Resultado:

::::{tab-set}
:::{tab-item} Método analítico
Resolviendo la ecuación diferencial directamente.
:::

:::{tab-item} Método numérico
Aproximando la solución paso a paso con un ordenador.
:::
::::

## Pestañas con pasos de un procedimiento

````md
::::{tab-set}
:::{tab-item} Paso 1: Preparar la muestra
Pesar 0.5 g del compuesto sólido con precisión de 0.001 g.
:::

:::{tab-item} Paso 2: Disolver
Añadir 50 mL de disolvente y agitar durante 5 minutos.
:::

:::{tab-item} Paso 3: Medir
Calcular la absorbancia a 280 nm usando el espectrofotómetro.
:::
::::
````

Resultado:

::::{tab-set}
:::{tab-item} Paso 1: Preparar la muestra
Pesar 0.5 g del compuesto sólido con precisión de 0.001 g.
:::

:::{tab-item} Paso 2: Disolver
Añadir 50 mL de disolvente y agitar durante 5 minutos.
:::

:::{tab-item} Paso 3: Medir
Calcular la absorbancia a 280 nm usando el espectrofotómetro.
:::
::::

## Tarjetas (`{card}`)

Las tarjetas presentan información en bloques visuales:

````md
```{card} Práctica 1: Espectroscopía
Determinación de la concentración de proteínas mediante el método de Bradford.
+++
Semana 3
```
````

Resultado:

```{card} Práctica 1: Espectroscopía
Determinación de la concentración de proteínas mediante el método de Bradford.
+++
Semana 3
```

```{warning}
Las pestañas y tarjetas funcionan en **HTML** pero **no en PDF**. En PDF, el contenido de todas las pestañas se muestra secuencialmente.
```
