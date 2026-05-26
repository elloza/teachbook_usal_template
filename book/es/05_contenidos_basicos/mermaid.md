(mermaid)=
# Diagramas con Kroki (Mermaid)

**Kroki** permite convertir texto en diagramas SVG durante la compilación del libro. Si usas `:type: mermaid`, puedes escribir sintaxis Mermaid y obtener un diagrama que funciona tanto en **HTML** como en **PDF**.

## Cómo se genera la imagen en este proyecto

En un archivo `.md`, el punto de partida puede ser un bloque de texto como este:

````md
```{kroki}
:type: mermaid
:align: center

flowchart LR
    A[Muestra] --> B[Preparación]
    B --> C[Medición]
    C --> D[Resultados]
```
````

Ese bloque no es una imagen todavía: es la **fuente editable** del diagrama. En este proyecto, cuando se trabaja con las skills de diagramas y compilación, el agente prepara el contenido siguiendo un flujo más robusto que dejar el bloque `{kroki}` directamente en la página final:

1. Guarda la fuente editable en `diagram_sources/`.
2. Genera una imagen SVG en `book/_static/generated/diagrams/`.
3. Para Mermaid, genera además un PNG de respaldo en `book/_static/generated/diagrams_pdf/` para la exportación PDF.
4. Sustituye el bloque `{kroki}` por una figura MyST normal que apunta a la imagen generada.

El resultado final que queda en el libro se parece a esto:

````md
```{figure} ../../_static/generated/diagrams/es/mi_diagrama.svg
:name: fig-mi-diagrama
:alt: Diagrama generado desde Mermaid
:width: 75%
:align: center

Diagrama generado desde código Mermaid.
```
````

```{important}
Jupyter Book por sí solo no hace esta sustitución automática. La conversión a imagen estática forma parte del flujo de las skills del proyecto: `teachbook-generate-diagram` prepara y renderiza el diagrama, y `teachbook-build` compila después el libro usando esas imágenes ya generadas.
```

## Diagrama de flujo (`flowchart`)

````md
```{kroki}
:type: mermaid
:align: center

%%{init: {"themeVariables": {"fontSize": "12px", "fontFamily": "Arial"}}}%%
flowchart LR
    A[Muestra] --> B[Preparación]
    B --> C[Medición]
    C --> D[Análisis]
    D --> E[Resultados]
```
````

Resultado:


Como muestra la {numref}`fig-diagrama-05-contenidos-basicos-mermaid-01`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/05_contenidos_basicos_mermaid_01.svg
:name: fig-diagrama-05-contenidos-basicos-mermaid-01
:alt: Diagrama: Diagrama de flujo (`flowchart`)
:width: 75%
:align: center

Diagrama: Diagrama de flujo (`flowchart`).
```

````md
```{kroki}
:type: mermaid
:align: center

%%{init: {"themeVariables": {"fontSize": "12px", "fontFamily": "Arial"}}}%%
sequenceDiagram
    participant E as Estudiante
    participant P as Profesor
    participant L as Laboratorio
    E->>P: Entrega informe
    P->>E: Correcciones
    E->>L: Reserva equipo
    L->>E: Confirmación
```
````

Resultado:


Como muestra la {numref}`fig-diagrama-05-contenidos-basicos-mermaid-02`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/05_contenidos_basicos_mermaid_02.svg
:name: fig-diagrama-05-contenidos-basicos-mermaid-02
:alt: Diagrama: Diagrama de secuencia (`sequenceDiagram`)
:width: 80%
:align: center

Diagrama: Diagrama de secuencia (`sequenceDiagram`).
```

````md
```{kroki}
:type: mermaid
:align: center

%%{init: {"themeVariables": {"fontSize": "11px", "fontFamily": "Arial"}}}%%
classDiagram
    direction LR
    class Experimento {
        +nombre
        +ejecutar()
    }
    class Muestra {
        +tipo
        +preparar()
    }
    Experimento --> Muestra : usa
```
````

Resultado:


Como muestra la {numref}`fig-diagrama-05-contenidos-basicos-mermaid-03`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/05_contenidos_basicos_mermaid_03.svg
:name: fig-diagrama-05-contenidos-basicos-mermaid-03
:alt: Diagrama: Diagrama de clases (`classDiagram`)
:width: 45%
:align: center

Diagrama: Diagrama de clases (`classDiagram`).
```

````md
```{kroki}
:type: mermaid
:align: center

%%{init: {"themeVariables": {"fontSize": "11px", "fontFamily": "Arial"}}}%%
erDiagram
    ALUMNO ||--o{ MATRICULA : hace
```
````

Resultado:


Como muestra la {numref}`fig-diagrama-05-contenidos-basicos-mermaid-04`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/05_contenidos_basicos_mermaid_04.svg
:name: fig-diagrama-05-contenidos-basicos-mermaid-04
:alt: Diagrama: Diagrama entidad-relación (`erDiagram`)
:width: 38%
:align: center

Diagrama: Diagrama entidad-relación (`erDiagram`).
```

````md
```{kroki}
:type: mermaid
:align: center

%%{init: {"themeVariables": {"fontSize": "11px", "fontFamily": "Arial"}}}%%
stateDiagram-v2
    direction LR
    [*] --> Pendiente
    Pendiente --> EnProgreso : iniciar
    EnProgreso --> Completado : finalizar
    EnProgreso --> Error : fallo
    Error --> Pendiente : reintentar
    Completado --> [*]
```
````

Resultado:


Como muestra la {numref}`fig-diagrama-05-contenidos-basicos-mermaid-05`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/05_contenidos_basicos_mermaid_05.svg
:name: fig-diagrama-05-contenidos-basicos-mermaid-05
:alt: Diagrama: Diagrama de estados (`stateDiagram-v2`)
:width: 50%
:align: center

Diagrama: Diagrama de estados (`stateDiagram-v2`).
```
La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Direcciones del diagrama de flujo.**

| Código | Dirección |
|--------|-----------|
| `flowchart LR` | Izquierda a derecha |
| `flowchart RL` | Derecha a izquierda |
| `flowchart TB` | Arriba a abajo |
| `flowchart BT` | Abajo a arriba |

```{tip}
Usa siempre `{kroki}` con `:type: mermaid` en lugar de `{mermaid}`. Así el diagrama funcionará en HTML y PDF sin fallbacks manuales.
```
