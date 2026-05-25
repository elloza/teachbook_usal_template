(mermaid)=
# Diagrams with Kroki (Mermaid)

**Kroki** converts text into SVG diagrams during the book build. If you use `:type: mermaid`, you can write Mermaid syntax and get a diagram that works in both **HTML** and **PDF**.

## Flowchart (`flowchart`)

````md
```{kroki}
:type: mermaid
:align: center

%%{init: {"themeVariables": {"fontSize": "12px", "fontFamily": "Arial"}}}%%
flowchart LR
    A[Sample] --> B[Preparation]
    B --> C[Measurement]
    C --> D[Analysis]
    D --> E[Results]
```
````

Result:


As shown in {numref}`fig-diagram-05-basic-content-mermaid-01`, the diagram is versioned as a static image.

```{figure} ../../_static/generated/diagrams/en/05_basic_content_mermaid_01.svg
:name: fig-diagram-05-basic-content-mermaid-01
:alt: Diagram: Flowchart (`flowchart`)
:width: 75%
:align: center

Diagram: Flowchart (`flowchart`).
```

````md
```{kroki}
:type: mermaid
:align: center

%%{init: {"themeVariables": {"fontSize": "12px", "fontFamily": "Arial"}}}%%
sequenceDiagram
    participant S as Student
    participant T as Teacher
    participant L as Laboratory
    S->>T: Submit report
    T->>S: Corrections
    S->>L: Book equipment
    L->>S: Confirmation
```
````

Result:


As shown in {numref}`fig-diagram-05-basic-content-mermaid-02`, the diagram is versioned as a static image.

```{figure} ../../_static/generated/diagrams/en/05_basic_content_mermaid_02.svg
:name: fig-diagram-05-basic-content-mermaid-02
:alt: Diagram: Sequence diagram (`sequenceDiagram`)
:width: 80%
:align: center

Diagram: Sequence diagram (`sequenceDiagram`).
```

````md
```{kroki}
:type: mermaid
:align: center

%%{init: {"themeVariables": {"fontSize": "11px", "fontFamily": "Arial"}}}%%
classDiagram
    direction LR
    class Experiment {
        +name
        +run()
    }
    class Sample {
        +type
        +prepare()
    }
    Experiment --> Sample : uses
```
````

Result:


As shown in {numref}`fig-diagram-05-basic-content-mermaid-03`, the diagram is versioned as a static image.

```{figure} ../../_static/generated/diagrams/en/05_basic_content_mermaid_03.svg
:name: fig-diagram-05-basic-content-mermaid-03
:alt: Diagram: Class diagram (`classDiagram`)
:width: 45%
:align: center

Diagram: Class diagram (`classDiagram`).
```

````md
```{kroki}
:type: mermaid
:align: center

%%{init: {"themeVariables": {"fontSize": "11px", "fontFamily": "Arial"}}}%%
erDiagram
    STUDENT ||--o{ ENROLLMENT : makes
```
````

Result:


As shown in {numref}`fig-diagram-05-basic-content-mermaid-04`, the diagram is versioned as a static image.

```{figure} ../../_static/generated/diagrams/en/05_basic_content_mermaid_04.svg
:name: fig-diagram-05-basic-content-mermaid-04
:alt: Diagram: Entity-relationship diagram (`erDiagram`)
:width: 38%
:align: center

Diagram: Entity-relationship diagram (`erDiagram`).
```

````md
```{kroki}
:type: mermaid
:align: center

%%{init: {"themeVariables": {"fontSize": "11px", "fontFamily": "Arial"}}}%%
stateDiagram-v2
    direction LR
    [*] --> Pending
    Pending --> InProgress : start
    InProgress --> Completed : finish
    InProgress --> Error : failure
    Error --> Pending : retry
    Completed --> [*]
```
````

Result:


As shown in {numref}`fig-diagram-05-basic-content-mermaid-05`, the diagram is versioned as a static image.

```{figure} ../../_static/generated/diagrams/en/05_basic_content_mermaid_05.svg
:name: fig-diagram-05-basic-content-mermaid-05
:alt: Diagram: State diagram (`stateDiagram-v2`)
:width: 50%
:align: center

Diagram: State diagram (`stateDiagram-v2`).
```
The following table summarizes the main elements of this section.

**Table. Flowchart directions.**

| Code | Direction |
|------|-----------|
| `flowchart LR` | Left to right |
| `flowchart RL` | Right to left |
| `flowchart TB` | Top to bottom |
| `flowchart BT` | Bottom to top |

```{tip}
Always use `{kroki}` with `:type: mermaid` instead of `{mermaid}`. This makes the diagram work in both HTML and PDF without manual fallbacks.
```
