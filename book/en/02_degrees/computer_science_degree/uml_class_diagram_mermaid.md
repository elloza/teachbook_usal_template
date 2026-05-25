# UML Class Diagram with Kroki (Mermaid)

Class diagrams are essential for modeling object-oriented systems.
With Kroki and `:type: mermaid`, you can represent classes, attributes, methods, and inheritance in both HTML and PDF.

## Example: Geometric Shape Hierarchy

**Code:**

````md
```{kroki}
:type: mermaid
:align: center

classDiagram
    class Shape {
        <<abstract>>
        +String color
        +area() float
        +perimeter() float
    }

    class Circle {
        +float radius
        +area() float
        +perimeter() float
    }

    class Rectangle {
        +float width
        +float height
        +area() float
        +perimeter() float
    }

    class Triangle {
        +float base
        +float height
        +area() float
        +perimeter() float
    }

    Shape <|-- Circle
    Shape <|-- Rectangle
    Shape <|-- Triangle
```
````

**Result:**


As shown in {numref}`fig-diagram-02-degrees-computer-science-degree-uml-class-diagram-mermaid-01`, the diagram is versioned as a static image.

```{figure} ../../../_static/generated/diagrams/en/02_degrees_computer_science_degree_uml_class_diagram_mermaid_01.svg
:name: fig-diagram-02-degrees-computer-science-degree-uml-class-diagram-mermaid-01
:alt: Diagram: Example: Geometric Shape Hierarchy
:width: 90%
:align: center

Diagram: Example: Geometric Shape Hierarchy.
```
- **Methods**: Listed in the second section, with return type.
- **Abstract class**: Indicated with `<<abstract>>`.

## Relationship types


The following table summarizes the main elements of this section.

**Table. Relationship types.**

| Notation | Meaning |
|----------|---------|
| `<\|--` | Inheritance (is a) |
| `*--` | Composition |
| `o--` | Aggregation |
| `-->` | Association |
| `..>` | Dependency |
