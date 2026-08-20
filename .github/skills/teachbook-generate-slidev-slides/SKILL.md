---
name: teachbook-generate-slidev-slides
description: >
  Crea o actualiza diapositivas Slidev multi-idioma asociadas a capítulos padre
  del TeachBook. Usa una deck por capítulo del TOC; las sections heredan esa deck.
  Trigger phrases: "slides", "diapositivas", "slidev", "presentación",
  "presentacion", "crear diapositivas", "actualizar slides", "deck".
---

# Skill: Generar Diapositivas Slidev

## Regla obligatoria

> Las diapositivas son contenido docente y deben existir en **TODOS los idiomas** configurados. Si se crea o actualiza una deck en `slides/es/`, debe existir la deck equivalente en `slides/en/` y en cualquier otro idioma activo.

> La unidad de trabajo es **una deck por capítulo padre del TOC**. No crear decks independientes para entradas `sections:` en v1; esas páginas apuntan a la deck del capítulo al que pertenecen.

## Estructura esperada

Las fuentes viven bajo `slides/`:

```text
slides/
├── package.json
├── components/
├── layouts/
├── styles/
├── public/
├── es/<ruta-del-capitulo>/slides.md
└── en/<ruta-del-capitulo>/slides.md
```

Ejemplo:

```text
book/es/02_grados/grado_fisica/intro.md
slides/es/02_grados/grado_fisica/intro/slides.md

book/en/02_degrees/physics_degree/intro.md
slides/en/02_degrees/physics_degree/intro/slides.md
```

## Proceso para crear o actualizar una deck

1. Identificar el capítulo padre en `book/_toc_<lang>.yml`.
2. Confirmar la posición equivalente en todos los idiomas. La posición, no el nombre de carpeta traducido, es la correspondencia multi-idioma.
3. Crear o actualizar `slides/<lang>/<ruta-del-capitulo>/slides.md` en todos los idiomas.
4. Si una traducción no está lista, crear una deck mínima con aviso de contenido pendiente.
5. Mantener títulos, objetivos docentes y ejemplos alineados entre idiomas.
6. No duplicar decks para `sections:`; el manifest debe mapear esas páginas a la deck del capítulo padre.

## Plantilla mínima recomendada

```markdown
---
theme: default
title: Título del capítulo
info: Diapositivas docentes asociadas al TeachBook.
class: text-center
drawings:
  persist: false
transition: slide-left
---

# Título del capítulo

Subtítulo o contexto de la sesión

---

# Objetivos

- Objetivo 1
- Objetivo 2
- Objetivo 3

---

# Idea clave

Contenido pendiente de adaptar.
```

En inglés, traducir el contenido visible. Mantener rutas y nombres de archivo según el idioma correspondiente del TOC.

## Validación obligatoria

Antes de cerrar:

```bash
python scripts/check_encoding.py
python scripts/check_slides_integrity.py
python scripts/build_slides.py
```

Si también se ha tocado el libro:

```bash
python scripts/check_multilang_integrity.py
python scripts/build_book.py
```

## Errores que debes evitar

- Crear una deck solo en un idioma.
- Crear una deck por sección en vez de por capítulo padre.
- Referenciar imágenes externas sin copia o fallback estable cuando formen parte del material docente.
- Editar `.agents/skills/`, `.claude/skills/` o `.agent/skills/` directamente; se regeneran desde `.github/skills/`.
- Publicar manualmente solo la carpeta de Slidev. Las slides deben salir dentro del build del TeachBook.
