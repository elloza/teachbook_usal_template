# Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial 🎓

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20449102-blue.svg)](https://doi.org/10.5281/zenodo.20449102)
[![Licencia: CC BY 4.0](https://img.shields.io/badge/Licencia-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Material y plantilla del curso **Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial**, dirigido a las **Facultades de Ciencias y de Ciencias Químicas de la USAL** y diseñado para que profesores sin conocimientos de informática puedan crear y publicar libros digitales usando **agentes de código con IA**.

👉 **Demo rápida para docentes:** [http://elloza.com/teachbook_usal_template/](http://elloza.com/teachbook_usal_template/)

---

## Cita y DOI

La cita recomendada está en formato APA 7.ª edición. También hay metadatos reutilizables en [`CITATION.cff`](CITATION.cff), [`CITATION.bib`](CITATION.bib) y [`.zenodo.json`](.zenodo.json).

> Lozano Murciego, Á., & Sales Mendes, A. F. (2026). *Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial*. Universidad de Salamanca. https://doi.org/10.5281/zenodo.20449102

El DOI del conjunto de versiones lleva al registro actualizado del libro. Cada edición archivada tiene además su propio DOI. [Consultar en Zenodo](https://doi.org/10.5281/zenodo.20449102)

Autores:

- Álvaro Lozano Murciego — ORCID: https://orcid.org/0000-0002-0493-4471
- André Filipe Sales Mendes — ORCID: https://orcid.org/0000-0003-0976-2784

---

## 🤖 Herramientas compatibles

Puedes usar esta plantilla con cualquiera de estos agentes de código:

| Herramienta | Requisito | Tipo |
|---|---|---|
| **VS Code + GitHub Copilot** | [VS Code](https://code.visualstudio.com/) + extensión GitHub Copilot (requiere suscripción **Copilot Pro**) | Editor de código |
| **Antigravity IDE** | Cuenta Google | App de escritorio de Google |
| **OpenAI Codex** | Suscripción **ChatGPT Plus** o superior | App de escritorio de OpenAI |

> **¿Cuál elegir?** Si ya usas VS Code, ve con Copilot. Si prefieres la app de Google, Antigravity IDE. Si usas ChatGPT Plus, la app de escritorio Codex de OpenAI.

---

## 📋 Requisitos previos

Antes de abrir la plantilla con tu agente de IA, necesitas tener instalado **como mínimo**:

### Imprescindible
1. **Python 3.12** → [Descargar](https://www.python.org/downloads/)
   - ⚠️ **En Windows**: marca la casilla **"Add Python to PATH"** durante la instalación
   - Para verificar: abre una terminal y escribe `python --version` (o `py --version` en Windows)

### Recomendado (no obligatorio, el agente te ayudará a instalarlo)
2. **Git** → [Descargar](https://git-scm.com/) (necesario para publicar en GitHub)
3. **uv** (gestor de paquetes ultrarrápido) → El agente te preguntará si quieres instalarlo
4. **Node.js 22.18 o superior y npm** solo para proyectos que activan Slidev. [Descargar Node.js](https://nodejs.org/)

### Para publicar en la web
5. **Cuenta en GitHub** → [Crear cuenta](https://github.com/signup)
6. **Un repositorio** creado a partir de esta plantilla (botón "Use this template" en GitHub)

---

## 🚀 Guía de inicio — Qué decirle al agente

Abre tu herramienta (VS Code, Antigravity o Codex) en la carpeta del proyecto y dile lo siguiente:

### 1️⃣ Primera vez: configurar el entorno

Dile al agente:

> **"Prepara el entorno del proyecto. Es la primera vez que lo abro."**

O también puedes decir:
- *"Configura el proyecto"*
- *"Instala todo lo necesario"*
- *"No me funciona, falta algo"*

El agente:
- Detectará tu sistema operativo (Windows, macOS o Linux)
- Instalará `uv` (gestor de paquetes rápido) si no lo tienes
- Creará el entorno virtual `.venv`
- Instalará las dependencias del libro y los extras que solicites
- Si usas diapositivas, comprobará Node.js y preparará `slides/`
- Sincronizará las instrucciones para que funcione con tu herramienta

Puedes decirle **«Prepara la plantilla sin diapositivas»** antes de instalar. El agente pondrá `"slides": false` en `teachbook.json` y preparará el libro sin Node.js. La demo usa `"slides": true`. Para activar las diapositivas en tu proyecto, cambia ese valor a `true` y vuelve a ejecutar `python scripts/setup_env.py --yes`.

### 2️⃣ Compilar el libro (generar la web)

> **"Compila el libro"** o **"Genera la web"**

Esto crea la versión HTML navegable en `book/_build/html/`. Puedes abrirla en cualquier navegador.

El build reutiliza el HTML por idioma y las presentaciones que siguen al día. Con Slidev activado, integra las diapositivas en la web final. Para comprobar un build desde cero usa `python scripts/build_book.py --clean`.

### 3️⃣ Ver cambios en tiempo real (desarrollo)

> **"Quiero ver el libro en vivo"** o **"Abre la vista previa"**

Se abrirá tu navegador en `localhost:8000`. Tras guardar, la vista previa prepara los cambios con el mismo build que producción. Si una compilación falla durante la edición, puedes seguir consultando la última compilación correcta y ver el error en el registro.

### 4️⃣ Generar los PDFs

> **"Genera los PDFs del libro"** o **"Exportar a PDF"**

El agente instalará LaTeX (Tectonic) si es necesario y generará `ElaboracionDeLibrosElectronicosMedianteCodigoYAsistentesDeInteligenciaArtificial.pdf` y `CreatingElectronicBooksWithCodeAndArtificialIntelligenceAssistants.pdf`.

Tras exportar ambos PDF una vez con conexión, puedes volver a generarlos con `python scripts/export_pdf.py --offline` mientras Tectonic tenga los recursos necesarios en la caché del proyecto.

### 5️⃣ Generar diapositivas para clase

> **"Crea diapositivas para este capítulo"** o **"Actualiza las slides del tema de Física"**

El agente usará `slides/` para crear una presentación Slidev por cada capítulo principal. En la web aparecerá un botón **Slides** arriba: desde una página del capítulo abrirá sus diapositivas, y desde otras páginas abrirá el índice de diapositivas del idioma.

Las diapositivas también son multi-idioma: si se crean en español, debe existir su equivalente en inglés. Se escriben en Markdown, como el libro, para que el agente pueda generarlas y mantenerlas sin que tengas que aprender una herramienta nueva.

Las presentaciones que han cambiado se compilan en paralelo. Si el equipo tiene poca memoria, puedes usar `TEACHBOOK_SLIDEV_JOBS=1`.

> Nota: descargar las diapositivas como PDF está planificado para una versión futura. Ahora la funcionalidad estable es la publicación web de las diapositivas.

### 6️⃣ Guardar cambios en GitHub

> **"Guarda y publica los cambios"** o **"Haz commit y push"**

El agente hará `git add` + `commit` + `push` automáticamente con un mensaje descriptivo.

### 7️⃣ Publicar en GitHub Pages (solo la primera vez)

**Esto lo haces tú manualmente, una sola vez:**

1. Ve a tu repositorio en [github.com](https://github.com)
2. Ve a **Settings** → **Pages**
3. En **Source**, selecciona: **GitHub Actions**
4. ¡Listo! A partir de ahora, cada vez que hagas push, el libro se publicará automáticamente

> La URL de tu libro será: `https://<tu-usuario>.github.io/<nombre-del-repo>/`

### 8️⃣ Empezar con un libro mínimo sin borrar los ejemplos

Si al principio quieres que el libro muestre **solo una parte** (por ejemplo, un único capítulo que te interese), no hace falta borrar todo el contenido de ejemplo.

La opción recomendada es decirle al agente algo como:

> **"Quiero dejar visible solo este capítulo y ocultar el resto como referencia"**

o:

> **"Oculta temporalmente los capítulos de ejemplo que no voy a usar todavía"**

El agente puede:

- quitar esos capítulos del menú
- comentarlos en los `_toc_es.yml` y `_toc_en.yml`
- dejar los archivos intactos en el repositorio

Así tienes una plantilla limpia para empezar, pero conservas material reutilizable para más adelante.

### ¿Por qué es mejor ocultar que borrar?

- puedes volver a activar ejemplos en cualquier momento
- sigues teniendo páginas de referencia para copiar estructura, estilo y recursos
- reduces el riesgo de borrar cosas útiles demasiado pronto

**Recomendación**: al principio, **oculta primero**. Borra solo cuando ya tengas claro que no vas a necesitar ese contenido.

---

## 📂 Estructura del proyecto (no hace falta tocarla)

```
teachbook_usal_template/
├── book/                    # ← Contenido del libro (aquí editas)
│   ├── es/                  # Contenido en español
│   │   ├── intro.md         # Página de inicio
│   │   ├── 01_tutorial/     # Tutoriales
│   │   └── 02_grados/       # Ejemplos por grado
│   ├── en/                  # Contenido en inglés (misma estructura)
│   ├── _config_es.yml       # Configuración español
│   ├── _toc_es.yml          # Índice español
│   └── _static/             # Imágenes, CSS, logos
├── slides/                  # ← Diapositivas Slidev del libro
│   ├── package.json         # Configuración técnica de Slidev
│   ├── es/                  # Presentaciones en español
│   └── en/                  # Presentaciones en inglés
├── scripts/                 # Scripts de automatización (no editar)
├── latex_templates/         # Plantillas PDF (personalizable)
├── teachbook.json           # Activa o desactiva Slidev para todo el proyecto
├── AGENTS.md                # Instrucciones para el agente de IA
└── .github/skills/          # Skills del agente (no editar)
```

### Archivos que SÍ puedes editar:
- `book/es/*.md` y `book/en/*.md` — contenido del libro
- `book/_toc_es.yml` y `book/_toc_en.yml` — índice del libro
- `book/_config_es.yml` y `book/_config_en.yml` — título, autor, etc.
- `book/_static/` — imágenes y logos
- `book/_static/references.bib` — bibliografía global del libro
- `teachbook.json` — activar o desactivar Slidev
- `slides/es/**/slides.md` y `slides/en/**/slides.md` — diapositivas de cada capítulo principal, preferiblemente con ayuda del agente

### Archivos que NO debes tocar:
- `scripts/` — los ejecuta el agente automáticamente
- `.github/skills/` — instrucciones para el agente
- `AGENTS.md`, `CLAUDE.md` — configuración del agente
- `slides/package.json` y `slides/package-lock.json` — configuración técnica de las diapositivas

---

## 🌍 Soporte multi-idioma

El libro genera versiones en **español** e **inglés** automáticamente con un selector de idioma en la web.

**Regla importante**: Si añades contenido en un idioma, DEBE existir en todos los idiomas. Díselo al agente:

> **"Añade un nuevo capítulo de Biología al libro"**

El agente se encargará de crear el contenido en `book/es/` Y `book/en/`, y de actualizar ambos índices.

Con Slidev activado, cada capítulo principal tiene una presentación en `slides/<idioma>/.../slides.md` para cada idioma. Las secciones del capítulo usan esa misma presentación. El botón **Slides** abre la presentación asociada a la página que estás leyendo.

Para revisar que no falta ninguna presentación multi-idioma, dile al agente:

> **"Comprueba que las slides están en todos los idiomas"**

---

## 📚 Bibliografía y referencias

La forma más simple de gestionar bibliografía en esta plantilla es:

1. guardar todas las entradas BibTeX en:
   - `book/_static/references.bib`
2. citar en cualquier página con:
   - `{cite:t}`
   - `{cite:p}`
3. usar la página final de:
   - `Referencias` / `References`

Esa página imprime la bibliografía global del libro y sirve también para la exportación a PDF/LaTeX.

---

## 💬 Frases útiles para el agente

| Quiero... | Dile al agente |
|---|---|
| Configurar todo | *"Prepara el entorno"* |
| Compilar la web | *"Compila el libro"* |
| Ver cambios en vivo | *"Abre la vista previa"* |
| Generar PDFs | *"Genera los PDFs"* |
| Crear diapositivas | *"Crea las slides de este capítulo"* |
| Revisar diapositivas | *"Comprueba que las slides están en todos los idiomas"* |
| Guardar cambios | *"Guarda y publica los cambios"* |
| Añadir un capítulo | *"Añade un capítulo de [tema]"* |
| Añadir una imagen | *"Inserta una imagen en [sección]"* |
| Añadir un video | *"Añade un video de YouTube en [sección]"* |
| Convertir un PDF | *"Convierte este PDF a Markdown"* |
| Que algo no funciona | *"No me funciona [cosa]"* |
| Añadir una ecuación | *"Añade la ecuación [ecuación] en [sección]"* |

---

## 🧪 Tests de verificación

El workflow manual **Test Clean Setup** comprueba la instalación y el build en Linux, macOS y Windows, con pruebas del libro sin Slidev en x64 y ARM64.

Los tests se lanzan **solo manualmente** desde la pestaña **Actions** en GitHub, cuando quieras comprobar que el proyecto arranca bien desde cero.

Estos tests verifican que:
- Todos los scripts compilan correctamente
- El entorno se configura desde cero
- El libro se compila en ambos idiomas
- Las skills se sincronizan

### Cuándo usarlos

- antes de compartir la plantilla con otros
- antes de una entrega importante
- cuando cambies scripts, entorno o skills

### Qué sí se ejecuta automáticamente

El **deploy de GitHub Pages** sí se ejecuta automáticamente al hacer `push` a `main`.

Los workflows de Pages y SFTP regeneran los PDF y reutilizan la caché de Tectonic. Con Slidev activado en `teachbook.json`, también preparan Node.js y publican las presentaciones dentro del mismo sitio.

Las ediciones archivables se publican como releases de GitHub tras validar el despliegue. La integración de Zenodo archiva el código etiquetado con los metadatos de `.zenodo.json`. [Releases del proyecto](https://github.com/elloza/teachbook_usal_template/releases)

---

## 📄 Licencia

Este proyecto está licenciado bajo **CC BY 4.0** — eres libre de usar, modificar y redistribuir con atribución.

---

## 👥 Créditos

- **Álvaro Lozano Murciego** — Universidad de Salamanca
- **André Filipe Sales Mendes** — Universidad de Salamanca
- Basado en [TeachBooks](https://teachbooks.io/) y [Jupyter Book](https://jupyterbook.org/)
