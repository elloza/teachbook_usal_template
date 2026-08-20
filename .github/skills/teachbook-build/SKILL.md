---
name: teachbook-build
description: >
  Compila el libro TeachBook generando una versión web HTML multi-idioma.
  Lee todos los archivos de contenido, los procesa y genera una web estática navegable.
  Trigger phrases: "compila", "compilar", "build", "genera web", "genera HTML",
  "construye el libro", "quiero ver cómo queda", "genera la versión web",
  "rebuild", "construir", "crear web".
---

# Skill: Compilar el Libro (Build HTML)

## Cuándo usar esta skill

- Después de crear o editar contenido (archivos `.md` o `.ipynb`).
- Para verificar que todo el contenido se renderiza correctamente.
- Antes de publicar cambios en GitHub Pages.
- Si se sospecha que algo está mal formateado.

## Qué hace `build_book.py`

1. **Detecta los idiomas** automáticamente buscando archivos `_config_<lang>.yml` en `book/`.
2. **Para cada idioma**, crea un proyecto temporal standalone, compila con `jupyter-book build`, y mueve el resultado.
3. **Genera `languages.json`** para el selector de idiomas en la interfaz web.
4. **Fusiona los assets estáticos** (CSS, JS, logos) de todos los idiomas en un `_static` global.
5. **Crea un `index.html`** raíz que redirige al idioma principal (español por defecto).
6. **Genera `.nojekyll`** para compatibilidad con GitHub Pages.
7. **Compila las diapositivas Slidev** si existe `slides/package.json`, generando hubs, decks y `_static/slides_manifest.json`.

## Ubicación de salida

```
book/_build/html/           ← Raíz del sitio web
├── index.html              ← Redirección al idioma principal
├── es/                     ← Versión en español
├── en/                     ← Versión en inglés
├── slides/                 ← Diapositivas Slidev publicadas
├── _static/                ← Assets compartidos (CSS, JS, imágenes)
│   └── slides_manifest.json ← Mapa página → deck contextual
└── .nojekyll               ← Para GitHub Pages
```

## Instrucciones para el agente

### Ejecutar la compilación

El agente DEBE usar el Python del entorno virtual (`.venv`), NO el Python del sistema:

Antes de compilar contenido nuevo o modificado, comprobar siempre la codificación para evitar que acentos y eñes aparezcan como caracteres rotos en HTML, PDF, consola o GitHub:

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/check_encoding.py` |
| Windows | `.venv\Scripts\python.exe scripts/check_encoding.py` |

Esta comprobación es obligatoria antes de publicar. Revisa archivos de contenido, notebooks, configuraciones, scripts, skills, fuentes de diagramas, workflows y textos sin extensión como `LICENSE` o `CODEOWNERS`. Si falla, corregir el archivo indicado antes de compilar o hacer commit.

Si se han añadido o cambiado imágenes, GIFs o logos, comprobar también que los assets estáticos son aptos para web/PDF:

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/optimize_static_assets.py --check` |
| Windows | `.venv\Scripts\python.exe scripts\optimize_static_assets.py --check` |

Si existe `slides/package.json` o se han tocado diapositivas, comprobar antes la integridad de Slidev:

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/check_slides_integrity.py` |
| Windows | `.venv\Scripts\python.exe scripts\check_slides_integrity.py` |

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/build_book.py` |
| Windows | `.venv\Scripts\python.exe scripts/build_book.py` |

`scripts/build_slides.py` compila varias decks en paralelo con un límite conservador de 2 jobs. Para equipos con poca memoria se puede forzar ejecución secuencial con `TEACHBOOK_SLIDEV_JOBS=1`; para CI o máquinas potentes se puede aumentar de forma controlada con `TEACHBOOK_SLIDEV_JOBS=<n>`.

### Si el build falla

1. **Verificar `_toc_<lang>.yml`**: Comprobar que la sintaxis YAML es correcta (indentación con 2 espacios, sin tabs).
2. **Verificar rutas de archivos**: Cada entrada `file:` en el TOC debe apuntar a un archivo real en `book/<lang>/`.
3. **Verificar `_config_<lang>.yml`**: Comprobar que no hay errores de sintaxis YAML.
4. **Verificar contenido**: Los archivos `.md` deben tener sintaxis MyST válida.
5. **Verificar codificación**: Ejecutar `scripts/check_encoding.py` siempre; si aparecen acentos, eñes, signos o comillas como caracteres raros, corregir el archivo fuente indicado por el script.
6. **Re-ejecutar**: Tras corregir, volver a ejecutar `build_book.py`.

### Errores comunes

| Error | Causa probable | Solución |
|---|---|---|
| `FileNotFoundError` en build | Un archivo referenciado en `_toc.yml` no existe | Crear el archivo faltante o corregir la ruta |
| `EISDIR` error | El TOC apunta a un directorio en vez de un archivo | Usar `file: ruta/al/archivo` sin la extensión `.md` |
| YAML parse error | Sintaxis YAML incorrecta en config o TOC | Revisar indentación (2 espacios) y comillas |
| Build exit code 1 | Contenido MyST con directivas mal cerradas | Revisar que los bloques ```` ```{directive} ```` estén bien cerrados |
| No aparece el botón Slides | Falta `_static/slides_manifest.json` o no existe deck/hub para el idioma | Ejecutar `scripts/check_slides_integrity.py` y `scripts/build_slides.py` |
| Slidev falla al compilar | Node/npm no instalado o dependencias de `slides/` sin instalar | Ejecutar `python scripts/setup_env.py --yes` y revisar la versión de Node |

## Después de la compilación

El resultado está en `book/_build/html/`. Se puede abrir `book/_build/html/index.html` en un navegador para verificar visualmente, o usar la skill `teachbook-live-preview` para una vista previa interactiva.

Si hay diapositivas, verificar además que existen `book/_build/html/slides/<lang>/` y `book/_build/html/_static/slides_manifest.json`, y que el botón superior `Slides` abre la deck contextual desde una página de capítulo o sección.
