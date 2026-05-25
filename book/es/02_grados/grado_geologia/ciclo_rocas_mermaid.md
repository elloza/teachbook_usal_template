# Ciclo de las Rocas con Kroki (Mermaid)

El ciclo de las rocas describe las transformaciones entre los tres tipos principales de rocas.
Con Kroki y `:type: mermaid` podemos representar este ciclo como un diagrama de flujo compatible con HTML y PDF.

## El ciclo

**Código:**

````md
```{kroki}
:type: mermaid
:align: center

flowchart LR
    Magma["Magma"]
    Ignea["Roca Ígnea"]
    Sedimentaria["Roca Sedimentaria"]
    Metamorfica["Roca Metamórfica"]

    Magma -->|"Enfriamiento y solidificación"| Ignea
    Ignea -->|"Meteorización y erosión"| Sedimentaria
    Sedimentaria -->|"Calor y presión"| Metamorfica
    Metamorfica -->|"Fusión"| Magma
    Ignea -->|"Calor y presión"| Metamorfica
    Metamorfica -->|"Meteorización y erosión"| Sedimentaria
    Sedimentaria -->|"Fusión"| Magma
```
````

**Resultado:**


Como muestra la {numref}`fig-diagrama-02-grados-grado-geologia-ciclo-rocas-mermaid-01`, el diagrama queda versionado como imagen estática.

```{figure} ../../../_static/generated/diagrams/es/02_grados_grado_geologia_ciclo_rocas_mermaid_01.svg
:name: fig-diagrama-02-grados-grado-geologia-ciclo-rocas-mermaid-01
:alt: Diagrama: El ciclo
:width: 90%
:align: center

Diagrama: El ciclo.
```
La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Explicación de las transiciones.**

| Transición | Proceso geológico |
|------------|-------------------|
| Magma → Roca Ígnea | Enfriamiento y solidificación del magma en superficie o en profundidad |
| Roca Ígnea → Sedimentaria | Meteorización, erosión, transporte y sedimentación |
| Sedimentaria → Metamórfica | Calor y presión (metamorfismo) sin llegar a fundir |
| Metamórfica → Magma | Fusión completa por temperaturas extremas |
| Ígnea → Metamórfica | Metamorfismo directo por calor y presión |
| Metamórfica → Sedimentaria | Exhumación, meteorización y erosión |

## Punto clave

Cualquier tipo de roca puede transformarse en cualquier otro. No es un ciclo lineal, sino una **red de transformaciones** que opera a escalas de tiempo geológicas (millones de años).
