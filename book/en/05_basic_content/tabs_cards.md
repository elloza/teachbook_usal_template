(tabs_cards)=
# Tabs and Cards

The **sphinx-design** extension (already installed) lets you organize content into tabs and cards. Ideal for comparing options, showing code in multiple languages, or presenting alternative steps.

## Simple tabs (`{tab-set}` / `{tab-item}`)

`````md
::::{tab-set}
:::{tab-item} Python
```python
print("Hello, world")
```
:::

:::{tab-item} R
```r
print("Hello, world")
```
:::

:::{tab-item} MATLAB
```matlab
disp('Hello, world')
```
:::
::::
`````

Result:

::::{tab-set}
:::{tab-item} Python
```python
print("Hello, world")
```
:::

:::{tab-item} R
```r
print("Hello, world")
```
:::

:::{tab-item} MATLAB
```matlab
disp('Hello, world')
```
:::
::::

## Grouped tabs (`{tab-set}` / `{tab-item}`)

Tab groups allow synchronization:

````md
::::{tab-set}
:::{tab-item} Analytical method
Solving the differential equation directly.
:::

:::{tab-item} Numerical method
Approximating the solution step by step with a computer.
:::
::::
````

Result:

::::{tab-set}
:::{tab-item} Analytical method
Solving the differential equation directly.
:::

:::{tab-item} Numerical method
Approximating the solution step by step with a computer.
:::
::::

## Tabs for procedure steps

````md
::::{tab-set}
:::{tab-item} Step 1: Prepare the sample
Weigh 0.5 g of the solid compound with 0.001 g precision.
:::

:::{tab-item} Step 2: Dissolve
Add 50 mL of solvent and stir for 5 minutes.
:::

:::{tab-item} Step 3: Measure
Read absorbance at 280 nm using the spectrophotometer.
:::
::::
````

Result:

::::{tab-set}
:::{tab-item} Step 1: Prepare the sample
Weigh 0.5 g of the solid compound with 0.001 g precision.
:::

:::{tab-item} Step 2: Dissolve
Add 50 mL of solvent and stir for 5 minutes.
:::

:::{tab-item} Step 3: Measure
Read absorbance at 280 nm using the spectrophotometer.
:::
::::

## Cards (`{card}`)

Cards present information in visual blocks:

````md
```{card} Lab 1: Spectroscopy
Determination of protein concentration using the Bradford method.
+++
Week 3
```
````

Result:

```{card} Lab 1: Spectroscopy
Determination of protein concentration using the Bradford method.
+++
Week 3
```

```{warning}
Tabs and cards work in **HTML** but **not in PDF**. In PDF, the content of all tabs is shown sequentially.
```
