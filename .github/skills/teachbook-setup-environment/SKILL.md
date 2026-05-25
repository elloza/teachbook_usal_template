---
name: teachbook-setup-environment
description: >
  Prepara el entorno completo desde cero: detecta/instala Python, git, uv,
  crea el entorno virtual, instala dependencias y sincroniza skills.
  Cubre Windows (x86 + ARM), macOS (Intel + Apple Silicon) y Linux.
  CRÍTICO: usar la primera vez que se abre el proyecto en cualquier ordenador.
  Trigger phrases: "prepara el entorno", "instala todo", "configura el proyecto",
  "setup", "primera vez", "no me funciona", "falta algo", "no compila",
  "ModuleNotFoundError", "command not found", "no tengo python", "no tengo git",
  "Mac", "MacBook", "Windows ARM", "Surface", "Apple Silicon", "M1", "M2", "M3", "M4".
---

# Skill: Preparar Entorno Completo (Desde Cero)

## Cuándo usar esta skill

- Es la **primera vez** que se abre el proyecto en este ordenador.
- Algo no funciona (`ModuleNotFoundError`, `command not found`, errores raros).
- Se ha cambiado de ordenador o se ha clonado el repositorio de nuevo.
- Se han añadido dependencias nuevas a `requirements.txt`.
- El usuario dice: "no tengo python", "no me compila", "falta algo".

## Política estricta para agentes/IDEs

El proyecto usa **un único entorno virtual oficial**: `.venv/` en la raíz del
repositorio.

Prohibido:

- Crear `.venv2`, `.venv-linux`, `.venv_windows_backup`, `env/`, `venv/`,
  `/tmp/teachbook_venv` u otros entornos paralelos.
- Instalar dependencias globalmente.
- Cambiar versiones de dependencias para "probar" sin permiso explícito.
- Arreglar un `.venv` roto moviéndolo a backups dentro del repo.

Si `.venv` existe pero no corresponde al sistema actual (por ejemplo, venv de
Windows ejecutado desde WSL), el agente debe **parar y explicar el conflicto**.
Solo debe recrear `.venv` si el usuario lo pide explícitamente.

Para lanzar la preview, NO preparar entornos nuevos: usar
`python scripts/launch_preview.py`.

---

## Paso 0: Diagnóstico del sistema

**OBLIGATORIO.** El agente DEBE ejecutar estos checks ANTES de hacer cualquier otra cosa:

```bash
# Sistema operativo
uname -a                    # Linux/macOS
systeminfo | findstr /B /C:"OS Name" /C:"OS Architecture"   # Windows CMD
# O en PowerShell:
[System.Environment]::OSVersion.VersionString; $env:PROCESSOR_ARCHITECTURE

# Herramientas
python --version 2>&1 || python3 --version 2>&1 || py --version 2>&1 || echo "NO PYTHON"
git --version 2>&1 || echo "NO GIT"
uv --version 2>&1 || echo "NO UV"

# Arquitectura del procesador
uname -m                    # Linux/macOS: "arm64" = ARM, "x86_64" = Intel
echo %PROCESSOR_ARCHITECTURE%  # Windows CMD: "AMD64" = Intel/AMD, "ARM64" = ARM

# Entorno virtual
test -d .venv && echo "VENV EXISTS" || echo "NO VENV"
```

**Tabla de arquitecturas:**

| Resultado `uname -m` | Resultado Windows | Significado |
|---|---|---|
| `x86_64` / `amd64` | `AMD64` | Intel/AMD 64-bit (lo más común) |
| `arm64` / `aarch64` | `ARM64` | ARM 64-bit (Apple Silicon M1-M4, Windows ARM) |

---

## Paso 1: Instalar lo que falte

### Escenario A: No hay Python

**macOS (Intel y Apple Silicon):**
```bash
# Opción 1: Homebrew (recomendado)
brew install python@3.12

# Opción 2: Descargar de https://python.org
# Los instaladores de python.org detectan Apple Silicon automáticamente

# Opción 3: Si ya tienes uv (ver Escenario C):
uv python install 3.12
```

**Windows (x86 y ARM):**
1. Descargar desde https://python.org
2. **CRÍTICO**: Marcar **"Add Python to PATH"** durante la instalación
3. Verificar abriendo una NUEVA terminal: `py --version`
4. Si `py` funciona pero `python` no, usar `py` en todos los comandos

> **Windows ARM** (Surface Pro X, Snapdragon laptops): Los paquetes Python compilados (numpy, pandas) deberían funcionar vía emulación x86. Si fallan, usar `uv pip install` que maneja mejor las ruedas compatibles.

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install python3 python3-venv python3-pip
```

**Alternativa universal (si se instala uv primero):**
```bash
uv python install 3.12    # uv descarga y gestiona Python automáticamente
```

### Escenario B: No hay git

**macOS:**
```bash
xcode-select --install    # Instala herramientas de línea de comandos (incluye git)
# O: brew install git
```

**Windows:**
- Descargar desde https://git-scm.com
- En Windows ARM: funciona nativamente, no hay problema

**Linux (Ubuntu/Debian):**
```bash
sudo apt install git
```

### Escenario C: No hay uv (pero Python ya existe)

uv es **muy recomendable** — 10-100x más rápido que pip y puede gestionar versiones de Python.

**Windows PowerShell:**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Después de instalar uv, recargar el PATH:**
- macOS/Linux: `source ~/.zshrc` (o `source ~/.bashrc` si usa bash)
- O cerrar y reabrir la terminal
- Windows: cerrar y reabrir la terminal

> **Nota**: uv funciona nativamente en Apple Silicon y Windows ARM.
> `scripts/setup_env.py --yes` usa el instalador oficial de uv y, si este falla en Windows/CI, aplica fallback automático con `python -m pip install uv` y actualiza el `PATH` de la sesión.

### Escenario D: Python no es 3.12

**Si uv está disponible:**
```bash
uv python install 3.12    # uv descarga Python 3.12 automáticamente
uv venv .venv --python 3.12 --seed   # Crea venv con pip incluido
```

**Si no:**
- Descargar Python 3.12 desde https://python.org o dejar que `setup_env.py --yes` lo instale con uv

---

## Paso 2: Ejecutar setup_env.py

Solo después de que los prerrequisitos estén cubiertos:

| Situación | Comando |
|---|---|
| Primera instalación guiada | `python scripts/setup_env.py --yes` (o `py scripts/setup_env.py --yes` en Windows) |
| Instalar y medir tiempos | `python scripts/setup_env.py --yes --profile` |
| Añadir soporte PDF | `python scripts/setup_env.py --yes --extras pdf` |
| Añadir notebooks científicos | `python scripts/setup_env.py --yes --extras notebooks` |
| Añadir importación PDF→Markdown | `python scripts/setup_env.py --yes --extras pdf-import` |
| Instalar todos los extras | `python scripts/setup_env.py --yes --all` |
| `.venv` ya existe con Python 3.12 | Se reutiliza e instala/actualiza dependencias |
| `.venv` ya existe con otra versión | El script se para; ejecutar `python scripts/setup_env.py --recreate --yes` solo si se quiere recrear |
| Solo sincronizar skills (venv ya existe) | `python scripts/setup_env.py --sync-only` |
| Modo desarrollo (con herramientas de test) | `python scripts/setup_env.py --yes --dev` |
| Perfilar dependencias sin instalar | `python scripts/profile_dependencies.py --dry-run --requirements requirements.txt requirements-pdf.txt` |
| Perfilar instalación real temporal | `python scripts/profile_dependencies.py --real-install --requirements requirements.txt --json .build_logs/dependency_profile.json` |

El script hace todo automáticamente:
1. Detecta OS/arquitectura y estado de `.venv`
2. Detecta/instala uv si hace falta
3. Instala/localiza Python 3.12 con `uv python install 3.12`
4. Crea `.venv/` con `uv venv .venv --python 3.12 --seed`
5. Instala dependencias base con uv
6. Verifica paquetes clave con `importlib.metadata`, sin depender de `pip freeze`
7. Comprueba que `pip` existe y que `manim` no está instalado
8. Instala extras opcionales solo si se piden (`pdf`, `notebooks`, `pdf-import`, `dev`)
9. Sincroniza skills a `.claude/skills/`, `.agents/skills/`, `.agent/skills/`
10. Sincroniza `AGENTS.md` a `.github/copilot-instructions.md`
11. Muestra resumen final con el estado de todo

### Capas de dependencias

| Archivo | Uso |
|---|---|
| `requirements.txt` | Instalación base ligera: build HTML, preview, citas, Kroki, Thebe y assets |
| `requirements-pdf.txt` | Exportación PDF y conversión SVG/LaTeX |
| `requirements-notebooks.txt` | Ejecución local de notebooks científicos |
| `requirements-pdf-import.txt` | Conversión PDF→Markdown; puede arrastrar dependencias pesadas |
| `requirements-dev.txt` | Tests y herramientas de desarrollo |

---

## Paso 3: Verificación final

Después del setup, el agente DEBE verificar que todo está bien:

```bash
# 1. El venv existe y tiene Python correcto
.venv/bin/python --version          # Linux/macOS
.venv\Scripts\python.exe --version  # Windows

# 2. jupyter-book está instalado
.venv/bin/python -c "import jupyter_book; print('OK')"          # Linux/macOS
.venv\Scripts\python.exe -c "import jupyter_book; print('OK')"  # Windows

# 3. Skills sincronizadas (carpetas existen con contenido)
ls .claude/skills/ .agents/skills/ .agent/skills/
```

Resultado esperado:
- ✅ Entorno listo — informar al usuario
- ❌ Si algo falla — consultar la tabla de troubleshooting

---

## Tabla de Troubleshooting Completa

| Problema | Causa | Solución |
|---|---|---|
| `python: command not found` (Mac) | Python no instalado o no en PATH | Probar `python3`. Si tampoco: instalar via brew o python.org |
| `python: command not found` (Windows) | Python no instalado o no en PATH | Probar `py`. Si tampoco: instalar desde python.org marcando "Add to PATH" |
| `py: command not found` (Windows) | Python no instalado | Instalar desde python.org |
| `git: command not found` | Git no instalado | macOS: `xcode-select --install`. Windows: git-scm.com |
| `uv: command not found` después de instalar | Shell no recargó el PATH | Cerrar y reabrir la terminal. Mac/Linux: `source ~/.zshrc` |
| Error creating venv | Python no tiene venv (Linux) | `sudo apt install python3-venv` |
| Error de permisos | Usando sudo | NO usar sudo. Todo se instala en el directorio del usuario |
| `pip` falla con SSL (macOS) | Certificados no instalados | `/Applications/Python\ 3.12/Install\ Certificates.command` |
| Deps fallan al instalar (Linux) | Falta compilador | `sudo apt install build-essential python3-dev` |
| Windows: `Scripts` vs `bin` | Windows usa `Scripts\` | Usar `.venv\Scripts\python.exe` |
| Windows: "cannot run scripts" | PowerShell execution policy | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `.venv` usa Python distinto de 3.12 | Entorno creado con otra versión | `python scripts/setup_env.py --recreate --yes` |
| Python del sistema no es 3.12 | Normal en muchos equipos | `setup_env.py --yes` usará uv para instalar/localizar Python 3.12 |
| numpy/pandas fallan en ARM | Ruedas binarias no disponibles | `uv pip install numpy pandas` (uv resuelve ruedas compatibles automáticamente) |
| `jupyter-book: not found` tras setup | venv no activado o PATH | Usar siempre la ruta completa del venv: `.venv/bin/jupyter-book` o `.venv\Scripts\jupyter-book.exe` |
| macOS: "developer tools" popup | Falta Xcode CLI | `xcode-select --install` y esperar a que termine |
| Windows: CRLF vs LF | Git convierte saltos de línea | No afecta funcionalidad. Ignorar los warnings de git |

---

## Notas especiales por sistema operativo

### Windows (x86_64 — Intel/AMD)
- Después de instalar Python, el PATH puede no actualizarse hasta reiniciar la terminal
- El launcher `py` es más fiable que `python`
- Si PowerShell bloquea scripts: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
- Rutas del venv usan `Scripts\` en vez de `bin/`
- Git Bash funciona como terminal alternativa

### Windows (ARM64 — Surface Pro X, Snapdragon)
- Python funciona via emulación x86_64 (transparente al usuario)
- uv funciona nativamente en ARM
- Los paquetes compilados (numpy, pandas, matplotlib) pueden tardar más la primera vez
- Si un paquete falla: `uv pip install --force-reinstall <paquete>` para forzar recompilación

### macOS (Intel — MacBook Pro/Air hasta 2020)
- `python3` suele estar disponible por defecto
- Si pip falla por SSL: ejecutar `Install Certificates.command` en `/Applications/Python 3.12/`
- Homebrew recomendado: `brew install python@3.12 git`

### macOS (Apple Silicon — M1/M2/M3/M4)
- **Python**: Los instaladores de python.org son Universal2 (funcionan nativamente)
- **Homebrew**: Instalar la versión nativa (no la de Rosetta): `brew install python@3.12 git`
- **uv**: Funciona nativamente, muy rápido
- **numpy/pandas/scipy**: Disponibles como wheels nativos ARM desde PyPI. No deberían dar problemas.
- **Si Homebrew no se instaló nativo** (está en `/usr/local/` en vez de `/opt/homebrew/`):
  ```bash
  # Verificar: si dice /usr/local, es Rosetta (lento)
  # Si dice /opt/homebrew, es nativo (rápido)
  brew --prefix
  ```
- **Tectonic (LaTeX)**: Descarga el binario `aarch64-apple-darwin` nativo. El script `setup_latex.py` lo detecta automáticamente.

### Linux (Ubuntu/Debian)
- Puede necesitar `python3-venv`: `sudo apt install python3-venv`
- Puede necesitar herramientas de compilación: `sudo apt install build-essential python3-dev`
- El comando puede ser `python3` en vez de `python`

---

## Problemas conocidos no comprobables en todos los entornos

El proyecto se prueba automáticamente en **Windows** y **macOS** mediante GitHub Actions. Sin embargo:

| Plataforma | Estado tests | Notas |
|---|---|---|
| Windows x86_64 | ✅ Probado en CI | Funciona correctamente |
| macOS Apple Silicon | ✅ Probado en CI | Funciona correctamente |
| macOS Intel | ⚠️ No probado en CI | Debería funcionar igual que ARM |
| Windows ARM | ⚠️ No probado | Emulación x86 debería funcionar |
| Linux x86_64 | ✅ Probado en CI | Solo syntax check |
| Linux ARM | ❌ No probado | Poco probable en docentes |

Si un usuario tiene problemas en una plataforma no probada, el agente debe:
1. Seguir la tabla de troubleshooting habitual
2. Si no encuentra solución, sugerir instalar Python y uv desde cero
3. Último recurso: abrir un issue en GitHub reportando el problema

---

## Después del setup

El entorno está listo. Siguiente paso: compilar el libro.

```bash
# Compilar HTML multi-idioma
.venv/bin/python scripts/build_book.py          # Linux/macOS
.venv\Scripts\python.exe scripts/build_book.py  # Windows

# Vista previa en localhost:8000
python scripts/launch_preview.py          # recomendado: detecta el .venv correcto
```
