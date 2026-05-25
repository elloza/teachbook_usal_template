(tables)=
# Tables

Tables are the most direct way to present structured data. MyST supports standard Markdown tables and the `{table}` directive for adding numbering.

## Simple Markdown table

```md

The following table summarizes the main elements of this section.

**Table. Simple Markdown table.**

| Element | Symbol | Atomic number |
|---------|--------|---------------|
| Hydrogen | H     | 1             |
| Helium   | He    | 2             |
| Lithium  | Li    | 3             |
```

Result:


The following table summarizes the main elements of this section.

**Table. Simple Markdown table.**

| Element | Symbol | Atomic number |
|---------|--------|---------------|
| Hydrogen | H     | 1             |
| Helium   | He    | 2             |
| Lithium  | Li    | 3             |

## Numbered table with caption

Use `{table}` for automatic numbering and cross-referencing:

````md
```{table} Common laboratory solvents
:name: tab-solvents
:align: center

| Solvent | Formula | Boiling point (°C) |
|---------|---------|---------------------|
| Water   | H₂O     | 100                 |
| Ethanol | C₂H₅OH  | 78                  |
| Acetone | CH₃COCH₃| 56                  |
| Ether   | C₄H₁₀O  | 35                  |
```
````

Result:

```{table} Common laboratory solvents
:name: tab-solvents
:align: center

| Solvent | Formula | Boiling point (°C) |
|---------|---------|---------------------|
| Water   | H₂O     | 100                 |
| Ethanol | C₂H₅OH  | 78                  |
| Acetone | CH₃COCH₃| 56                  |
| Ether   | C₄H₁₀O  | 35                  |
```

## List-table directive

MyST does not support per-column alignment in Markdown tables. Use `{list-table}` for more control:

````md
```{list-table} Experimental data
:header-rows: 1
:name: tab-list-en
:align: center

* - Sample
  - pH
  - Conductivity (mS/cm)
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

Result:

```{list-table} Experimental data
:header-rows: 1
:name: tab-list-en
:align: center

* - Sample
  - pH
  - Conductivity (mS/cm)
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

## Tips for readable tables

- **Fewer than 6 columns**: wide tables are hard to read on screen.
- **Align numbers**: makes visual comparison easier.
- **Units in the header**: do not repeat units in each cell.
- **Long tables**: if you exceed 15 rows, consider using a chart instead.

```{tip}
The {numref}`tab-solvents` shows an example with units in the header. Notice how numeric columns make comparison easier.
```
