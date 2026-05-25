---
name: teachbook-add-content
description: >
  Guía paso a paso para añadir nuevos capítulos o secciones al libro.
  Garantiza que el contenido se crea en TODOS los idiomas y que los TOC se mantienen sincronizados.
  Es la skill MÁS CRÍTICA del proyecto: un error aquí rompe la estructura multi-idioma.
  Trigger phrases: "añadir capítulo", "nueva sección", "nuevo contenido", "agregar contenido",
  "add chapter", "add content", "nueva página", "crear sección", "nuevo apartado",
  "añadir grado", "nuevo ejemplo".
---

# Skill: Añadir Contenido (Capítulos y Secciones)

## REGLA OBLIGATORIA

> Todo contenido debe existir en **TODOS los idiomas** configurados. Si se añade un archivo en español, DEBE existir el equivalente en inglés (y viceversa). Los cambios de contenido + TOC deben ir en el mismo commit.

> **Puerta de cierre obligatoria:** antes de decir “listo”, el agente DEBE comprobar que el menú lateral y los archivos visibles tienen correspondencia en todos los idiomas. Si hay más de un idioma configurado, no se puede cerrar un cambio de contenido sin ejecutar `python scripts/check_multilang_integrity.py` con el Python de `.venv` y obtener resultado correcto.

> Toda tabla, figura, imagen, diagrama, circuito, vídeo o recurso visual/tabular que forme parte del discurso docente debe tener un **título/caption escueto** y debe estar **referenciado explícitamente en el texto**. No basta con “ponerlo ahí”: el estudiante debe saber por qué aparece y cuándo mirarlo.

> Todo asset nuevo en `book/_static/` debe mantener formatos seguros para web y PDF. PNG/JPG/SVG son la base estable; WebP solo como mejora HTML con fallback. Tras añadir imágenes o GIFs, ejecutar `python scripts/optimize_static_assets.py --check` y corregir fallbacks GIF si faltan.

> Toda sección nueva con citas bibliográficas debe decidir el alcance antes de escribir: **global por defecto** con `{cite:t}` / `{cite:p}` y la página final `Bibliografía` / `Bibliography` con `:cited:`, o **local solo si el usuario lo pide** con `{bibliography}` filtrada dentro de `{only} html`. En PDF no se generan bibliografías locales por página; `export_pdf.py` crea un `.bib` temporal con las citas usadas.

> Si una cita está asociada a contenido `{raw} html`, no la dejes solo dentro del HTML crudo. Para que aparezca en la bibliografía final del PDF, pon la cita en Markdown normal o añade `\cite{clave}` dentro del fallback `{raw} latex`.

> **Codificación obligatoria:** todo archivo de contenido, configuración, notebook, script o skill debe guardarse como **UTF-8**. No se admite mojibake, caracteres de reemplazo (`U+FFFD`) ni sustituir letras con tilde por `?`. Antes de cerrar cambios de contenido, ejecutar `python scripts/check_encoding.py` o `python scripts/check_multilang_integrity.py` con el Python de `.venv`.

## Regla obligatoria de captions y referencias

Cuando añadas contenido nuevo, aplica esta norma en **TODOS los idiomas**:

1. **Cada elemento visual o tabular debe tener título/caption breve.**
   - Bueno: “Circuito RC de carga y descarga.”
   - Malo: “Figura” o un bloque visual sin explicación.
2. **Cada elemento debe citarse en el texto cercano.**
   - ES: “Como muestra la {numref}`fig-circuito-rc`, la resistencia y el condensador forman una etapa de carga.”
   - EN: “As shown in {numref}`fig-rc-circuit`, the resistor and capacitor form a charging stage.”
3. **Usa directivas con caption cuando el elemento sea parte de la explicación.**
   - Imágenes/diagramas renderizados: preferir `{figure}` con `name` y caption.
   - Diagramas Kroki: usar `{kroki}` con `:type:` y añadir antes una frase de referencia + un título textual en negrita. En esta plantilla **NO uses `{kroki-figure}`**: no está disponible en el build actual.
   - Tablas: añadir un título textual escueto antes de la tabla o usar una directiva MyST con caption cuando se necesite referencia formal.
4. **Evita `{image}` para contenido que se vaya a comentar o citar.** `{image}` sirve para elementos decorativos o logos; para contenido docente usa `{figure}`.
5. **La referencia debe aportar sentido.** No escribir “ver figura” como relleno: explica qué debe observar el estudiante.

## Regla obligatoria de bibliografía global/local

El proyecto usa `book/_static/references.bib` como archivo BibTeX común para todos los idiomas.

### Modo global por defecto

- Usa `{cite:t}` o `{cite:p}` dentro del contenido.
- No añadas `{bibliography}` al final de páginas normales.
- La única página global de bibliografía debe mantener:

````markdown
```{bibliography}
:cited:
```
````

### Modo local solo si se pide y solo para HTML

- Usa `{cite:t}` o `{cite:p}` dentro de la página.
- Deja las citas en el texto normal si deben contar para el PDF y envuelve solo `{bibliography}` con filtro dentro de `{only} html`:

`````markdown
Texto con cita local {cite:p}`clave_cita`.

````{only} html
## Bibliografía de esta página

```{bibliography}
:filter: docname in docnames
```
````
`````

Para una bibliografía local parcial, se puede filtrar por claves dentro del mismo bloque HTML:

`````markdown
````{only} html
```{bibliography}
:filter: docname in docnames and key in {"clave1", "clave2"}
```
````
`````

- Como la página global con `:cited:` puede repetir entradas ya mostradas localmente en HTML, los `_config_<lang>.yml` deben mantener `suppress_warnings: ["bibtex.duplicate_citation"]`.
- El modo local funciona solo en HTML. En PDF debe aparecer únicamente la bibliografía global final generada desde el `.bib` temporal de citas usadas.
- La repetición en HTML entre bibliografía local y global es aceptable; no intentes eliminar la página global para evitarla si el libro necesita bibliografía completa.

### Citas en bloques raw HTML/LaTeX

- `{raw} html` no se imprime en PDF. Las citas escritas solo ahí no alimentan la bibliografía final del PDF.
- Si el contenido HTML necesita una referencia en PDF, añadir fallback `{raw} latex` con `\cite{clave}`.
- `scripts/collect_used_bibliography.py` valida esas citas LaTeX y `scripts/export_pdf.py` las incluye en el `.bib` temporal usado por la página final `Bibliografía` / `Bibliography`.

### Verificación obligatoria con citas

Tras añadir o modificar citas:

1. Confirmar que todas las claves existen en `book/_static/references.bib`.
2. Validar con `python scripts/collect_used_bibliography.py --lang es` y el idioma equivalente que corresponda.
3. Compilar HTML y revisar que no aparezca `could not find bibtex key`.
4. Si se exporta PDF, comprobar que los PDFs de todos los idiomas se generan de nuevo.

### Ejemplo recomendado — figura en español

````markdown
Como muestra la {numref}`fig-circuito-rc`, el condensador se carga a través de la resistencia.

```{figure} ../../../_static/generated/circuito_rc.png
---
name: fig-circuito-rc
width: 70%
align: center
---
Circuito RC de carga y descarga.
```
````

### Recommended example — figure in English

````markdown
As shown in {numref}`fig-rc-circuit`, the capacitor charges through the resistor.

```{figure} ../../../_static/generated/rc_circuit.png
---
name: fig-rc-circuit
width: 70%
align: center
---
RC charging and discharging circuit.
```
````

### Ejemplo recomendado — diagrama Kroki

````markdown
El diagrama siguiente resume el flujo básico del proceso experimental.

**Diagrama. Flujo básico del proceso experimental.**

```{kroki}
:type: mermaid
:align: center

flowchart LR
    A[Pregunta] --> B[Experimento]
    B --> C[Datos]
    C --> D[Conclusión]
```
````

### Ejemplo recomendado — tabla sencilla

```markdown
La Tabla 1 resume qué herramienta conviene usar según el tipo de material.

**Tabla 1. Herramientas recomendadas por tipo de recurso.**

| Recurso | Herramienta recomendada |
|---|---|
| Diagrama de flujo | Kroki/Mermaid |
| Circuito eléctrico simple | Schemdraw |
| Circuito eléctrico preciso | CircuitikZ local |
```

## Recomendación clave para primeros usos

Cuando un docente o estudiante quiera "dejar el libro solo con un capítulo" para empezar, **NO recomendar borrar contenido de ejemplo a la primera**.

La estrategia recomendada es:

1. **ocultar** temporalmente capítulos o secciones en los `_toc_<lang>.yml`
2. **mantener los archivos `.md` / `.ipynb` en el repo** como referencia reutilizable
3. documentar con un comentario YAML qué se ha ocultado y por qué

Esto permite:

- empezar con un libro pequeño y limpio
- conservar ejemplos listos para copiar/adaptar
- volver a activarlos más adelante sin reconstruir nada

## Patrón recomendado: ocultar sin borrar

### Opción preferida

Comentar en el TOC las entradas que no se quieren mostrar todavía.

Ejemplo en `_toc_es.yml`:

```yaml
  - caption: Ejemplos por Grado
    chapters:
    - file: es/02_grados/grado_fisica/intro
      sections:
      - file: es/02_grados/grado_fisica/ejemplo_fisica
    # Contenido oculto temporalmente para primer arranque del curso:
    # - file: es/02_grados/grado_matematicas/intro
    #   sections:
    #   - file: es/02_grados/grado_matematicas/ejemplo_matematicas
    # - file: es/02_grados/grado_estadistica/intro
    #   sections:
    #   - file: es/02_grados/grado_estadistica/ejemplo_estadistica
```

Y el mismo patrón en `_toc_en.yml`.

### Regla

- **Ocultar en TODOS los idiomas** al mismo tiempo
- **NO borrar** archivos de contenido de referencia salvo que el usuario lo pida explícitamente
- añadir comentario tipo:
  - `# Contenido oculto temporalmente para usar esta plantilla como base mínima`

## Cuándo sugerir ocultar en vez de borrar

Sugerir esta opción si el usuario dice cosas como:

- "quiero empezar solo con una página"
- "quiero quitar todo lo demás por ahora"
- "solo quiero quedarme con un capítulo"
- "me abruma el contenido de ejemplo"

En esos casos, el agente debe proponer algo así:

> "Puedo quitarlo del menú y dejarlo oculto en el TOC para que no se vea, pero mantenerlo en el repo como referencia por si luego quieres reutilizarlo. Es más seguro que borrarlo del todo."

## Proceso paso a paso

### Paso 1: Identificar qué se va a añadir

Determinar ANTES de escribir nada:
- ¿Es un **capítulo nuevo** (entrada directa en `chapters:`) o una **sección** dentro de un capítulo existente (entrada en `sections:`)?
- ¿En qué **parte** del TOC va? (Tutorial, Ejemplos por Grado, Información...)
- ¿Cuál es el **nombre del archivo** y la **ruta** en cada idioma?
- ¿El usuario quiere **añadir**, **reordenar**, **ocultar temporalmente** o **eliminar definitivamente**?
- ¿Habrá citas bibliográficas? Si las hay, usar bibliografía global por defecto o bibliografía local con `{bibliography}` filtrada dentro de `{only} html` solo si el usuario lo pide.

### Paso 2: Crear los archivos de contenido en TODOS los idiomas

Los archivos se crean SIN la extensión `.md` en el TOC, pero el archivo físico SÍ la lleva.

**Ejemplo: Añadir "Grado Biología"**

Crear el directorio y archivos en español:
```
book/es/02_grados/grado_biologia/intro.md
book/es/02_grados/grado_biologia/ejemplo_biologia.md
```

Crear el directorio y archivos en inglés:
```
book/en/02_degrees/biology_degree/intro.md
book/en/02_degrees/biology_degree/biology_example.md
```

**Si la traducción no está lista aún**, crear el archivo con:
```markdown
*(Traducción pendiente)*
```

### Paso 3: Actualizar TODOS los `_toc_<lang>.yml`

**Los cambios deben ser IDÉNTICOS en estructura** en todos los idiomas (mismo orden, mismas secciones).

Si el objetivo es **ocultar** contenido existente, comentar las entradas en ambos TOCs en vez de borrarlas, salvo instrucción explícita del usuario para eliminación definitiva.

#### `_toc_es.yml` — Añadir dentro de la parte "Ejemplos por Grado":

```yaml
  - caption: Ejemplos por Grado
    chapters:
    - file: es/02_grados/grado_fisica/intro
      sections:
      - file: es/02_grados/grado_fisica/ejemplo_fisica
    - file: es/02_grados/grado_matematicas/intro
      sections:
      - file: es/02_grados/grado_matematicas/ejemplo_matematicas
    - file: es/02_grados/grado_estadistica/intro
      sections:
      - file: es/02_grados/grado_estadistica/ejemplo_estadistica
    - file: es/02_grados/grado_biologia/intro        # ← NUEVO
      sections:
      - file: es/02_grados/grado_biologia/ejemplo_biologia  # ← NUEVO
```

#### `_toc_en.yml` — Mismo cambio, rutas en inglés:

```yaml
  - caption: Examples by Degree
    chapters:
    - file: en/02_degrees/physics_degree/intro
      sections:
      - file: en/02_degrees/physics_degree/physics_example
    - file: en/02_degrees/math_degree/intro
      sections:
      - file: en/02_degrees/math_degree/math_example
    - file: en/02_degrees/stats_degree/intro
      sections:
      - file: en/02_degrees/stats_degree/stats_example
    - file: en/02_degrees/biology_degree/intro        # ← NUEVO
      sections:
      - file: en/02_degrees/biology_degree/biology_example  # ← NUEVO
```

### Reglas de formato del TOC

| Regla | Detalle |
|---|---|
| Indentación | **2 espacios** por nivel (NUNCA tabs) |
| Capítulos | `- file: ruta/sin/extension` (sin `.md`) |
| Secciones | Debajo del capítulo, con `sections:` y luego `- file: ...` |
| `root` | Solo el archivo raíz del libro (ej: `es/intro`) |
| Orden | Los idiomas deben tener la MISMA estructura en el MISMO orden |

### Paso 4: Verificar integridad

El agente DEBE ejecutar estas verificaciones ANTES de commit:

1. Ejecutar la comprobación automática de codificación:

   | Sistema | Comando |
   |---|---|
   | Linux / macOS | `.venv/bin/python scripts/check_encoding.py` |
   | Windows | `.venv\Scripts\python.exe scripts\check_encoding.py` |

   Este check es estricto y debe pasarse en local antes de publicar: valida contenido, notebooks, scripts, skills, workflows, fuentes de diagramas y archivos de texto sin extensión. Si informa de mojibake, caracteres de reemplazo, `?` dentro de palabras o texto no ASCII en celdas `code`, corregir el archivo antes de seguir.

2. Ejecutar la comprobación automática multi-idioma:

   | Sistema | Comando |
   |---|---|
   | Linux / macOS | `.venv/bin/python scripts/check_multilang_integrity.py` |
   | Windows | `.venv\Scripts\python.exe scripts/check_multilang_integrity.py` |

3. Si se han añadido o cambiado imágenes, vídeos o GIFs, validar assets estáticos:

   | Sistema | Comando |
   |---|---|
   | Linux / macOS | `.venv/bin/python scripts/optimize_static_assets.py --check` |
   | Windows | `.venv\Scripts\python.exe scripts\optimize_static_assets.py --check` |

4. Confirmar que cada `_toc_<lang>.yml` tiene la **misma forma**: mismas partes, mismos capítulos, mismas secciones y mismo orden.
5. Confirmar que cada entrada `file:` apunta a un archivo `.md` o `.ipynb` existente.
6. Confirmar que no hay archivos huérfanos en `book/<lang>/` fuera del TOC.
7. **Reportar** cualquier diferencia de menú, archivo huérfano, entrada rota, problema de codificación o asset estático sin fallback. No ocultes el problema.

La comprobación automática es obligatoria aunque el cambio parezca pequeño. En un libro multi-idioma, “solo he tocado una página” puede romper el menú lateral de otro idioma.

**Importante**: un archivo ocultado deliberadamente al comentar su entrada en el TOC **NO cuenta como error** si el usuario pidió conservarlo como referencia.

### Paso 5: Compilar para verificar

El agente DEBE usar el Python del entorno virtual (`.venv`):

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/build_book.py` |
| Windows | `.venv\Scripts\python.exe scripts/build_book.py` |

Si la compilación falla, revisar los errores y corregir antes de continuar.

### Paso 6: Commitear todo junto

Los cambios de contenido (archivos `.md`) + cambios de estructura (`_toc_*.yml`) deben ir en el **mismo commit**.

## Para añadir un nuevo idioma

Si se necesita un idioma completamente nuevo (ej: portugués `pt`):

1. Crear `book/_config_pt.yml` (copiar de `_config_es.yml` y adaptar).
2. Crear `book/_toc_pt.yml` (misma estructura que `_toc_es.yml`).
3. Crear `book/pt/` con TODO el contenido traducido (misma estructura de carpetas).
4. Crear `latex_templates/pt/language_support.tex` si se quiere PDF.
5. Añadir `"pt": "Português"` al mapa `LANG_DISPLAY_NAMES` en `scripts/build_book.py`.

## Resumen práctico para el agente

| Caso | Acción recomendada |
|---|---|
| Añadir capítulo nuevo | Crear archivos en todos los idiomas + actualizar TOCs |
| Reordenar capítulos | Cambiar el orden en todos los TOCs |
| Ocultar temporalmente contenido de ejemplo | **Comentar entradas en todos los TOCs** y conservar archivos |
| Borrar contenido definitivamente | Solo si el usuario lo pide explícitamente |
