---
name: teachbook-pdf-to-markdown
description: >
  Convierte archivos PDF a Markdown para incluirlos en el libro.
  Extrae texto, imágenes y estructura básica. Compatible con HTML y PDF.
  Trigger phrases: "convertir PDF", "PDF a markdown", "importar PDF",
  "pasar PDF a texto", "extraer PDF", "importar apuntes", "PDF a MD",
  "convert pdf", "import document".
---

# Skill: PDF a Markdown

## Cuándo usar esta skill

- Cuando el docente tiene apuntes, diapositivas o materiales en PDF y quiere incorporarlos al libro.
- Para convertir PDFs existentes en Markdown editable como punto de partida.
- Al importar documentos de texto que estaban en formato PDF.

## Qué hace `pdf_to_markdown.py`

1. **Verifica e instala** `pymupdf4llm` automáticamente si no está disponible.
2. **Convierte PDF a Markdown** preservando títulos, listas y estructura básica.
3. **Opcionalmente extrae imágenes** y las guarda con directivas MyST `{image}`.
4. **Soporta archivo individual o directorio completo** (búsqueda recursiva).

## Requisitos previos

El entorno virtual base debe estar configurado. La importación PDF vive en un extra separado porque arrastra dependencias pesadas:

```bash
python scripts/setup_env.py --yes
python scripts/setup_env.py --yes --extras pdf-import
```

El script también intenta instalar `pymupdf4llm` automáticamente si no lo encuentra, pero para una instalación reproducible es mejor usar el extra `pdf-import`.

## Comandos

El agente DEBE usar el Python del entorno virtual (`.venv`):

| Sistema | Comando base |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/pdf_to_markdown.py` |
| Windows | `.venv\Scripts\python.exe scripts\pdf_to_markdown.py` |

### Ejemplos de uso

**Convertir un solo archivo:**
```bash
python scripts/pdf_to_markdown.py apuntes.pdf
# Genera: apuntes.md (en el mismo directorio)
```

**Convertir un directorio completo:**
```bash
python scripts/pdf_to_markdown.py mis_apuntes/
# Convierte TODOS los PDFs encontrados recursivamente
```

**Especificar directorio de salida:**
```bash
python scripts/pdf_to_markdown.py apuntes.pdf --output book/es/03_nuevo_capitulo/
```

**Extraer imágenes también:**
```bash
python scripts/pdf_to_markdown.py apuntes.pdf --images
# Genera: apuntes.md + carpeta apuntes_images/ con las imágenes
```

**Combinar opciones:**
```bash
python scripts/pdf_to_markdown.py mis_apuntes/ --output book/es/03_nuevo_capitulo/ --images
```

## Formato de salida

Para cada `archivo.pdf`:

| Archivo | Descripción |
|---|---|
| `archivo.md` | Markdown con el texto extraído |
| `archivo_images/` | Carpeta con imágenes (solo con `--images`) |

Cada archivo `.md` generado incluye un comentario inicial:

```html
<!-- Convertido automáticamente desde PDF. Revisar y corregir formato si es necesario. -->
```

Las imágenes se referencian con directivas MyST compatibles con HTML y PDF:

```markdown
```{image} archivo_images/page1_img1.png
:alt: Imagen extraída del PDF
:width: 80%
:align: center
```
```

## Pasos POST-conversión (obligatorios)

Después de convertir, el agente DEBE:

### 1. Revisar la calidad del Markdown

- Verificar que los títulos tienen la jerarquía correcta (`#`, `##`, `###`).
- Comprobar que las listas y párrafos están bien formateados.
- Revisar que no hay texto corrupto o caracteres extraños.

### 2. Corregir problemas comunes

- **Tablas complejas**: pueden necesitar ajuste manual a formato MyST.
- **Fórmulas matemáticas**: convertirlas a LaTeX (`$...$` o `$$...$$`).
- **Imágenes sin contexto**: añadir descripciones alternativas (`:alt:`) significativas.
- **Páginas en blanco**: eliminar las marcas de salto de página sobrantes.

### 3. Integrar en el libro

Si el contenido va a formar parte del libro, seguir la skill **`teachbook-add-content`**:

1. Colocar el `.md` revisado en la carpeta del idioma correspondiente (`book/es/` y `book/en/`).
2. Crear la versión en el otro idioma (o placeholder: `*(Traducción pendiente)*`).
3. Actualizar TODOS los `_toc_<lang>.yml` con la nueva entrada.
4. Si se extrajeron imágenes, mover la carpeta `_images/` junto al `.md` o a `book/_static/`.
5. Ajustar las rutas de las imágenes en el Markdown si es necesario.

## Limitaciones

| Limitación | Detalle |
|---|---|
| **PDFs escaneados** | Si el PDF es una imagen de texto (escaneado), no se extraerá texto. Se necesitaría OCR previo. |
| **Tablas complejas** | Las tablas con celdas combinadas o anidadas pueden no convertirse correctamente y requerir ajuste manual. |
| **Fórmulas** | Las ecuaciones matemáticas se extraen como texto plano. Hay que convertirlas manualmente a LaTeX. |
| **Diapositivas** | Las presentaciones tipo slide suelen tener poco texto por página; el resultado puede ser fragmentado. |
| **Columnas** | Los diseños a varias columnas pueden mezclar el texto de ambas columnas. |
| **No es contenido final** | El resultado es un **PUNTO DE PARTIDA** que siempre requiere revisión y edición manual. |

## Solución de problemas

| Problema | Solución |
|---|---|
| "No se encontró el entorno virtual" | Ejecutar `python scripts/setup_env.py --yes` primero |
| "Error instalando pymupdf4llm" | Ejecutar `.venv/bin/python scripts/setup_env.py --yes --extras pdf-import` |
| Texto ilegible o basura | El PDF probablemente es escaneado; se necesita OCR |
| Faltan imágenes | Usar la bandera `--images` para extraerlas |
| Las rutas de imágenes no funcionan | Ajustar rutas relativas según la ubicación final del `.md` |
