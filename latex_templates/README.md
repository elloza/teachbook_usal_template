# Plantillas LaTeX Personalizadas

Esta carpeta permite personalizar la generación de PDFs del libro.
El script `scripts/export_pdf.py` buscará archivos aquí y los copiará sobre la carpeta de compilación de LaTeX antes de generar el PDF.

## Estructura

*   `common/`: Archivos comunes para **todos** los idiomas.
    *   Aquí debería ir `jupyterBook.cls` si tiene personalizaciones (ej: macros matemáticas).
    *   También puedes poner logos o estilos globales.

*   `es/`, `en/`, `fr/`, etc.: Archivos específicos para cada idioma.
    *   El script buscará una carpeta con el código del idioma (ej: `es`).
    *   Los archivos aquí **sobrescribirán** a los de `common/` y a los generados automáticamente.
    *   Úsalo para portadas traducidas, preámbulos específicos, etc.

## Ejemplo de uso
Si quieres una portada diferente para inglés:
1.  Crea `latex_templates/en/custom_cover.sty`.
2.  Al generar el PDF en inglés, este archivo se copiará y se usará.
