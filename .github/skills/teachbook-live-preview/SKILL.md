---
name: teachbook-live-preview
description: >
  Inicia un servidor local con previsualización en vivo del libro usando el
  MISMO pipeline que producción: scripts/build_book.py + servidor estático.
  Compatible con Windows, macOS, Linux y WSL. Evita previews obsoletas al
  recompilar antes de abrir el navegador y servir con cabeceras no-cache.
  Trigger phrases: "vista previa", "preview", "en vivo", "live", "quiero ver el libro",
  "abre el navegador", "servidor local", "hot reload", "ver cambios en tiempo real",
  "enséñame cómo queda", "previsualizar".
---

# Skill: Previsualización en Vivo (Live Preview)

## Principio fundamental

Esta skill está pensada para agentes de código e IDEs. La regla principal es:

> **NO improvisar entornos. NO crear `.venv2`, `.venv-linux`, `/tmp/venv`,
> `env/`, ni instalar dependencias fuera del `.venv` del proyecto.**

Si el entorno no está bien, el agente debe **parar y mostrar el diagnóstico**.
No debe intentar "arreglarlo" creando entornos paralelos.

La preview DEBE usar el mismo resultado que se publica:

```text
scripts/build_book.py  →  book/_build/html  →  servidor local
```

NO usar `sphinx-autobuild` directamente en este proyecto. Este TeachBook tiene
un build multiidioma personalizado con `_config_es.yml`, `_config_en.yml`,
`_toc_es.yml`, `_toc_en.yml` y postprocesados propios. Un Sphinx genérico puede
usar configuración incompleta y mostrar contenido viejo, rutas rotas o funciones
que no coinciden con la web final.

## Qué hace `preview_book.py`

1. Verifica que `.venv` funciona en el sistema operativo actual.
2. Ejecuta `scripts/build_book.py` antes de abrir el navegador.
3. Sirve exactamente `book/_build/html`.
4. Añade cabeceras HTTP `no-cache` para evitar HTML viejo del navegador.
5. Vigila cambios en `book/` mediante sondeo portable y recompila con el mismo
   `build_book.py`.
6. Abre el navegador automáticamente en Windows, macOS, Linux y WSL.

## Comando único para agentes/IDEs

Los agentes deben ejecutar SIEMPRE este lanzador conservador.

### Si lo lanza un agente de código

Usar modo segundo plano para no quedarse bloqueado:

```bash
python scripts/launch_preview.py --background
```

Después comprobar estado/log:

```bash
python scripts/launch_preview.py --status
python scripts/launch_preview.py --log
```

Para detenerlo:

```bash
python scripts/launch_preview.py --stop
```

El agente debe esperar a ver en el log:

```text
✅ Build correcto
🌐 Preview listo: http://localhost:XXXX
```

### Si lo lanza una persona en una terminal

Puede usarse en primer plano:

```bash
python scripts/launch_preview.py
```

Si `python` no existe:

```bash
python3 scripts/launch_preview.py   # macOS/Linux/WSL
py scripts/launch_preview.py        # Windows
```

`launch_preview.py` detecta el sistema operativo, localiza el `.venv` correcto,
evita previews duplicadas y delega en `scripts/preview_book.py`. Si el `.venv`
no corresponde al sistema actual, mostrará instrucciones y terminará.
**No crea entornos nuevos.**

## Script interno

`scripts/preview_book.py` es el servidor interno que ejecuta el build real y
sirve `book/_build/html`. No lo invoques directamente desde un agente salvo que
el usuario lo pida explícitamente. El punto de entrada seguro es siempre
`scripts/launch_preview.py`.

Opciones útiles:

```bash
# Usar otro puerto
python scripts/launch_preview.py --port 8010

# No abrir navegador automáticamente
python scripts/launch_preview.py --no-browser

# Compilar una vez y servir sin vigilar cambios
python scripts/launch_preview.py --no-watch
```

## Prohibido para agentes

No hacer nada de esto:

- No ejecutar `sphinx-autobuild` directamente.
- No ejecutar `python -m http.server` sobre carpetas antiguas.
- No crear entornos alternativos (`.venv_linux`, `.venv2`, `/tmp/venv`, etc.).
- No instalar paquetes globalmente.
- No cambiar versiones de dependencias por iniciativa propia.
- No abrir el navegador hasta que aparezca `✅ Build correcto` y `🌐 Preview listo`.

## Comportamiento esperado

- La primera vez tarda porque compila el libro completo en todos los idiomas.
- Después, cada cambio en `.md`, `.ipynb`, `.yml`, imágenes, CSS, JS o BibTeX
  provoca una recompilación completa usando `build_book.py`.
- La URL habitual es `http://localhost:8000`.
- Si el puerto está ocupado, usa automáticamente el siguiente libre.

## Si el usuario ve contenido viejo

1. Confirmar que está entrando en la URL que imprime el script.
2. Pedir `Ctrl+F5` en el navegador.
3. Verificar que el log dice `✅ Build correcto` antes de `🌐 Preview listo`.
4. Si el build falla, NO confiar en la web anterior: arreglar primero el error.

## WSL y entornos virtuales

Si se ejecuta en WSL, `.venv` debe ser un venv Linux (`.venv/bin/python`).
Un `.venv` creado en Windows (`.venv\Scripts\python.exe`) no funciona dentro de
WSL. En ese caso, usar PowerShell o recrear el entorno desde WSL.

## Detener el servidor

Pulsar `Ctrl+C` en la terminal donde está corriendo.
