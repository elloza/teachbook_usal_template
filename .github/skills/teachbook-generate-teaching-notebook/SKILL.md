---
name: teachbook-generate-teaching-notebook
description: >
  Crea notebooks de Jupyter orientados a la enseñanza con estructura pedagógica clara.
  Incluye plantillas JSON para generar archivos .ipynb correctos y reglas de diseño docente.
  Trigger phrases: "notebook", "jupyter", "cuaderno", "ejemplo python", "código ejecutable",
  "notebook de enseñanza", "notebook interactivo", "código python", "simulación".
---

# Skill: Generar Notebooks de Enseñanza

## Qué es un notebook de enseñanza

Un Jupyter Notebook (`.ipynb`) que combina explicaciones en markdown con código Python ejecutable. Está diseñado para que un estudiante lo siga paso a paso.

## Estructura obligatoria

Cada notebook debe seguir este orden de celdas:

1. **Celda título** (markdown) — Nombre del tema y objetivo de aprendizaje.
2. **Celda explicación** (markdown) — Contexto teórico breve (2-5 líneas).
3. **Celda código** (code) — El ejemplo con comentarios en cada línea relevante.
4. **Celda interpretación** (markdown) — Qué significan los resultados.
5. **Celda ejercicio** (markdown) — 1-2 ejercicios propuestos para el estudiante.

## Estructura JSON de un notebook

```json
{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": ["# Título del Notebook\n\n**Objetivo:** Describir qué aprenderá el estudiante."]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": ["import numpy as np\nimport matplotlib.pyplot as plt\n\n# Generar datos de ejemplo\nx = np.linspace(0, 2 * np.pi, 100)\ny = np.sin(x)\n\n# Visualizar\nplt.figure(figsize=(8, 4))\nplt.plot(x, y, label='sin(x)')\nplt.title('Funcion seno')\nplt.xlabel('x')\nplt.ylabel('y')\nplt.legend()\nplt.grid(True)\nplt.show()"]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": ["## Interpretación\n\nLa gráfica muestra un ciclo completo de la función seno."]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": ["## Ejercicio\n\n1. Modifica el código para graficar `cos(x)` en lugar de `sen(x)`.\n2. ¿Qué ocurre si cambias el rango de `x` a `[0, 4π]`?"]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.10.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}
```

## Reglas de diseño docente

| Regla | Detalle |
|---|---|
| Celdas cortas | **Un concepto por celda**. Máximo 10-15 líneas de código por celda. |
| Comentarios | Comentar las líneas clave del código (no todas, solo las que aportan valor) y escribirlos en ASCII. |
| Resultados explícitos | Usar `print()` para mostrar resultados numéricos, no depender del output automático. |
| Visualizaciones | Usar `matplotlib.pyplot` para gráficas. Siempre con `title`, `xlabel`, `ylabel`, y texto ASCII en títulos/ejes/leyendas. |
| Datos autogenerados | Usar `numpy` para generar datos. **Nunca** requerir archivos externos. |
| Extensión | Mantener entre **3 y 6 celdas** como máximo por notebook. |
| Kernel | Siempre usar kernel `python3`. |
| Imports | Agrupar todos los imports en la primera celda de código. |

## Regla crítica de codificación en celdas de código

Las celdas `code` de un notebook deben ser **ASCII-safe** aunque el Markdown esté en español.
Motivo: el código fuente visible y las figuras generadas con Matplotlib pasan por HTML, PDF, fuentes del sistema y visores distintos. Caracteres como letras con tilde, eñes, símbolos griegos, superíndices, subíndices o flechas pueden acabar como `?` en ejes, títulos, leyendas o bloques de código.

Aplicar siempre:

- En celdas Markdown: se permiten acentos y texto normal en español.
- En celdas `code`: usar ASCII en comentarios, `print()`, strings, títulos, ejes, leyendas y nombres de variables.
- En Matplotlib: escribir `plt.title("Funcion seno")`, no `plt.title("Función seno")`.
- Para símbolos: usar texto ASCII (`Ohm`, `pi`, `Delta`, `uF`, `tau`, `x^2`) o mathtext de Matplotlib cuando sea necesario (`r"$x^2$"`, `r"$\pi$"`).
- Tras crear o modificar notebooks, ejecutar y guardar outputs con `.venv`, y luego validar:

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/check_encoding.py` |
| Windows | `.venv\Scripts\python.exe scripts/check_encoding.py` |

Si `scripts/check_encoding.py` detecta una celda de código con texto no ASCII, hay que corregirla antes de compilar o commitear.

## Configuración de ejecución

Los notebooks se ejecutan (o no) según la configuración en `_config_<lang>.yml`:

| Valor | Comportamiento |
|---|---|
| `off` (por defecto) | No se ejecuta. Las celdas muestran el código pero sin output. |
| `auto` | Se ejecuta al compilar. Los outputs se generan automáticamente. |
| `force` | Fuerza ejecución aunque ya tenga outputs. |

Si `execute_notebooks: off`, hay dos opciones:
1. **Activar ejecución**: cambiar a `auto` en el config (más lento al compilar).
2. **Dejar outputs manuales**: ejecutar el notebook localmente y guardarlo con los outputs ya generados.

## Librerías disponibles

Estas librerías no se instalan en la base ligera. Antes de ejecutar o regenerar notebooks científicos, instalar el extra:

```bash
python scripts/setup_env.py --yes --extras notebooks
```

Después se pueden usar:

- `numpy` — Cálculo numérico y generación de datos.
- `matplotlib` — Gráficas y visualizaciones.
- `scipy` — Cálculo científico avanzado.
- `schemdraw` — Diagramas de circuitos (ver skill teachbook-generate-schemdraw-circuit).
- `sympy` — Matemáticas simbólicas.

## Flujo de trabajo

1. Preguntar qué tema debe cubrir el notebook y para qué asignatura/grado.
2. Diseñar la estructura de celdas siguiendo la plantilla.
3. Generar el JSON del `.ipynb` y guardarlo en la carpeta del idioma.
4. Repetir para el/los otro/s idioma/s.
5. Añadir al `_toc_<lang>.yml` correspondiente.
6. Verificar la configuración de `execute_notebooks`.
