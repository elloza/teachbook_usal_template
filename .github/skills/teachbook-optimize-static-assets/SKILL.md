---
name: teachbook-optimize-static-assets
description: >
  Revisa y optimiza assets estáticos del TeachBook para web sin romper PDF.
  Use when Codex adds, replaces, audits, or prepares images, logos, GIFs, PNG/JPG files,
  WebP fallbacks, or any content under book/_static for publication across Windows,
  macOS, Linux, GitHub Actions, HTML, and PDF.
---

# Skill: Optimizar Assets Estáticos

## Regla

Mantener PNG como formato principal cuando una imagen deba funcionar en HTML y PDF. No convertir referencias existentes a WebP de forma general. WebP solo puede usarse como mejora HTML si existe fallback PNG/JPG y el PDF se ha probado.

## Flujo

1. Guardar assets finales en `book/_static/` con nombres estables.
2. Para GIF animado, guardar también un `.png` con el mismo nombre base junto al `.gif`.
3. Validar:

   | Sistema | Comando |
   |---|---|
   | Windows | `.\.venv\Scripts\python.exe scripts\optimize_static_assets.py --check` |
   | macOS/Linux | `.venv/bin/python scripts/optimize_static_assets.py --check` |

4. Si el check informa PNG/JPG optimizables, aplicar:

   | Sistema | Comando |
   |---|---|
   | Windows | `.\.venv\Scripts\python.exe scripts\optimize_static_assets.py --fix` |
   | macOS/Linux | `.venv/bin/python scripts/optimize_static_assets.py --fix` |

5. Volver a ejecutar `--check`.
6. Si cambian imágenes citadas en páginas, compilar el libro y revisar visualmente HTML/PDF.

## Qué Hace El Script

- Escanea `book/_static/`.
- Optimiza PNG/JPG/JPEG sin cambiar extensión ni rutas.
- No recomprime GIFs para no arriesgar animaciones; solo valida que tengan fallback PNG si están referenciados.
- No toca PDFs, `.bib`, CSS, JS ni SVG.
- Usa Pillow dentro de `.venv`, así que no depende de herramientas nativas del sistema.
- Puede escribir informe JSON con `--report .build_logs/static_assets.json`.

## Cierre Obligatorio

No cerrar una tarea que añade imágenes, logos o GIFs sin comprobar:

- `scripts/optimize_static_assets.py --check`
- `scripts/check_encoding.py`
- `scripts/build_book.py` si la imagen aparece en una página visible
