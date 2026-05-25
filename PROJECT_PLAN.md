# Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial — Project Plan (v1)

Este documento define el **plan completo de implementación**
del repositorio `teachbook_sciences_template`.

El objetivo es crear una **plantilla docente reutilizable**
para el curso **Elaboración de libros electrónicos mediante código y asistentes de Inteligencia Artificial** y para libros electrónicos interactivos basados en TeachBooks,
orientada a asignaturas de las **Facultades de Ciencias y de Ciencias Químicas (USAL)**.

Este documento es la **fuente única de verdad** para el agente.
No inventes funcionalidades fuera de este plan.

---

## 1. OBJETIVO GENERAL

Crear un **template estable, simple y pedagógico** que permita
a profesorado universitario **no informático**:

- crear un libro docente electrónico
- combinar texto, código y visualizaciones
- publicar el libro como web
- reutilizar ejemplos por grado y asignatura
- usar asistentes de IA como apoyo continuo

---

## 2. PRINCIPIOS DE DISEÑO (OBLIGATORIOS)

- Priorizar **simplicidad** sobre potencia
- Todo debe funcionar con **VS Code**
- Evitar configuraciones complejas
- No asumir conocimientos de Git
- No activar funcionalidades avanzadas por defecto
- El template debe compilar sin tocar nada
- El contenido debe ser **didáctico y editable**

---

## 3. STACK TECNOLÓGICO (FIJO)

No introducir tecnologías adicionales.

- TeachBooks / Jupyter Book
- MyST Markdown
- Jupyter Notebooks
- Python básico
- GitHub Pages
- VS Code
- Asistentes de IA (Copilot / Antigravity)

---

## 4. ESTRUCTURA FINAL DEL REPOSITORIO

Implementar exactamente esta estructura:

teachbook_sciences_template/
├── book/
│   ├── es/              # Contenido en Español
│   │   ├── intro.md
│   │   ├── ...
│   ├── en/              # Contenido en Inglés
│   │   ├── intro.md
│   │   ├── ...
│   ├── _toc_es.yml      # Índice Español
│   ├── _config_es.yml   # Config Español
│   ├── _toc_en.yml      # Índice Inglés
│   ├── _config_en.yml   # Config Inglés
│   └── _static/
├── latex_templates/     # Plantillas para PDF
│   ├── common/
│   ├── es/
│   └── en/
├── scripts/             # Scripts de utilidad (build, export_pdf, preview)
├── Agent.md
├── PROJECT_PLAN.md
├── README.md
├── requirements.txt
└── LICENSE


---

## 5. CONTENIDOS A IMPLEMENTAR

### 5.1 Introducción (`intro.md`)
- Qué es un TeachBook
- Contexto USAL
- Enlace a “Cómo citar”
- Badge de Zotero (placeholder)

---

### 5.2 Tutoriales (`01_tutorial/`)
Contenido guiado, paso a paso:

1. Qué es un TeachBook
2. Flujo de trabajo completo
3. Edición con IA desde VS Code
4. Publicación web

Lenguaje:
- claro
- sin jerga técnica
- orientado a docentes

---

### 5.3 Ejemplos por grado (`02_grados/`)

Organización obligatoria:
Grado → Asignatura → Ejemplo


Cada ejemplo debe:
- ser sencillo
- ser realista
- poder borrarse o copiarse
- servir como referencia

---

### 5.4 Secciones finales

#### Acerca de
- autores
- institución
- año
- contexto del curso

#### Licencias
- CC-BY para contenidos
- MIT para código
- atribuciones a TeachBooks / Jupyter Book

#### Cómo citar
- referencia textual
- BibTeX
- mención a DOI futuro (Zenodo)
- referencia a Zotero

---

## 6. AGENTE Y ASISTENCIA CON IA

El archivo `Agent.md` define el comportamiento del asistente.

El agente debe:
- ayudar a crear contenidos
- explicar errores de compilación
- proponer ejemplos didácticos
- priorizar claridad y resultados visibles

---

## 7. FUNCIONALIDADES AVANZADAS (ESTADO)

- [x] **Multidioma**: Estructura `book/es/` y `book/en/` implementada. Selector de idioma automático.
- [x] **Exportación a PDF**: Script `export_pdf.py` y GitHub Actions configurados con soporte para `latex_templates` personalizados.
- [ ] **Comentarios**: (giscus / utterances) - Pendiente de configuración por el usuario.
- [ ] **DOI automático**: Pendiente (Zenodo).

Solo documentar puntos de extensión si procede.

---

## 8. CRITERIOS DE FINALIZACIÓN (DEFINITION OF DONE)

El proyecto se considera correcto cuando:

- El libro compila sin errores
- Se puede publicar como web
- La estructura es clara
- El contenido es editable
- El template puede clonarse y usarse
- Un docente no informático puede empezar

---

## 9. ORDEN DE IMPLEMENTACIÓN (OBLIGATORIO)

El agente debe implementar en este orden:

1. Estructura de carpetas
2. `_toc.yml` funcional
3. `_config.yml` mínimo
4. Contenidos base (vacíos o mínimos)
5. Ejemplos sencillos
6. README pedagógico
7. Verificación de compilación

No saltarse pasos.

---

## 10. NORMA FINAL

No optimizar prematuramente.
No añadir funcionalidades no solicitadas.
No romper la simplicidad del template.

Este proyecto es una **herramienta docente**, no un framework.
