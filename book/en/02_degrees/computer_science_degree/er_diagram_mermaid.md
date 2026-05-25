# Entity-Relationship Diagram with Kroki (Mermaid)

E-R diagrams are fundamental in database design.
With Kroki and `:type: mermaid`, you can include them directly in your book and make them work in both HTML and PDF.

## Example: University database

**Code:**

````md
```{kroki}
:type: mermaid
:align: center

erDiagram
    STUDENT {
        int id PK
        string name
        string email
    }
    COURSE {
        int id PK
        string name
        int credits
    }
    PROFESSOR {
        int id PK
        string name
        string department
    }
    ENROLLMENT {
        int id PK
        float grade
        string term
    }

    STUDENT ||--o{ ENROLLMENT : "enrolls in"
    COURSE ||--o{ ENROLLMENT : "has"
    PROFESSOR ||--o{ COURSE : "teaches"
```
````

**Result:**


As shown in {numref}`fig-diagram-02-degrees-computer-science-degree-er-diagram-mermaid-01`, the diagram is versioned as a static image.

```{figure} ../../../_static/generated/diagrams/en/02_degrees_computer_science_degree_er_diagram_mermaid_01.svg
:name: fig-diagram-02-degrees-computer-science-degree-er-diagram-mermaid-01
:alt: Diagram: Example: University database
:width: 90%
:align: center

Diagram: Example: University database.
```
- **Relationship types**: Use `||--o{` (one-to-many), `||--||` (one-to-one), `}o--o{` (many-to-many).
- **Primary keys**: Mark attributes with `PK`.
- **Foreign keys**: Mark attributes with `FK`.

## Cardinality reference


The following table summarizes the main elements of this section.

**Table. Cardinality reference.**

| Notation | Meaning |
|----------|---------|
| `||--||` | One to one |
| `||--o{` | One to many |
| `}o--o{` | Many to many |
