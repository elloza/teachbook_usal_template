---
name: teachbook-generate-circuitikz
description: >
  Genera circuitos precisos con CircuitikZ como flujo avanzado: compila LaTeX con Tectonic,
  exporta una imagen PNG y la inserta en el libro con `{figure}`. Compatible con HTML y PDF.
  Trigger phrases: "circuitikz", "circuito latex", "esquema latex", "circuito preciso",
  "circuito avanzado", "tikz circuito".
---

# Skill: Generar Circuitos con CircuitikZ

## Qué es CircuitikZ

CircuitikZ es la opción **avanzada** para dibujar circuitos eléctricos con calidad LaTeX. Produce esquemas muy precisos y profesionales.

## Cuándo usarlo

- **Usa SchemDraw** si quieres la opción más simple y rápida.
- **Usa CircuitikZ** si necesitas un acabado más formal, estilo artículo científico o apuntes técnicos avanzados.

## Flujo recomendado en TeachBook

No insertes `raw latex` directamente en la página como flujo principal.

Haz esto:

1. Crea un archivo `.tex` con el código CircuitikZ.
2. Ejecuta:

```bash
python scripts/render_circuitikz.py ruta/al/circuito.tex book/_static/generated/circuito.png
```

3. Inserta la imagen en tu página MyST con `{figure}`.

Así funciona tanto en **HTML** como en **PDF**.

## Ejemplo de fuente CircuitikZ

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

## Inserción en MyST

```md
```{figure} _static/generated/rc_circuit.png
:alt: Circuito RC generado con CircuitikZ
:width: 70%
:align: center

Circuito RC generado con CircuitikZ.
```
```

## Requisitos

- Tener **Tectonic** instalado:

```bash
python scripts/setup_latex.py
```

- Tener **PyMuPDF** disponible (ya viene con el proyecto en la práctica si el entorno está bien preparado).

## Reglas

| Regla | Detalle |
|---|---|
| Opción avanzada | Recomendado solo cuando SchemDraw se quede corto |
| Salida final | Siempre convertir a imagen PNG y usar `{figure}` |
| HTML + PDF | La imagen final funciona en ambos formatos |
| Multi-idioma | Si añades contenido nuevo, crea también la versión en todos los idiomas |
| Trazabilidad | Guarda la fuente `.tex` si el circuito se va a reutilizar o editar |

## Flujo de trabajo

1. Preguntar qué circuito necesita el usuario.
2. Generar el archivo `.tex` de CircuitikZ.
3. Renderizarlo con `scripts/render_circuitikz.py`.
4. Insertar la imagen resultante con `{figure}`.
5. Mantener el archivo fuente `.tex` si el usuario puede querer editarlo después.
