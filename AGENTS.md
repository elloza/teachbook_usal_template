# Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial — Instrucciones para el Agente

## Objetivo del Proyecto

Material del curso **Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial** y plantilla para que docentes NO informáticos creen libros interactivos con Jupyter Book / TeachBooks.
El usuario típico es un profesor de las Facultades de Ciencias y de Ciencias Químicas (USAL) que **nunca ha usado un terminal**.
Tu trabajo es que TODO funcione con fricción CERO.

## Reglas de Oro

1. **SIEMPRE** usa el entorno virtual `.venv`. Nunca instales paquetes en el Python global.
2. **Requiere Python 3.12**. `scripts/setup_env.py` crea `.venv` con Python 3.12 mediante `uv`; si `.venv` existe con otra versión, para y muestra diagnóstico.
3. **Acción > Explicación**. Ejecuta los scripts, no des clases de informática.
4. **Responde en español** siempre (salvo que te pidan lo contrario).
5. **No añadas frameworks JS** (React, Vue, etc.). El sistema de build es Jupyter Book, punto.
6. **No rompas la estructura multi-idioma**. Si añades contenido en un idioma, DEBE existir en TODOS los idiomas configurados.
7. **No crees entornos alternativos** (`.venv_linux`, `.venv2`, `/tmp/venv`, etc.). Si `.venv` no corresponde al sistema actual, para y muestra diagnóstico.
8. **Codificación UTF-8 siempre**. Todos los `.md`, `.ipynb`, `.yml`, `.py`, `.tex`, `.bib`, `.js`, `.css` y skills deben guardarse como UTF-8. Nunca escribas texto con mojibake, caracteres de reemplazo (`U+FFFD`) ni sustituyas acentos por `?`. Antes de cerrar cambios de contenido, ejecuta `python scripts/check_encoding.py` o `python scripts/check_multilang_integrity.py`.
9. **Celdas de código ASCII-safe**. En notebooks, el Markdown puede llevar acentos, pero las celdas `code` deben usar ASCII en comentarios, `print()`, títulos/ejes/leyendas de Matplotlib y strings visibles. Usa `Ohm`, `pi`, `Delta`, `uF`, `tau`, `x^2` o mathtext (`r"$x^2$"`) en lugar de símbolos Unicode dentro del código.
10. **Assets web seguros**. PNG/JPG/SVG son formatos estables para HTML/PDF. No cambies referencias a WebP de forma general salvo que exista fallback PNG/JPG y se haya probado el PDF. Tras añadir imágenes o GIFs, ejecuta `python scripts/optimize_static_assets.py --check`; usa `--fix` solo para optimización conservadora de PNG/JPG.

## Arquitectura del Proyecto

```
teachbook_usal_template/
├── book/                          # Contenido del libro
│   ├── _config_es.yml             # Configuración español (idioma principal)
│   ├── _config_en.yml             # Configuración inglés
│   ├── _toc_es.yml                # Tabla de contenidos español
│   ├── _toc_en.yml                # Tabla de contenidos inglés
│   ├── _static/                   # Assets estáticos (CSS, JS, logos, PDFs)
│   │   ├── custom.css
│   │   ├── custom.js
│   │   ├── logo.png
│   │   ├── usal_logo.png
│   │   └── references.bib         # Bibliografía BibTeX
│   ├── es/                        # Contenido en español
│   │   ├── intro.md
│   │   ├── 01_tutorial/           # Sección tutorial
│   │   ├── 02_grados/             # Sección ejemplos por grado
│   │   ├── 90_acerca_de.md
│   │   ├── 91_licencias.md
│   │   └── 92_como_citar.md
│   └── en/                        # Contenido en inglés (misma estructura)
├── scripts/                       # Scripts de automatización
│   ├── setup_env.py               # Configuración del entorno
│   ├── build_book.py              # Compilación HTML
│   ├── launch_preview.py          # Lanzador seguro de vista previa para personas/agentes
│   ├── preview_book.py            # Vista previa usando el MISMO build que producción
│   ├── export_pdf.py              # Exportación a PDF
│   ├── setup_latex.py             # Instalación de LaTeX (Tectonic)
│   └── git_helper.py              # Guardar y publicar
├── latex_templates/               # Plantillas LaTeX personalizadas
│   ├── common/                    # Estilos compartidos (jupyterBook.cls)
│   ├── es/                        # Ajustes español (language_support.tex)
│   └── en/                        # Ajustes inglés
├── .github/
│   ├── skills/                    # Skills del proyecto (FUENTE DE VERDAD)
│   └── workflows/deploy.yml       # GitHub Actions: build + deploy
├── AGENTS.md                      # Este archivo
└── requirements.txt               # Dependencias Python
```

## Dependencias por Capas

La instalación inicial debe ser ligera. No mezcles dependencias científicas o de importación PDF en la base.

| Archivo | Cuándo se instala | Contenido |
|---|---|---|
| `requirements.txt` | Siempre | Build HTML, preview, citas, Kroki, Thebe y assets básicos |
| `requirements-pdf.txt` | `--extras pdf` | Exportación PDF y conversión SVG para LaTeX |
| `requirements-notebooks.txt` | `--extras notebooks` | Ejecución local de notebooks científicos |
| `requirements-pdf-import.txt` | `--extras pdf-import` | Conversión de PDFs a Markdown; puede arrastrar paquetes pesados |
| `requirements-dev.txt` | `--dev` | Tests y herramientas de desarrollo |

Regla práctica: para un docente que abre la plantilla por primera vez, usar `python scripts/setup_env.py --yes`. Para publicar con PDF, CI usa `python scripts/setup_env.py --yes --extras pdf`.
Si el instalador oficial de `uv` falla en Windows/CI, `setup_env.py` debe usar fallback automático con `python -m pip install uv` y añadir el directorio de scripts al `PATH` de la sesión.

## Idiomas Configurados

- **Español (es)**: Idioma principal. Config en `_config_es.yml`, TOC en `_toc_es.yml`.
- **Inglés (en)**: Idioma secundario. Config en `_config_en.yml`, TOC en `_toc_en.yml`.

Para añadir un nuevo idioma (ej: portugués `pt`):
1. Crear `book/_config_pt.yml` (copiar de `_config_es.yml` y adaptar).
2. Crear `book/_toc_pt.yml` (misma estructura que `_toc_es.yml`).
3. Crear `book/pt/` con TODO el contenido traducido (misma estructura de carpetas).
4. Crear `latex_templates/pt/language_support.tex` si se quiere PDF.
5. Añadir el código de idioma al mapa en `scripts/build_book.py` (`LANG_DISPLAY_NAMES`).

## Protocolo OBLIGATORIO para Añadir Contenido

Cuando añadas un capítulo o sección, DEBES seguir estos pasos EN ORDEN:

### 1. Crear el archivo de contenido en TODOS los idiomas
- Si creas `book/es/02_grados/grado_biologia/intro.md`, TAMBIÉN creas `book/en/02_degrees/grado_biology/intro.md`.
- Si un idioma no está traducido aún, crea el archivo con un placeholder: `*(Traducción pendiente)*`.

### 2. Actualizar TODOS los `_toc_<lang>.yml`
- Añadir la entrada en `_toc_es.yml` Y en `_toc_en.yml` (y cualquier otro idioma).
- La estructura debe ser IDÉNTICA en todos los TOC (mismas secciones, mismo orden).

### 3. Verificar que no hay contenido huérfano
- Ningún archivo `.md` en `book/es/` o `book/en/` debe existir sin estar referenciado en su `_toc.yml`.
- Ninguna entrada en `_toc.yml` debe apuntar a un archivo que no existe.

### 4. Verificar codificación UTF-8
- Ejecutar `python scripts/check_encoding.py` con el Python de `.venv`.
- Si aparecen secuencias típicas de mojibake o caracteres de reemplazo (`U+FFFD`), corregir el archivo fuente antes de compilar o commitear.
- En Windows, si una consola muestra acentos como `?`, repetir el comando con `$env:PYTHONUTF8='1'` y preferir los scripts del proyecto a `Get-Content` para validar texto.

### 5. Commitear todo junto
- Los cambios de contenido + TOC deben ir en el mismo commit.

## Contenido Multimedia — Compatibilidad HTML y PDF

### Imágenes
```md
```{image} _static/mi_imagen.png
:alt: Descripción de la imagen
:width: 80%
:align: center
```
```
- Formato: PNG, JPG o SVG.
- Ubicación: `book/_static/` (compartido) o junto al `.md`.
- Funciona en HTML ✅ y PDF ✅.

### Optimización segura de assets

- PNG se mantiene como formato principal por compatibilidad HTML/PDF.
- WebP solo se usa como mejora HTML si ya existe un PNG/JPG fallback y no se rompe PDF.
- Antes de publicar, validar con `python scripts/optimize_static_assets.py --check`.
- Para optimizar PNG/JPG sin cambiar rutas ni formatos: `python scripts/optimize_static_assets.py --fix`.
- El script usa Pillow dentro de `.venv`, por lo que funciona igual en Windows, macOS y Linux.

### GIFs animados con fallback PDF
Para un GIF animado docente, usa `{figure}` apuntando al `.gif` y guarda al lado un `.png` con el mismo nombre base:

````md
```{figure} _static/tutorial_gifs/es/paso_01.gif
---
name: fig-paso-01
alt: Descripción del GIF animado
width: 90%
align: center
---
Descripción breve del paso mostrado.
```
````

- En HTML se muestra el `.gif`.
- En PDF `scripts/export_pdf.py` sustituye la referencia por `paso_01.png` en la copia temporal.
- Si falta el `.png` equivalente, la exportación PDF debe fallar con un mensaje claro.
- Regla práctica: **GIF animado = `.gif` para HTML + `.png` del mismo nombre para PDF**.

### Figuras con etiqueta y referencia
```md
```{figure} _static/mi_imagen.png
---
width: 70%
name: fig-ejemplo
align: center
---
Descripción de la figura.
```

Como se ve en {numref}`fig-ejemplo`, la figura puede citarse.
```

### Videos de YouTube (compatible HTML + PDF)
Usa SIEMPRE este patrón para que funcione en ambos formatos:

```md
```{raw} html
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allowfullscreen></iframe>
```

```{raw} latex
\begin{center}
\textbf{Video:} \url{https://www.youtube.com/watch?v=VIDEO_ID}
\end{center}
```
```

- En HTML se ve el video embebido.
- En PDF se ve el enlace como texto.
- NUNCA uses `iframe` sin el bloque `{raw} latex` alternativo.

### Vídeo local estático (HTML5)
Para un vídeo generado externamente o exportado desde otra herramienta, guárdalo en `book/_static/videos/` e insértalo así:

```md
```{raw} html
<video width="720" controls>
  <source src="_static/videos/mi_animacion.mp4" type="video/mp4">
  Tu navegador no soporta vídeo HTML5.
</video>
```

```{raw} latex
\begin{center}
\textbf{Vídeo local:} consulte la versión HTML del libro para reproducirlo.
\end{center}
```
```

- En HTML se reproduce el `.mp4`.
- En PDF se muestra una referencia textual.
- Úsalo para vídeos docentes ya generados, capturas de pantalla o animaciones exportadas fuera del entorno base.
- Las herramientas pesadas de vídeo no forman parte de la instalación base de la plantilla.

### Código Python ejecutable (Notebooks)
- Los notebooks `.ipynb` se ejecutan si `_config.yml` tiene `execute_notebooks: auto`.
- Por defecto están DESACTIVADOS (`off`) para velocidad. Actívalo solo si el usuario lo pide.

### Ecuaciones LaTeX
```md
Ecuación inline: $E = mc^2$

Ecuación display numerada:
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$ (eq-gaussiana)

Referencia: la ecuación {eq}`eq-gaussiana` calcula...
```
- Funciona en HTML ✅ y PDF ✅ (requiere `dollarmath` en `myst_enable_extensions`, ya configurado).

### Citas Bibliográficas (BibTeX)
- Archivo de referencias: `book/_static/references.bib`.
- Bibliografía global del libro: mantener una sola página final `Bibliografía` / `Bibliography` con las citas usadas:
  ````md
  ```{bibliography}
  :cited:
  ```
  ````
- Citas normales para la bibliografía global: `{cite:t}`\`clave_cita\` (textual) o `{cite:p}`\`clave_cita\` (parentética).
- Bibliografía local de una página: SOLO para HTML. Las citas van en el texto normal si deben contar para PDF; al final se añade el bloque filtrado con `{only} html`:
  `````md
  Texto con cita local {cite:p}`clave_cita`.

  ````{only} html
  ## Bibliografía de esta página

  ```{bibliography}
  :filter: docname in docnames
  ```
  ````
  `````
- Para una bibliografía local parcial, se puede filtrar por claves dentro del mismo bloque HTML: `:filter: docname in docnames and key in {"clave1", "clave2"}`.
- En PDF NO se deben generar bibliografías locales: `scripts/export_pdf.py` genera un `.bib` temporal con las citas usadas y lo imprime solo en la página global `Bibliografía` / `Bibliography`.
- Como la web puede mostrar las mismas entradas en bibliografías locales y en la página global con `:cited:`, los `_config_<lang>.yml` deben mantener `suppress_warnings: ["bibtex.duplicate_citation"]`.
- Si hay bibliografías locales en HTML, la repetición con la página global es aceptable: local = comodidad por página; global = bibliografía completa del libro. En PDF solo debe aparecer la global final.
- Tras tocar citas, compilar HTML y PDF y revisar que no aparezcan avisos `could not find bibtex key`.

### Admonitions (cajas de información)
```md
```{admonition} Título
:class: tip

Contenido de la caja.
```
```
Clases disponibles: `tip`, `warning`, `note`, `important`, `caution`, `dropdown` (colapsable), `error`, `seealso`.

### Dropdowns (contenido colapsable)
```md
```{admonition} Solución
:class: dropdown

Aquí va la solución que el estudiante puede desplegar.
```
```

### Tabs (pestañas, requiere sphinx-design)
````md
```{tabbed} Python
```python
print("Hola")
```
```

```{tabbed} R
```r
print("Hola")
```
```
````

### Referencias cruzadas
- Secciones: `(mi-seccion)=` antes del título, luego `{ref}`\`mi-seccion\`
- Figuras: `{numref}`\`fig-ejemplo\`
- Ecuaciones: `{eq}`\`eq-gaussiana\`
- Tablas: `{numref}`\`tabla-ejemplo\`

### Diagramas con Kroki (HTML ✅ y PDF ✅)
Kroki convierte texto en diagramas. Usa Mermaid por defecto.

**Regla crítica del proyecto:** los diagramas finales del libro NO deben depender de bloques `{kroki}` en tiempo de compilación. El flujo correcto es:

1. Mantener la fuente editable en `diagram_sources/`.
2. Renderizar SVG para HTML con `python scripts/render_diagrams.py`.
3. Usar las imágenes generadas desde `{figure}`.
4. Para PDF, `render_diagrams.py` también genera fallbacks PNG SOLO para Mermaid en `book/_static/generated/diagrams_pdf/`.

Motivo: Kroki/Mermaid genera algunos SVG con texto HTML (`foreignObject`). En navegador se ve bien, pero algunos conversores LaTeX/PDF pierden ese texto y dejan cajas vacías. Por eso:

- HTML usa SVG nítido desde `book/_static/generated/diagrams/`.
- PDF usa SVG convertido si hay conversor vectorial real.
- Si no hay conversor vectorial, PDF usa el PNG nativo de Kroki desde `book/_static/generated/diagrams_pdf/`, que conserva el texto.

**NO usar `resvg` como fallback único para Mermaid con `foreignObject`: puede renderizar cajas sin texto.**

````md
```{kroki}
:type: mermaid
:align: center

flowchart LR
    A[Inicio] --> B[Proceso]
    B --> C[Fin]
```
````

Tipos disponibles: `mermaid` (recomendado), `plantuml`, `graphviz`, `excalidraw`, `vegalite`, `wavedrom`, `ditaa`, y 15+ más.
Requiere internet solo durante el pre-renderizado de diagramas, no durante la lectura del libro ya generado.
Para añadir título final: usar `{figure}` con caption, no `{kroki-figure}`.

**NO usar `{mermaid}`** (requiere sphinxcontrib-mermaid, no funciona en PDF). Para contenido final, usar fuentes en `diagram_sources/` + `{figure}` renderizado.

### CircuitikZ (opción avanzada para circuitos precisos)
CircuitikZ usa LaTeX para generar esquemas eléctricos con acabado profesional. En TeachBook se usa como flujo **a imagen**:

1. Crear un archivo `.tex` con el circuito.
2. Renderizarlo con:

```bash
python scripts/render_circuitikz.py ruta/al/circuito.tex book/_static/generated/circuito.png
```

3. Insertar la imagen con `{figure}`.

```md
```{figure} _static/generated/circuito.png
:alt: Circuito generado con CircuitikZ
:width: 70%
:align: center

Circuito generado con CircuitikZ.
```
```

- Funciona en HTML ✅ y PDF ✅ porque el resultado final es una imagen.
- Requiere Tectonic (`python scripts/setup_latex.py`).
- **SchemDraw** sigue siendo la opción sencilla; **CircuitikZ** es la opción avanzada.

### HTML interactivo autocontenido (SOLO HTML)
````md
```{raw} html
<details>
<summary>Ver pista</summary>
<p>Texto oculto que se despliega.</p>
</details>
```

```{raw} latex
\textbf{Pista:} Texto alternativo para PDF.
```
````

### Tabla de compatibilidad HTML/PDF

| Elemento | HTML | PDF | Regla |
|---|---|---|---|
| Texto, listas, imágenes | ✅ | ✅ | Usar libremente |
| Ecuaciones LaTeX | ✅ | ✅ | Usar libremente |
| Admonitions | ✅ | ✅ | Usar libremente |
| Dropdowns | ✅ | ✅ expandido | Usar libremente |
| Diagramas Kroki (Mermaid, etc.) | ✅ | ✅ | Usar `diagram_sources/` + SVG renderizado; PDF usa fallback PNG Mermaid si hace falta |
| iframe/YouTube | ✅ | ❌ | Añadir `{raw} latex` con URL |
| Thebe live code | ✅ | ❌ | Código visible como texto |
| Tabs | ✅ | ❌ | Añadir alternativa sin tabs |
| HTML personalizado | ✅ | ❌ | Añadir `{raw} latex` fallback |

## Comandos Disponibles

Todos los comandos se ejecutan desde la raíz del proyecto usando el Python del `.venv`:

| Tarea | Comando | Qué hace |
|---|---|---|
| Configurar entorno base | `python scripts/setup_env.py --yes` | Crea `.venv` con Python 3.12 e instala solo lo necesario para web/preview |
| Añadir soporte PDF | `python scripts/setup_env.py --yes --extras pdf` | Instala dependencias Python para exportar PDF |
| Añadir notebooks científicos | `python scripts/setup_env.py --yes --extras notebooks` | Instala NumPy, Matplotlib, pandas, SciPy, SymPy, Schemdraw, ipywidgets y JupyterQuiz |
| Añadir importación de PDFs | `python scripts/setup_env.py --yes --extras pdf-import` | Instala el conversor PDF→Markdown bajo demanda |
| Instalar todo | `python scripts/setup_env.py --yes --all` | Instala base + todos los extras opcionales |
| Configurar + dev | `python scripts/setup_env.py --yes --dev` | Base + herramientas de testing |
| Recrear entorno | `python scripts/setup_env.py --recreate --yes` | Borra y recrea `.venv` si existe con otra versión de Python |
| Perfilar instalación | `python scripts/setup_env.py --yes --profile` | Mide tiempos por fase y guarda `.build_logs/setup_env_profile.json` |
| Perfilar dependencias | `python scripts/profile_dependencies.py --dry-run --requirements requirements.txt requirements-pdf.txt` | Mide resolución de uno o varios grupos sin instalar |
| Solo sincronizar skills | `python scripts/setup_env.py --sync-only` | Copia skills a .claude/, .agents/, .agent/ sin tocar deps |
| Compilar libro | `python scripts/build_book.py` | Genera HTML multi-idioma en `book/_build/html/` |
| Vista previa | `python scripts/launch_preview.py` | Lanza la preview segura en `localhost:8000` usando el mismo build que producción |
| Exportar PDF | `python scripts/export_pdf.py` | Genera PDF para cada idioma en `book/_static/` |
| Exportar LaTeX editable | `python scripts/export_latex_project.py --output latex_exports` | Genera carpetas LaTeX y ZIPs Overleaf-ready para retoques editoriales finales |
| Instalar LaTeX | `python scripts/setup_latex.py` | Instala Tectonic (motor LaTeX ligero) |
| Instalar PDF completo | `python scripts/setup_latex.py --yes --full` | Instala Tectonic + TinyTeX-1 portable ligero como fallback quirúrgico |
| Extraer fuentes Kroki | `python scripts/extract_kroki_sources.py` | Copia bloques `{kroki}` existentes a `diagram_sources/` sin modificar el contenido |
| Renderizar diagramas | `python scripts/render_diagrams.py` | Convierte fuentes en `diagram_sources/` a imágenes estáticas en `book/_static/generated/diagrams/` |
| Sustituir diagramas renderizados | `python scripts/replace_kroki_with_figures.py` | Cambia bloques `{kroki}` por `{figure}` solo si existe la imagen generada |
| Verificar idiomas/menús | `python scripts/check_multilang_integrity.py` | Comprueba que todos los idiomas tienen la misma estructura de menú y archivos completos |
| Verificar/generar bibliografía usada | `python scripts/collect_used_bibliography.py --lang es --output .build_logs/references_used_es.bib` | Valida claves `{cite}` y genera un `.bib` de inspección con solo las citas usadas |
| Verificar/optimizar assets estáticos | `python scripts/optimize_static_assets.py --check` | Audita imágenes web, PNG/JPG optimizables y fallbacks PNG para GIFs |
| Renderizar CircuitikZ | `python scripts/render_circuitikz.py <entrada.tex> [salida.png]` | Compila CircuitikZ y genera una imagen PNG |
| Convertir PDF a MD | `python scripts/pdf_to_markdown.py <ruta>` | Convierte PDFs a Markdown para el libro |
| Verificar codificación | `python scripts/check_encoding.py` | Comprueba UTF-8 y detecta mojibake en contenido, scripts y skills |
| Guardar y publicar | `python scripts/git_helper.py` | git add + commit + push; GitHub Actions regenera HTML y PDFs nuevos |
| Publicar en servidor propio | GitHub Actions → `sftp-deploy-book` → `Run workflow` | Compila PDFs/HTML y sincroniza `book/_build/html` por SFTP |

**IMPORTANTE**: En Windows, si `python` no funciona, probar con `py`. Los scripts manejan ambas opciones.

### PDF local/CI recomendado

El flujo recomendado para PDF sigue siendo:

```bash
python scripts/setup_latex.py --yes --full
python scripts/export_pdf.py --engine auto
```

Si el entorno se instaló en modo base, antes de exportar PDF ejecuta:

```bash
python scripts/setup_env.py --yes --extras pdf
```

Ese modo usa **Tectonic primero** y deja **TinyTeX-1 portable dentro de `.venv`** como fallback ligero (`latexmk` + XeLaTeX). TinyTeX se instala con paquetes explícitos mínimos para las plantillas del libro; no se deben usar colecciones pesadas como `collection-latexextra`, `collection-xetex`, `collection-latexrecommended`, `collection-fontsrecommended`, `collection-langspanish`, `collection-langenglish` ni `scheme-full`. El script avisa si detecta una instalación TinyTeX mayor de 1 GB o con colecciones pesadas, pero no borra nada automáticamente.

### Vista previa para agentes de código

Los agentes/IDEs deben lanzar la preview en segundo plano para no quedarse bloqueados:

```bash
python scripts/launch_preview.py --background
python scripts/launch_preview.py --status
python scripts/launch_preview.py --log
```

Para detenerla:

```bash
python scripts/launch_preview.py --stop
```

Reglas estrictas:

- NO usar `sphinx-autobuild` directamente.
- NO crear entornos alternativos (`.venv_linux`, `.venv2`, `/tmp/venv`, etc.).
- NO abrir una web antigua si el build falla.
- Esperar a que el log muestre `✅ Build correcto` y `🌐 Preview listo`.

## Publicación en GitHub Pages

El proyecto incluye un GitHub Action (`.github/workflows/deploy.yml`) que:
1. Se ejecuta automáticamente al hacer `push` a la rama principal.
2. Instala/prepara el entorno TeachBook.
3. Instala las dependencias Python de PDF con `scripts/setup_env.py --yes --extras pdf`.
4. Instala la cadena PDF completa con `scripts/setup_latex.py --yes --full`.
5. Genera PDFs nuevos para todos los idiomas con `scripts/export_pdf.py --engine auto`.
6. Compila el libro HTML para todos los idiomas con `scripts/build_book.py`.
7. Despliega a GitHub Pages.

**Regla crítica de publicación:** no se debe publicar una versión nueva subiendo solo HTML. La ruta soportada es `commit + push` a `main`, porque el workflow regenera primero los PDFs finales de `book/_static/` y después construye la web que enlaza esos PDFs recientes. Si se cambia contenido, diagramas, imágenes o notebooks, el deploy debe producir PDFs nuevos en la misma ejecución.

Para que GitHub Pages funcione, el usuario debe:
1. Tener el repo en GitHub.
2. Ir a Settings → Pages → Source: `GitHub Actions`.
3. Hacer el primer `push`.

## Publicación en Servidor Propio por SFTP

El proyecto también incluye un workflow manual (`.github/workflows/sftp-deploy.yml`) para desplegar el mismo build HTML en un servidor propio, por ejemplo un alojamiento institucional con dominio como `libro.usal.es`.

Reglas estrictas:

- El workflow `sftp-deploy-book` es **solo manual** (`workflow_dispatch`). No debe ejecutarse automáticamente en `push` ni en `pull_request`.
- Nunca commitear credenciales. El servidor, usuario, contraseña y puerto deben vivir solo en GitHub Actions secrets.
- Secretos requeridos: `SFTP_SERVER`, `SFTP_USERNAME`, `SFTP_PASSWORD`. Secreto opcional: `SFTP_PORT` (si falta, se usa `22`).
- El input `remote_dir` indica el directorio remoto que se sincroniza; por defecto es `public_html`.
- El deploy SFTP limpia el directorio remoto configurado para que quede igual que `book/_build/html`. Revisar bien `remote_dir` antes de lanzar la acción.
- Este workflow también genera PDFs antes del HTML. No publicar por SFTP builds parciales o carpetas generadas a mano.

El workflow valida que `remote_dir` no sea una ruta peligrosa como `/`, `.`, `..`, `~` o una ruta absoluta, pero el docente/mantenedor sigue siendo responsable de elegir el directorio correcto del servidor.

### Workflow de pruebas limpias

El workflow `.github/workflows/test.yml` (`Test Clean Setup`) es **solo manual** (`workflow_dispatch`). No debe ejecutarse automáticamente en `push` ni en `pull_request`, porque prueba instalaciones limpias completas en Windows y macOS y consume tiempo/minutos de CI.

Regla para agentes y alumnos:
- No añadir triggers automáticos (`push`, `pull_request`, `schedule`) a `Test Clean Setup`.
- No lanzarlo como parte del flujo normal de publicación.
- Solo debe ejecutarlo el docente/mantenedor cuando quiera validar cambios en instalación, dependencias, PDF o CI.

## Skills Disponibles

Las skills están en `.github/skills/` (fuente de verdad) y se sincronizan a `.claude/skills/`, `.agents/skills/` y `.agent/skills/` durante `setup_env.py`.

| Skill | Cuándo usarla |
|---|---|
| `teachbook-setup-environment` | Primera vez, algo no funciona, cambio de ordenador |
| `teachbook-build` | Compilar, ver HTML, verificar contenido |
| `teachbook-live-preview` | Escribir y ver cambios en tiempo real |
| `teachbook-export-pdf` | Generar PDF imprimible |
| `teachbook-export-latex-project` | Exportar el libro como proyecto LaTeX editable para retoques finales |
| `teachbook-git-publish` | Guardar y publicar cambios |
| `teachbook-add-content` | Añadir nuevos capítulos o secciones |
| `teachbook-multimedia` | Insertar imágenes, videos, ecuaciones |
| `teachbook-optimize-static-assets` | Revisar y optimizar assets estáticos para web sin romper PDF |
| `teachbook-pdf-to-markdown` | Convertir PDFs existentes a Markdown |
| `teachbook-generate-diagram` | Crear diagramas Kroki (Mermaid, PlantUML, GraphViz, etc.) compatibles con HTML y PDF |
| `teachbook-generate-schemdraw-circuit` | Crear diagramas de circuitos eléctricos |
| `teachbook-generate-circuitikz` | Crear circuitos precisos con CircuitikZ exportados a imagen |
| `teachbook-generate-teaching-notebook` | Crear notebooks docentes con código ejecutable |
| `teachbook-generate-interactive-html` | Añadir HTML interactivo sin frameworks JS |
| `teachbook-generate-quiz` | Crear cuestionarios con respuestas ocultas |
| `teachbook-generate-thebe-binder-page` | Crear páginas con código ejecutable mediante Thebe + Binder |
| `teachbook-review-teaching-quality` | Revisar calidad docente del contenido |
| `teachbook-review-html-pdf-compatibility` | Verificar que contenido funciona en HTML y PDF |

## Tono de Comunicación

- Amable, directo, en español.
- Sin jerga técnica innecesaria.
- Usa analogías de la vida real para explicar conceptos.
- Si algo falla, explica QUÉ falló y CÓMO se arregla, no POR QUÉ falló técnicamente.
