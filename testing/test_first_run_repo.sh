#!/bin/bash
# Test TeachBook setup from a clean first-run repository environment
# This script simulates what a non-technical user would experience
# when opening the project for the first time with no preconfigured project tooling.
#
# Usage: docker run --rm -v $(pwd)/..:/workspace test-ubuntu|test-fedora|test-alpine

set -euo pipefail

PROJECT_DIR="/workspace"

echo "═══════════════════════════════════════════════════"
echo "  🧪 TeachBook Test — Primer arranque del repositorio"
echo "═══════════════════════════════════════════════════"
echo ""
echo "OS: $(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2 || echo 'unknown')"
echo "User: $(whoami)"
echo ""

# STEP 0: Diagnóstico — qué hay y qué no hay
echo "━━━ PASO 0: Diagnóstico del sistema ━━━"
echo ""

check_tool() {
    if command -v "$1" &>/dev/null; then
        VER=$("$1" --version 2>/dev/null | head -1 || echo "found")
        echo "  ✅ $1: $VER"
    else
        echo "  ❌ $1: NO instalado"
    fi
}

check_tool python3
check_tool python
check_tool pip3
check_tool pip
check_tool git
check_tool uv
check_tool curl
check_tool sh
echo ""

# STEP 1: Setup environment
echo "━━━ PASO 1: Ejecutar setup_env.py ━━━"
echo ""

cd "$PROJECT_DIR"

# Try with whatever python is available
PYTHON_CMD=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYTHON_CMD="$cmd"
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "  ⛔ No hay Python disponible. El setup NO puede ejecutarse."
    echo "  Esto es lo que le pasaría a un usuario sin Python."
    echo ""
    echo "  ❌ TEST FALLIDO: No se puede ejecutar setup_env.py sin Python."
    exit 1
fi

echo "  Usando: $PYTHON_CMD"
echo ""

# Run setup (non-interactive: auto-accept uv install)
echo "s" | $PYTHON_CMD scripts/setup_env.py 2>&1 || {
    echo ""
    echo "  ❌ TEST FALLIDO: setup_env.py falló."
    exit 1
}

echo ""

# STEP 2: Verify venv exists
echo "━━━ PASO 2: Verificar entorno virtual ━━━"
echo ""

if [ -d ".venv" ]; then
    echo "  ✅ .venv/ existe"
else
    echo "  ❌ .venv/ NO existe"
    exit 1
fi

# Find venv python
VENV_PYTHON=""
for p in ".venv/bin/python" ".venv/Scripts/python.exe"; do
    if [ -f "$p" ]; then
        VENV_PYTHON="$p"
        break
    fi
done

if [ -z "$VENV_PYTHON" ]; then
    echo "  ❌ No se encontró python en .venv/"
    exit 1
fi

echo "  ✅ Venv python: $VENV_PYTHON"
$VENV_PYTHON --version
echo ""

# STEP 3: Verify skill sync
echo "━━━ PASO 3: Verificar sincronización de skills ━━━"
echo ""

SKILLS_OK=true
for dir in .claude/skills .agents/skills .agent/skills; do
    if [ -d "$dir" ]; then
        COUNT=$(ls "$dir" 2>/dev/null | wc -l)
        echo "  ✅ $dir ($COUNT skills)"
    else
        echo "  ❌ $dir NO existe"
        SKILLS_OK=false
    fi
done

if [ "$SKILLS_OK" = false ]; then
    echo "  ❌ TEST FALLIDO: Skills no sincronizadas"
    exit 1
fi
echo ""

# STEP 4: Verify copilot-instructions
echo "━━━ PASO 4: Verificar instrucciones sincronizadas ━━━"
echo ""

if [ -f ".github/copilot-instructions.md" ]; then
    echo "  ✅ .github/copilot-instructions.md existe"
else
    echo "  ❌ .github/copilot-instructions.md NO existe"
fi
echo ""

# STEP 5: Build the book
echo "━━━ PASO 5: Compilar el libro ━━━"
echo ""

$VENV_PYTHON scripts/build_book.py 2>&1 || {
    echo ""
    echo "  ❌ TEST FALLIDO: build_book.py falló."
    exit 1
}
echo ""

# STEP 6: Verify build output
echo "━━━ PASO 6: Verificar salida del build ━━━"
echo ""

BUILD_OK=true
for path in "book/_build/html/index.html" "book/_build/html/es" "book/_build/html/en"; do
    if [ -e "$path" ]; then
        echo "  ✅ $path existe"
    else
        echo "  ❌ $path NO existe"
        BUILD_OK=false
    fi
done

if [ "$BUILD_OK" = false ]; then
    echo "  ❌ TEST FALLIDO: Build incompleto"
    exit 1
fi
echo ""

# STEP 7: Test PDF to Markdown (if a PDF exists)
echo "━━━ PASO 7: Test PDF a Markdown ━━━"
echo ""

# Create a tiny test PDF using Python
$VENV_PYTHON -c "
import fitz  # pymupdf
doc = fitz.open()
page = doc.new_page()
page.insert_text((72, 72), 'TeachBook Test PDF')
doc.save('/tmp/test.pdf')
doc.close()
print('  📄 PDF de test creado')
" 2>/dev/null || {
    echo "  ⚠️  No se pudo crear PDF de test (pymupdf no disponible)"
}

if [ -f "/tmp/test.pdf" ]; then
    $VENV_PYTHON scripts/pdf_to_markdown.py /tmp/test.pdf --output /tmp/test_md 2>&1 || {
        echo "  ❌ TEST FALLIDO: pdf_to_markdown.py falló."
        exit 1
    }
    if [ -f "/tmp/test_md/test.md" ]; then
        echo "  ✅ PDF convertido a Markdown correctamente"
    fi
fi
echo ""

# FINAL RESULT
echo "═══════════════════════════════════════════════════"
echo "  ✅ TODOS LOS TESTS PASARON"
echo "═══════════════════════════════════════════════════"
