# 2. Flujo de Trabajo

Este es el flujo de trabajo recomendado para tu TeachBook:

1. **Escribir contenido** en archivos Markdown (`.md`) o Notebooks (`.ipynb`). En el caso de los Notebooks, es importante ejecutarlos previamente para que el libro conserve la salida de las celdas. El agente de IA puede ayudarte a escribir el contenido y a ejecutar los Notebooks.
2. **Previsualizar** con `python scripts/launch_preview.py` para ver el mismo build que se publicará. En este curso puedes pedírselo al agente de IA, porque tiene la información necesaria para hacerlo por ti.
3. **Guardar versiones** con Git (`commit`). El agente de IA te ayudará a guardar los cambios de forma ordenada.
4. **Publicar** en GitHub (`push`) para que la web se actualice automáticamente mediante GitHub Pages.

## Ciclo de desarrollo del libro

1. Modificas o añades contenido en archivos Markdown o Notebooks.
2. Compilas el libro y levantas un servidor local para previsualizar los cambios.
3. Generas, si procede, las versiones PDF del libro. En ese proceso se crea primero LaTeX y después se compilan los PDFs que se enlazan desde la web.
4. Si todo está correcto, haces commit de los cambios con Git.
5. Publicas los cambios en GitHub para desplegar la web.
6. Si encuentras errores o quieres mejorar algo, vuelves al paso 1 y repites el ciclo.

La {numref}`fig-flujo-trabajo-teachbook` resume el proceso completo: escribir contenido, previsualizarlo, revisar el resultado, versionar los cambios y publicar la web.

```{figure} ../../_static/images/01_tutorial_02_flujo_trabajo_01_es.png
---
name: fig-flujo-trabajo-teachbook
alt: Infografía del flujo de trabajo para editar, previsualizar, versionar y publicar un TeachBook.
width: 90%
align: center
---
Flujo de trabajo de un TeachBook desde la edición del contenido hasta la publicación web.
```

## Estructura de archivos

Para trabajar con el libro, necesitaremos conocer la estructura de archivos y carpetas. El contenido se organiza por idioma, y cada idioma tiene su propio índice y configuración. Esto permite mantener versiones en varios idiomas con el mismo contenido o con contenido adaptado a cada idioma. Seguiremos la misma filosofía del proyecto original de TeachBooks, pero con algunas adaptaciones para facilitar su uso con asistentes de IA.

El contenido en español se organiza en `book/es/`. El contenido en inglés se organiza en `book/en/`. Cada idioma tiene su propio índice (`_toc_*.yml`) y configuración (`_config_*.yml`), pero la estructura debe mantenerse coherente entre idiomas.

Archivos y carpetas principales:

- `book/es/intro.md`: página principal de la versión en español.
- `book/en/intro.md`: página principal de la versión en inglés.
- `book/_toc_es.yml` y `book/_toc_en.yml`: índices del libro; definen el orden de capítulos y secciones.
- `book/_config_es.yml` y `book/_config_en.yml`: configuración específica de cada idioma.
- `book/_static/`: imágenes, vídeos, estilos, scripts y PDFs compartidos.
- `book/es/01_tutorial/` y `book/en/01_tutorial/`: carpetas del tutorial inicial.

Buenas prácticas para mantener el orden:

- Usa prefijos numéricos en carpetas y archivos (`01_`, `02_`, `03_`) para reflejar la secuencia.
- Añade cada archivo nuevo al TOC del idioma correspondiente; si no está en el TOC, no aparecerá en la navegación.
- Mantén nombres claros y consistentes, por ejemplo `03_actividad_experimental.md`.
- Cuando añadas o cambies contenido en español, revisa también la página equivalente en inglés.

Los resultados de la compilación se generan en `book/_build/html/`, que es la versión estática del libro que se publica en GitHub Pages. No es necesario modificar nada en esa carpeta, ya que se genera automáticamente a partir de los archivos fuente.

La carpeta `book/_static/` está destinada a archivos estáticos como imágenes, vídeos, estilos CSS, scripts JavaScript, PDFs y referencias. Puedes colocar tus imágenes ahí y referenciarlas desde los archivos Markdown usando rutas relativas. Si no sabes cómo hacerlo, el agente de IA puede ayudarte a colocar las imágenes y referenciarlas correctamente.

## Árbol de directorios

```text
teachbook_usal_template/
├── book/
│   ├── _config_es.yml
│   ├── _config_en.yml
│   ├── _toc_es.yml
│   ├── _toc_en.yml
│   ├── _static/
│   ├── _build/
│   ├── es/
│   │   ├── intro.md
│   │   └── 01_tutorial/
│   │       ├── 01_que_es_un_teachbook.md
│   │       └── 02_flujo_trabajo.md
│   └── en/
│       ├── intro.md
│       └── 01_tutorial/
│           ├── 01_what_is_a_teachbook.md
│           └── 02_workflow.md
└── scripts/
    └── launch_preview.py
```

