# CircuitikZ Avanzado para Circuitos Precisos

**CircuitikZ** es la opción avanzada para dibujar circuitos con calidad LaTeX. Si quieres esquemas muy precisos, estilo apuntes técnicos o artículo científico, esta es la herramienta adecuada.

```{admonition} Recomendación práctica
:class: tip
Usa **SchemDraw** para la mayoría de ejemplos docentes. Usa **CircuitikZ** cuando necesites un acabado más formal y preciso.
```

## Flujo recomendado en TeachBook

En este proyecto, CircuitikZ no se inserta directamente como `raw latex` en la página. En su lugar:

1. Escribes el circuito en un archivo `.tex`
2. Lo conviertes a imagen con un script
3. Insertas la imagen con `{figure}`

Así funciona tanto en HTML como en PDF.

## Ejemplo de archivo fuente

Archivo `rc_circuit.tex`:

```tex
\begin{circuitikz}
\draw
  (0,0) to[battery1,l=$V$] (0,3)
  to[R,l=$R$] (3,3)
  to[C,l=$C$] (3,0)
  -- (0,0);
\end{circuitikz}
```

## Comando para renderizar

```bash
python scripts/render_circuitikz.py rc_circuit.tex book/_static/generated/rc_circuit.png
```

## Inserción en la página MyST

```md
```{figure} ../../../_static/generated/rc_circuit.png
:alt: Circuito RC generado con CircuitikZ
:width: 70%
:align: center
:name: fig-circuitikz-avanzado-1

Circuito RC generado con CircuitikZ.
```
```

## Resultado renderizado


El {numref}`fig-circuitikz-avanzado-2` resume visualmente esta parte de la explicación.

```{figure} ../../../_static/generated/circuito_rc_circuitikz.png
:alt: Circuito RC generado con CircuitikZ
:width: 70%
:align: center
:name: fig-circuitikz-avanzado-2

Circuito RC generado desde un archivo `.tex` con CircuitikZ y convertido a imagen PNG.
```

La ventaja de este flujo es que el circuito final se comporta como una imagen normal: se ve en la web, se incluye en el PDF y no depende de que el lector tenga instalado LaTeX.

## Cuándo usar CircuitikZ

- esquemas eléctricos formales
- apuntes avanzados de electrónica
- material con acabado tipo artículo o informe técnico

## Cuándo usar SchemDraw en su lugar

- ejemplos rápidos de clase
- material introductorio
- situaciones en las que quieras modificar el circuito con menos fricción

## Requisito previo

Si aún no tienes Tectonic instalado:

```bash
python scripts/setup_latex.py --yes
```
