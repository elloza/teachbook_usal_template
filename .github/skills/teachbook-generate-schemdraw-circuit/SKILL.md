---
name: teachbook-generate-schemdraw-circuit
description: >
  Genera diagramas de circuitos eléctricos con Schemdraw para incluir en el libro como notebooks.
  Schemdraw es una librería Python que produce imágenes estáticas de circuitos (compatible HTML y PDF).
  Trigger phrases: "circuito", "schemdraw", "diagrama circuito", "resistencia", "capacitor",
  "inductor", "circuito eléctrico", "esquema eléctrico", "RC", "RL", "RLC".
---

# Skill: Generar Circuitos con Schemdraw

## Qué es Schemdraw

Schemdraw es una librería Python para dibujar diagramas de circuitos eléctricos. Genera imágenes estáticas (PNG/SVG), por lo que funciona tanto en HTML como en PDF.

Ya está incluido en `requirements.txt` del proyecto.

## Requisitos

- El circuito debe ir en un archivo **.ipynb** (Jupyter notebook).
- El notebook debe estar en la carpeta del idioma correspondiente (`book/es/...` o `book/en/...`).
- Para que el código se ejecute al compilar, `_config_<lang>.yml` debe tener `execute_notebooks: auto`.
- Si está en `off` (por defecto), los notebooks no se ejecutan y no se generarán las imágenes.

## Elementos disponibles

Se accede mediante `import schemdraw.elements as elm` y `import schemdraw.dsp as dsp`:

| Elemento | Módulo | Descripción |
|---|---|---|
| `elm.Battery` | elements | Pila/batería |
| `elm.Resistor` | elements | Resistencia |
| `elm.ResistorVar` | elements | Resistencia variable |
| `elm.Capacitor` | elements | Capacitor |
| `elm.Inductor` | elements | Inductor |
| `elm.Diode` | elements | Diodo |
| `elm.LED` | elements | LED |
| `elm.Wire` | elements | Cable |
| `elm.Dot` | elements | Punto de conexión |
| `elm.Ground` | elements | Tierra |
| `elm.Source` | elements | Fuente de tensión |
| `elm.MeterV` | elements | Voltímetro |
| `elm.MeterA` | elements | Amperímetro |

## Plantilla: Circuito RC serie

```python
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d += elm.Battery().up().label('V', loc='bot')
    d += elm.Resistor().right().label('R')
    d += elm.Capacitor().down().label('C')
    d += elm.Wire().left()
    d.draw()
```

## Plantilla: Circuito RL serie

```python
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d += elm.Source().up().label('V', loc='bot')
    d += elm.Resistor().right().label('R')
    d += elm.Inductor().down().label('L')
    d += elm.Wire().left()
    d.draw()
```

## Plantilla: Circuito con diodo

```python
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d += elm.Battery().up().label('V', loc='bot')
    d += elm.Resistor().right().label('R')
    d += elm.Diode().down().label('D')
    d += elm.Wire().left()
    d.draw()
```

## Estructura del notebook

El notebook debe seguir esta estructura de celdas:

1. **Celda markdown** — Título y descripción del circuito.
2. **Celda code** — Importar `schemdraw` y `schemdraw.elements`.
3. **Celda code** — Crear el circuito y mostrarlo.
4. **Celda markdown** — Explicación del resultado.

## Reglas

| Regla | Detalle |
|---|---|
| Formato | Siempre crear como **.ipynb** (no .md con código). |
| Imports | `import schemdraw` + `import schemdraw.elements as elm`. |
| Contexto | Usar `with schemdraw.Drawing() as d:` para agrupar elementos. |
| Etiquetas | Añadir `.label('nombre')` a cada componente. |
| Direcciones | `.up()`, `.down()`, `.left()`, `.right()` para orientar componentes. |
| Multi-idioma | Crear el notebook en TODOS los idiomas configurados. |
| Ejecución | Si `execute_notebooks: off`, avisar al usuario que debe activarlo o ejecutar manualmente. |

## Flujo de trabajo

1. Preguntar qué circuito necesita el usuario (RC, RL, RLC, con diodo, etc.).
2. Elegir la plantilla adecuada y adaptarla.
3. Crear el notebook `.ipynb` en la carpeta del idioma correspondiente.
4. Crear el mismo notebook en el/los otro/s idioma/s (con texto traducido).
5. Añadir la entrada al `_toc_<lang>.yml` de cada idioma.
6. Avisar sobre la configuración de `execute_notebooks`.
