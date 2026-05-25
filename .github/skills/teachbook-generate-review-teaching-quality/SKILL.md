---
name: teachbook-generate-review-teaching-quality
description: >
  Revisa el contenido existente del libro evaluando la calidad didáctica y técnica.
  Genera un informe con checklist de verificación (✅/❌/⚠️) y ofrece corregir los problemas.
  Trigger phrases: "revisar", "calidad", "mejorar", "revisión", "review", "auditar contenido",
  "auditar", "checklist", "verificar contenido", "mejorar página".
---

# Skill: Revisar Calidad Docente

## Objetivo

Revisar páginas o secciones del libro y generar un informe de calidad con criterios pedagógicos y técnicos. Tras la revisión, ofrecer correcciones automáticas.

## Checklist de revisión

El agente debe evaluar CADA uno de los siguientes criterios:

### Criterios pedagógicos

| # | Criterio | Qué verificar |
|---|---|---|
| 1 | **Objetivo de aprendizaje** | ¿Hay un objetivo claro al inicio de la página/sección? |
| 2 | **Lenguaje accesible** | ¿Hay jerga técnica innecesaria? ¿El lenguaje es comprensible para el público objetivo? |
| 3 | **Ejemplos incluidos** | ¿Hay al menos un ejemplo práctico o caso aplicado? |
| 4 | **Visualizaciones** | ¿Hay gráficas, diagramas, tablas o imágenes que refuercen el contenido? |
| 5 | **Ejercicios propuestos** | ¿Se proponen ejercicios o preguntas al estudiante? |
| 6 | **Longitud adecuada** | ¿La página tiene más de 200 líneas? Si es así, sugerir dividirla. |

### Criterios técnicos

| # | Criterio | Qué verificar |
|---|---|---|
| 7 | **Código/diagramas funcionales** | ¿El código Python o diagramas Mermaid tienen sintaxis correcta? |
| 8 | **Sincronización multi-idioma** | ¿El contenido existe en TODOS los idiomas con la misma estructura? |
| 9 | **Archivos huérfanos** | ¿Hay archivos `.md`/`.ipynb` que no estén en el `_toc_<lang>.yml`? |
| 10 | **Entradas huérfanas en TOC** | ¿Hay entradas en `_toc_<lang>.yml` que apunten a archivos inexistentes? |
| 11 | **Compatibilidad PDF** | ¿Los elementos multimedia tienen fallback para PDF (`{raw} latex`)? |
| 12 | **Enlaces internos** | ¿Los enlaces entre páginas del libro funcionan (no 404)? |

## Formato del informe

```markdown
# Informe de Revisión: [nombre de la página/sección]

## Resumen
- **Páginas revisadas:** X
- **Problemas encontrados:** Y
- **Críticos:** Z

## Detalle por página

### `es/02_grados/grado_fisica/intro.md`

| # | Criterio | Estado | Notas |
|---|---|---|---|
| 1 | Objetivo de aprendizaje | ❌ | No hay objetivo explícito al inicio |
| 2 | Lenguaje accesible | ✅ | Lenguaje claro y directo |
| 3 | Ejemplos incluidos | ⚠️ | Hay ejemplos pero solo teóricos, sin aplicación práctica |
| 4 | Visualizaciones | ✅ | Incluye diagrama Mermaid y tabla |
| 5 | Ejercicios propuestos | ❌ | No hay ejercicios |
| 6 | Longitud adecuada | ✅ | 85 líneas |
| 7 | Código funcional | ✅ | Sintaxis correcta |
| 8 | Multi-idioma | ⚠️ | Existe en EN pero con contenido placeholder |
| 9 | Sin huérfanos | ✅ | Archivo referenciado en TOC |
| 10 | TOC sin entradas rotas | ✅ | TOC correcto |
| 11 | Compatibilidad PDF | ❌ | Video de YouTube sin fallback LaTeX |
| 12 | Enlaces internos | ✅ | Todos los enlaces funcionan |

## Problemas críticos
1. **[es/intro.md]** Falta objetivo de aprendizaje → Sugerir añadido.
2. **[es/02_grados/.../intro.md]** Video sin fallback LaTeX → Añadir bloque `{raw} latex`.

## Sugerencias de mejora
1. Añadir objetivo de aprendizaje al inicio de cada página.
2. Completar traducción pendiente en la versión en inglés.
3. Añadir 2-3 ejercicios tipo test al final de la sección.
```

## Flujo de trabajo

1. **Identificar alcance** — Preguntar qué página/sección/capítulo revisar. Si no especifica, revisar todo el libro.
2. **Leer los archivos** — Leer el contenido de cada archivo y su equivalente en otros idiomas.
3. **Verificar TOC** — Leer `_toc_<lang>.yml` para cada idioma y cruzar con archivos existentes.
4. **Evaluar cada criterio** — Aplicar el checklist completo a cada página.
5. **Generar informe** — Usar el formato de arriba con ✅/❌/⚠️.
6. **Ofrecer correcciones** — Preguntar si el usuario quiere que se corrijan automáticamente los problemas encontrados.

## Cómo verificar sincronización multi-idioma

```
Para cada idioma (es, en, ...):
  1. Listar archivos en book/<lang>/
  2. Leer _toc_<lang>.yml
  3. Cruce: archivos sin TOC = huérfanos, TOC sin archivo = rotos

Comparar estructuras:
  - ¿Mismo número de secciones?
  - ¿Mismo orden?
  - ¿Mismos niveles de profundidad?
```

## Cómo verificar compatibilidad PDF

Buscar en cada archivo:
- ` ```{raw} html` sin un ` ```{raw} latex` correspondiente → ❌
- Videos YouTube sin fallback → ❌
- Mermaid diagrams (no renderizan en PDF) → ⚠️ (avisar)
- Imágenes con `{image}` → ✅
- Ecuaciones LaTeX → ✅
