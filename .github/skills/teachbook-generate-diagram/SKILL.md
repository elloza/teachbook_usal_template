---
name: teachbook-generate-diagram
description: >
  Genera imágenes de diagramas para el libro usando Kroki: Mermaid, PlantUML, GraphViz,
  TikZ, WaveDrom, Excalidraw, etc.
  Los diagramas se renderizan como imágenes SVG que funcionan tanto en HTML como en PDF.
  Trigger phrases: "diagrama", "diagrama de flujo", "ER", "UML", "mermaid",
  "flowchart", "diagrama de clases", "diagrama entidad relación", "diagrama de secuencia",
  "diagrama de estados", "diagrama de gantt", "plantuml", "graphviz", "excalidraw",
  "tikz", "wavedrom", "cronograma digital", "señal digital",
  "kroki", "generar diagrama", "crear diagrama".
---

# Skill: Generar Diagramas con Kroki

## Qué es Kroki

Kroki convierte texto en **imágenes de diagramas**. El profesor escribe la sintaxis del diagrama (Mermaid, PlantUML, GraphViz, TikZ, WaveDrom, etc.) y Kroki la convierte en una imagen SVG durante la compilación del libro. La imagen se incrusta directamente, funcionando **tanto en HTML como en PDF**.

El agente NO debe pensar en Kroki como “solo Mermaid”. Kroki es una capa para generar artefactos visuales desde lenguajes intermedios. La elección correcta depende del tipo de diagrama.

## Ventajas

- ✅ Funciona en **HTML y PDF** (se renderiza como imagen SVG)
- ✅ Soporta **20+ tipos** de diagramas (Mermaid, PlantUML, GraphViz, TikZ, WaveDrom, Excalidraw, etc.)
- ✅ No requiere JavaScript ni herramientas externas instaladas
- ✅ No necesita fallbacks manuales

## Requisito

Necesita conexión a internet **durante la compilación** (no al leer el libro). GitHub Actions siempre tiene internet, así que el despliegue funciona siempre.

## Flujo recomendado para diagramas importantes: pre-render a imagen

Para diagramas importantes del libro, NO conviene depender de `kroki.io` durante cada build. La opción robusta es renderizar el diagrama previamente como imagen estática y luego insertarlo con `{figure}`.

Esto evita que una caída o timeout de Kroki rompa el build de Jupyter Book.

### Estructura recomendada

Guardar la fuente editable del diagrama en:

```text
diagram_sources/es/flujo_experimento.mermaid
diagram_sources/en/experiment_flow.mermaid
```

Renderizar con:

```bash
python scripts/extract_kroki_sources.py
python scripts/render_diagrams.py
```

El script genera imágenes en:

```text
book/_static/generated/diagrams/es/flujo_experimento.svg
book/_static/generated/diagrams/en/experiment_flow.svg
```

Después insertar la imagen generada:

````markdown
Como muestra la {numref}`fig-flujo-experimento`, el proceso va de la pregunta inicial a la conclusión.

```{figure} ../../../_static/generated/diagrams/es/flujo_experimento.svg
:name: fig-flujo-experimento
:alt: Diagrama de flujo del proceso experimental
:width: 80%
:align: center

Flujo básico del proceso experimental.
```
````

### Ventajas del pre-render

- El build HTML/PDF ya no depende de Kroki para ese diagrama.
- La figura tiene caption y referencia normal con `{numref}`.
- La fuente del diagrama sigue versionada y editable.
- Si Kroki falla, se conservan las imágenes ya generadas.

### Comandos útiles

| Comando | Uso |
|---|---|
| `python scripts/extract_kroki_sources.py --dry-run` | Detecta bloques `{kroki}` existentes sin escribir fuentes. |
| `python scripts/extract_kroki_sources.py` | Extrae bloques `{kroki}` a `diagram_sources/` y crea `manifest.json`. |
| `python scripts/render_diagrams.py --dry-run` | Lista fuentes detectadas sin llamar a Kroki. |
| `python scripts/render_diagrams.py` | Renderiza solo imágenes que aún no existen usando el endpoint oficial con `POST /<tipo>/<formato>`. |
| `python scripts/render_diagrams.py --force` | Regenera todas las imágenes. |
| `python scripts/render_diagrams.py --request-mode json` | Usa el modo JSON raíz (`POST /`) si se quiere comparar con el modo por ruta. |
| `python scripts/render_diagrams.py --max-failures 1` | Para pronto si el endpoint oficial está caído o responde con timeout. |
| `python scripts/render_diagrams.py --kroki-url http://localhost:8000/` | Usa un Kroki local si alguna vez se decide levantar uno. |

### Migración progresiva recomendada

1. Mantener temporalmente los bloques `{kroki}` existentes para no romper el libro.
2. Ejecutar `python scripts/extract_kroki_sources.py` para versionar las fuentes.
3. Ejecutar `python scripts/render_diagrams.py` cuando Kroki responda.
4. Sustituir solo los diagramas críticos por `{figure}` apuntando a los SVG generados. Para una migración automática conservadora, usar `python scripts/replace_kroki_with_figures.py --dry-run` y luego `python scripts/replace_kroki_with_figures.py`.
5. Dejar los diagramas de ejemplo simples como `{kroki}` si se acepta la dependencia externa.

## Decisión rápida: qué lenguaje usar

| Necesidad docente | Opción recomendada | Por qué |
|---|---|---|
| Diagrama de flujo, mapa conceptual, proceso simple | **Mermaid** (`:type: mermaid`) | Sintaxis simple, ideal para contenido general. |
| Informática: ER, clases, secuencia, estados, Gantt | **Mermaid** o **PlantUML** | Mermaid para casos sencillos; PlantUML si el UML es más formal/complejo. |
| Arquitectura software/C4 | **Structurizr** o **PlantUML C4** | Mejor semántica arquitectónica que un flowchart genérico. |
| Grafos matemáticos o redes | **GraphViz** (`:type: graphviz`) | Control claro de nodos/aristas y layout. |
| Electrónica/Física: circuitos docentes bonitos | **CircuitikZ local renderizado a imagen** | CircuitikZ es LaTeX/TikZ especializado, pero el servicio público de Kroki/TikZ no garantiza tener `circuitikz` disponible. Usar la skill `teachbook-generate-circuitikz`. |
| Señales digitales, buses, cronogramas, protocolos | **WaveDrom** (`:type: wavedrom`) | Diseñado específicamente para timing diagrams. |
| Diagramas de bloques electrónicos | **Mermaid**, **D2** o **GraphViz** | Mejor para arquitectura de sistema que para esquemas de componentes. |
| Campos de bits / paquetes / protocolos | **Bytefield** o **PacketDiag** | Más preciso que dibujarlo como cajas genéricas. |
| Visualización de datos declarativa | **Vega/Vega-Lite** | Gráficos desde JSON declarativo. |

```{admonition} Regla para circuitos
:class: important
Para circuitos eléctricos/electrónicos docentes, NO usar Mermaid como primera opción. Usar **CircuitikZ renderizado localmente a imagen** mediante `teachbook-generate-circuitikz`. Mermaid sirve para bloques, no para esquemas eléctricos con símbolos normalizados.
```

### Cuándo NO usar esta skill

- **Circuitos docentes con símbolos normalizados**: usar la skill `teachbook-generate-circuitikz`, que renderiza CircuitikZ localmente a PNG mediante el pipeline LaTeX del proyecto.
- **Circuitos electrónicos reales / netlists / KiCad**: usar un flujo avanzado tipo **SKiDL → netlist KiCad → KiCad CLI/export → SVG/PNG/PDF**. Esto es diseño electrónico real, no solo diagrama docente.
- **Animaciones**: Kroki no es una herramienta de vídeo; usar un `.mp4` generado externamente e insertarlo como vídeo local con fallback PDF.

## Sintaxis MyST

### Mermaid (recomendado — el más sencillo)

````markdown
```{kroki}
:type: mermaid
:align: center

flowchart LR
    A[Inicio] --> B[Proceso]
    B --> C[Fin]
```
````

### Con título (caption)

````markdown
El diagrama siguiente resume el flujo del método científico.

**Diagrama. Flujo del método científico.**

```{kroki}
:type: mermaid
:align: center

graph TD
    A[Observación] --> B[Hipótesis]
    B --> C[Experimentación]
    C --> D{¿Resultados válidos?}
    D -->|Sí| E[Conclusión]
    D -->|No| B
```
````

### Otros tipos de diagrama soportados

````markdown
```{kroki}
:type: plantuml
:align: center

@startuml
Alice -> Bob: Hello
Bob --> Alice: Hi!
@enduml
```
````

### Circuitos docentes: CircuitikZ NO va por Kroki público

Kroki soporta `:type: tikz`, pero eso no implica que el servicio público tenga cargado el paquete LaTeX `circuitikz`. En pruebas directas, `\begin{circuitikz}` puede fallar con `Environment circuitikz undefined`.

Para circuitos, usar el flujo local de la skill `teachbook-generate-circuitikz`:

````markdown
```{figure} _static/generated/circuito_rc_circuitikz.png
:alt: Circuito RC generado con CircuitikZ
:width: 70%
:align: center

Circuito RC generado desde código CircuitikZ y renderizado como imagen.
```
````

Notas para el agente:

- Mantener los circuitos CircuitikZ **pequeños y docentes**.
- Etiquetar magnitudes con unidades LaTeX legibles: `$5\,\mathrm{V}$`, `$20\,\mu\mathrm{F}$`.
- No prometer CircuitikZ vía Kroki público salvo que se haya verificado en ese entorno concreto.

### Señales digitales con WaveDrom

Usar WaveDrom para cronogramas, buses, señales digitales y protocolos.

````markdown
El diagrama siguiente muestra un cronograma digital de reloj, datos y señal de validez.

**Diagrama. Cronograma digital de una señal de reloj y datos.**

```{kroki}
:type: wavedrom
:align: center

{ signal: [
  { name: "clk",  wave: "p.....|..." },
  { name: "data", wave: "x.345x|=.x", data: ["A", "B", "C", "D"] },
  { name: "valid", wave: "0.1..0|1.0" }
]}
```
````

````markdown
```{kroki}
:type: graphviz
:align: center

digraph G {
    A -> B -> C;
    A -> C;
}
```
````

````markdown
```{kroki}
:type: excalidraw
:align: center

{"type":"excalidraw","version":2,"elements":[...]}
```
````

## Plantillas por tipo de diagrama (Mermaid)

### Flowchart (diagrama de flujo)

````markdown
```{kroki}
:type: mermaid
:align: center

graph TD
    A[Observación] --> B[Hipótesis]
    B --> C[Experimentación]
    C --> D{¿Resultados válidos?}
    D -->|Sí| E[Conclusión]
    D -->|No| B
```
````

Direcciones: `graph TD` (arriba→abajo), `graph LR` (izquierda→derecha), `flowchart TD`, `flowchart LR`.

### Diagrama ER (entidad-relación)

````markdown
```{kroki}
:type: mermaid
:align: center

erDiagram
    EXPERIMENTO ||--o{ MEDICION : tiene
    EXPERIMENTO {
        string nombre
        date fecha
        string responsable
    }
    MEDICION {
        float valor
        string unidad
        datetime timestamp
    }
```
````

### Diagrama de clases (UML)

````markdown
```{kroki}
:type: mermaid
:align: center

classDiagram
    class Organismo {
        +String nombre
        +String reino
        +clasificar()
    }
    class Animal {
        +String habitat
        +moverse()
    }
    Organismo <|-- Animal
```
````

### Diagrama de secuencia

````markdown
```{kroki}
:type: mermaid
:align: center

sequenceDiagram
    participant E as Estudiante
    participant L as Laboratorio
    participant P as Profesor
    E->>L: Enviar muestra
    L->>L: Analizar muestra
    L-->>P: Enviar resultados
    P-->>E: Devolver informe
```
````

### Diagrama de estados

````markdown
```{kroki}
:type: mermaid
:align: center

stateDiagram-v2
    [*] --> Liquido
    Liquido --> Gas : Evaporación
    Gas --> Liquido : Condensación
    Liquido --> Solido : Congelación
    Solido --> Liquido : Fusión
```
````

### Diagrama de Gantt

````markdown
```{kroki}
:type: mermaid
:align: center

gantt
    title Cronograma del experimento
    dateFormat  YYYY-MM-DD
    section Preparación
    Diseño experimental   :a1, 2025-01-01, 7d
    Recopilar material    :a2, after a1, 3d
    section Ejecución
    Realizar mediciones   :a3, after a2, 14d
```
````

## Tipos de diagrama soportados por Kroki

| Tipo | `:type:` | Descripción |
|---|---|---|
| Mermaid | `mermaid` | El más versátil. Flowcharts, ER, UML, secuencias, Gantt... |
| PlantUML | `plantuml` | Diagramas UML completos. Sintaxis `@startuml` / `@enduml`. |
| GraphViz | `graphviz` | Diagramas de nodos y aristas. Usa sintaxis DOT. |
| Excalidraw | `excalidraw` | Diagramas dibujados a mano (estilo pizarra). JSON. |
| TikZ | `tikz` | Diagramas LaTeX/TikZ simples. Para CircuitikZ, preferir render local con `teachbook-generate-circuitikz`. |
| Bytefield | `bytefield` | Diagramas de campos de bits (electrónica/protocolos). |
| BlockDiag | `blockdiag` | Diagramas de bloques simples. |
| SeqDiaq | `seqdiag` | Diagramas de secuencia (alternativa simple). |
| ActDiag | `actdiag` | Diagramas de actividad. |
| NwDiag | `nwdiag` | Diagramas de red. |
| PacketDiag | `packetdiag` | Diagramas de paquetes de red. |
| RackDiag | `rackdiag` | Diagramas de rack de servidores. |
| Vega / Vega-Lite | `vega` / `vegalite` | Gráficos y visualizaciones de datos. JSON. |
| Ditaa | `ditaa` | Diagramas ASCII convertidos a imágenes. |
| Erd | `erd` | Diagramas entidad-relación (sintaxis propia). |
| Nomnoml | `nomnoml` | Diagramas de clases UML minimalistas. |
| SvgBob | `svgbob` | Diagramas ASCII convertidos a SVG. |
| Umlet | `umlet` | Diagramas UML. |
| WaveDrom | `wavedrom` | Diagramas de formas de onda digitales, buses, timing y protocolos. |
| Pikchr | `pikchr` | Diagramas técnicos (tipo PIC). |
| Structurizr | `structurizr` | Diagramas C4 (arquitectura software). |

## Reglas

| Regla | Detalle |
|---|---|
| Tipo por defecto | Usar **Mermaid** (`:type: mermaid`) salvo que el usuario pida otro. |
| Circuitos docentes | Usar **CircuitikZ local renderizado a imagen** para circuitos de Física/Electrónica. No asumir que Kroki público carga `circuitikz`. |
| Señales digitales | Usar **WaveDrom** (`:type: wavedrom`) para cronogramas, buses y timing. |
| Circuitos reales | No usar Kroki como diseño electrónico real. Recomendar SKiDL/KiCad para netlists y KiCad CLI/export para render final. |
| Simplicidad | Máximo **10-15 nodos**. Si necesitas más, divide en varios diagramas. |
| Etiquetas | Usar **español** para los textos (salvo que el contenido sea en inglés). |
| Caption | Añadir siempre una frase de referencia y un título textual antes del bloque `{kroki}`. Para diagramas importantes, preferir pre-render + `{figure}` con caption. |
| Alineación | Usar `:align: center` por defecto. |
| HTML y PDF | Los diagramas **funcionan en ambos formatos**. No necesita fallbacks. |
| Validación | Verificar la sintaxis antes de insertar. Un error de sintaxis rompe la página. |
| Sin `{mermaid}` | **NO** usar la directiva `{mermaid}` (requiere sphinxcontrib-mermaid, no funciona en PDF). Usar siempre `{kroki}` con `:type: mermaid`. |

## Flujo de trabajo

1. Preguntar qué tipo de diagrama necesita el usuario y qué concepto quiere representar.
2. Elegir el tipo adecuado: Mermaid por defecto; PlantUML para UML complejo; GraphViz para grafos; CircuitikZ local para circuitos docentes; WaveDrom para señales digitales.
3. Generar el código del diagrama usando la plantilla correspondiente.
4. Para diagramas rápidos, insertar en el archivo `.md` usando `{kroki}` con `:type: <tipo>` y título textual cercano.
5. Para diagramas importantes o estables, guardar la fuente en `diagram_sources/`, ejecutar `python scripts/render_diagrams.py` e insertar el SVG generado con `{figure}`.
