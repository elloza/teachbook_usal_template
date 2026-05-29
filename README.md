# Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial 🎓

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20449102-blue.svg)](https://doi.org/10.5281/zenodo.20449102)
[![Licencia: CC BY 4.0](https://img.shields.io/badge/Licencia-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Material y plantilla del curso **Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial**, dirigido a las **Facultades de Ciencias y de Ciencias Químicas de la USAL** y diseñado para que profesores sin conocimientos de informática puedan crear y publicar libros digitales usando **agentes de código con IA**.

---

## Cita y DOI

La cita recomendada está en formato APA 7.ª edición. También hay metadatos reutilizables en [`CITATION.cff`](CITATION.cff), [`CITATION.bib`](CITATION.bib) y [`.zenodo.json`](.zenodo.json).

> Lozano Murciego, Á., & Sales Mendes, A. F. (2026). *Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial*. Universidad de Salamanca. https://doi.org/10.5281/zenodo.20449102

DOI definitivo de Zenodo para esta versión:

- https://doi.org/10.5281/zenodo.20449102

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

### Para publicar en la web
4. **Cuenta en GitHub** → [Crear cuenta](https://github.com/signup)
5. **Un repositorio** creado a partir de esta plantilla (botón "Use this template" en GitHub)

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
- Detectará tu sistema operativo (Windows o Mac)
- Instalará `uv` (gestor de paquetes rápido) si no lo tienes
- Creará el entorno virtual `.venv`
- Instalará todas las dependencias
- Sincronizará las instrucciones para que funcione con tu herramienta

⏱️ **Tarda 1-3 minutos** la primera vez.

### 2️⃣ Compilar el libro (generar la web)

> **"Compila el libro"** o **"Genera la web"**

Esto crea la versión HTML navegable en `book/_build/html/`. Puedes abrirla en cualquier navegador.

### 3️⃣ Ver cambios en tiempo real (desarrollo)

> **"Quiero ver el libro en vivo"** o **"Abre la vista previa"**

Se abrirá tu navegador en `localhost:8000` y los cambios se reflejarán automáticamente al guardar los archivos.

### 4️⃣ Generar los PDFs

> **"Genera los PDFs del libro"** o **"Exportar a PDF"**

El agente instalará LaTeX (Tectonic) si es necesario y generará `ElaboracionDeLibrosElectronicosMedianteCodigoYAsistentesDeInteligenciaArtificial.pdf` y `CreatingElectronicBooksWithCodeAndArtificialIntelligenceAssistants.pdf`.

### 5️⃣ Guardar cambios en GitHub

> **"Guarda y publica los cambios"** o **"Haz commit y push"**

El agente hará `git add` + `commit` + `push` automáticamente con un mensaje descriptivo.

### 6️⃣ Publicar en GitHub Pages (solo la primera vez)

**Esto lo haces tú manualmente, una sola vez:**

1. Ve a tu repositorio en [github.com](https://github.com)
2. Ve a **Settings** → **Pages**
3. En **Source**, selecciona: **GitHub Actions**
4. ¡Listo! A partir de ahora, cada vez que hagas push, el libro se publicará automáticamente

> La URL de tu libro será: `https://<tu-usuario>.github.io/<nombre-del-repo>/`

### 7️⃣ Empezar con un libro mínimo sin borrar los ejemplos

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
├── scripts/                 # Scripts de automatización (no editar)
├── latex_templates/         # Plantillas PDF (personalizable)
├── AGENTS.md                # Instrucciones para el agente de IA
└── .github/skills/          # Skills del agente (no editar)
```

### Archivos que SÍ puedes editar:
- `book/es/*.md` y `book/en/*.md` — contenido del libro
- `book/_toc_es.yml` y `book/_toc_en.yml` — índice del libro
- `book/_config_es.yml` y `book/_config_en.yml` — título, autor, etc.
- `book/_static/` — imágenes y logos
- `book/_static/references.bib` — bibliografía global del libro

### Archivos que NO debes tocar:
- `scripts/` — los ejecuta el agente automáticamente
- `.github/skills/` — instrucciones para el agente
- `AGENTS.md`, `CLAUDE.md` — configuración del agente

---

## 🌍 Soporte multi-idioma

El libro genera versiones en **español** e **inglés** automáticamente con un selector de idioma en la web.

**Regla importante**: Si añades contenido en un idioma, DEBE existir en todos los idiomas. Díselo al agente:

> **"Añade un nuevo capítulo de Biología al libro"**

El agente se encargará de crear el contenido en `book/es/` Y `book/en/`, y de actualizar ambos índices.

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
| Guardar cambios | *"Guarda y publica los cambios"* |
| Añadir un capítulo | *"Añade un capítulo de [tema]"* |
| Añadir una imagen | *"Inserta una imagen en [sección]"* |
| Añadir un video | *"Añade un video de YouTube en [sección]"* |
| Convertir un PDF | *"Convierte este PDF a Markdown"* |
| Que algo no funciona | *"No me funciona [cosa]"* |
| Añadir una ecuación | *"Añade la ecuación [ecuación] en [sección]"* |

---

## 🧪 Tests de verificación

El proyecto incluye tests de verificación en **Windows** y **macOS (Apple Silicon)**, pero **NO se ejecutan automáticamente en cada push**. Esto está hecho así para que el profesorado o alumnado que copie la plantilla no gaste minutos de GitHub Actions innecesariamente.

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

---

## 📄 Licencia

Este proyecto está licenciado bajo **CC BY 4.0** — eres libre de usar, modificar y redistribuir con atribución.

---

## 👥 Créditos

- **Álvaro Lozano Murciego** — Universidad de Salamanca
- **André Filipe Sales Mendes** — Universidad de Salamanca
- Basado en [TeachBooks](https://teachbooks.io/) y [Jupyter Book](https://jupyterbook.org/)
