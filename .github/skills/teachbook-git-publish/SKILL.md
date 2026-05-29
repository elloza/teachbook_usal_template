---
name: teachbook-git-publish
description: >
  Guarda todos los cambios (git add + commit + push) y los publica automáticamente
  en GitHub Pages mediante GitHub Actions. No requiere conocimientos de Git.
  Trigger phrases: "guarda", "publica", "sube a la web", "commit", "push",
  "guarda mis cambios", "publica la nueva versión", "sube todo",
  "guardar y publicar", "save and publish", "git push", "subir cambios".
---

# Skill: Guardar y Publicar

## Cuándo usar esta skill

- Al terminar una sesión de trabajo y querer guardar los cambios.
- Cuando se quiere que los alumnos vean los cambios en la web.
- Después de compilar y verificar que todo está correcto.

## Qué hace `git_helper.py`

1. **Muestra el estado** de los archivos modificados (`git status`).
2. **Comprueba la codificación UTF-8 localmente** con `scripts/check_encoding.py`.
3. **Añade todos los cambios** al área de staging (`git add .`).
4. **Crea un commit** con mensaje automático basado en la fecha y hora: `"Actualización automática YYYY-MM-DD HH:MM:SS"`.
5. **Sube a GitHub** (`git push`).

Tras el push, **GitHub Actions** se ejecuta automáticamente:
- Compila el libro HTML para todos los idiomas.
- Genera PDFs nuevos para todos los idiomas con `scripts/export_pdf.py --engine auto`.
- Despliega todo a GitHub Pages.

La publicación correcta NO consiste en subir solo HTML. El workflow de Pages debe regenerar primero los PDFs finales de `book/_static/` y después compilar la web que enlaza esos PDFs recientes.

## Instrucciones para el agente

### Ejecutar el guardado y publicación

El agente DEBE usar el Python del entorno virtual (`.venv`):

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/git_helper.py` |
| Windows | `.venv\Scripts\python.exe scripts/git_helper.py` |

`git_helper.py` debe parar antes de publicar si `scripts/check_encoding.py` detecta:
- archivos de texto que no son UTF-8 válido,
- mojibake típico (por ejemplo `U+00C3`, `U+00C2` o secuencias `U+00E2 U+20AC`),
- acentos sustituidos por `?`,
- texto no ASCII dentro de celdas `code` de notebooks.

No hacer `git push` manual si este check falla. Primero corregir el archivo indicado y repetir la comprobación en local.

### Si el script dice "No hay cambios para guardar"

Significa que no se ha modificado ningún archivo desde el último commit. No es un error.

## Requisitos previos para la publicación web

1. **El repositorio debe estar en GitHub** (no solo en local).
2. **GitHub Pages debe estar configurado**:
   - Ir a Settings → Pages → Source: seleccionar **"GitHub Actions"**.
3. **El workflow `deploy.yml`** debe existir en `.github/workflows/`.

## Verificar la publicación

Después de ejecutar `git_helper.py`:
1. Ir al repositorio en GitHub → pestaña **Actions**.
2. Verificar que el workflow se ha ejecutado correctamente (icono verde).
3. Una vez completado, el libro estará disponible en `https://<usuario>.github.io/<repo>/`.

## Solución de problemas

| Problema | Solución |
|---|---|
| `git: command not found` | Instalar Git desde git-scm.com |
| Error de autenticación al push | Configurar credenciales: `git config credential.helper store` o usar SSH |
| "No hay cambios para guardar" | No es un error; no hay archivos nuevos o modificados |
| El workflow de Actions falla | Revisar los logs en GitHub → Actions → click en el workflow fallido |
| La web no se actualiza | Verificar que GitHub Pages usa "GitHub Actions" como source (no "Deploy from branch") |

## Nota importante

El script hace commit de TODO (`git add .`). Si hay archivos que no se deben commitear (ej: archivos temporales grandes), asegurarse de que están en `.gitignore`. Los archivos de build (`book/_build/`) y el entorno virtual (`.venv/`) ya están excluidos por defecto.
