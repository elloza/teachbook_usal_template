# Diagramas Técnicos con Kroki para Física

Kroki es útil para representar **diagramas de bloques, flujo de señales, cronogramas y esquemas conceptuales**. Para **circuitos eléctricos con símbolos normalizados**, la herramienta recomendada es **CircuitikZ renderizado como imagen**.

## Cuándo usar cada herramienta

- **Usa Kroki** para explicaciones conceptuales, bloques funcionales, temporización, instrumentación y flujo de señal.
- **Usa WaveDrom vía Kroki** para señales digitales, buses, relojes y protocolos temporales.
- **Usa CircuitikZ** para resistencias, condensadores, fuentes, interruptores y esquemas eléctricos formales.
- **Usa SchemDraw** cuando quieras construir circuitos sencillos desde Python dentro de un notebook.

## 1. Mermaid: cadena de instrumentación


Como muestra la {numref}`fig-diagrama-02-grados-grado-fisica-diagramas-kroki-01`, el diagrama queda versionado como imagen estática.

```{figure} ../../../_static/generated/diagrams/es/02_grados_grado_fisica_diagramas_kroki_01.svg
:name: fig-diagrama-02-grados-grado-fisica-diagramas-kroki-01
:alt: Diagrama: Mermaid: cadena de instrumentación
:width: 90%
:align: center

Diagrama: Mermaid: cadena de instrumentación.
```
Como muestra la {numref}`fig-diagrama-02-grados-grado-fisica-diagramas-kroki-02`, el diagrama queda versionado como imagen estática.

```{figure} ../../../_static/generated/diagrams/es/02_grados_grado_fisica_diagramas_kroki_02.svg
:name: fig-diagrama-02-grados-grado-fisica-diagramas-kroki-02
:alt: Diagrama: GraphViz: flujo de señal en un montaje
:width: 90%
:align: center

Diagrama: GraphViz: flujo de señal en un montaje.
```


El {numref}`fig-diagramas-kroki-3` resume visualmente esta parte de la explicación.

```{figure} ../../../_static/generated/circuito_rc_circuitikz.png
:alt: Circuito RC generado con CircuitikZ
:width: 70%
:align: center
:name: fig-diagramas-kroki-3

Circuito RC generado desde código CircuitikZ.
```

```tex
\begin{circuitikz}
\draw
  (0,0) to[V, l=$5\,\mathrm{V}$] (0,3)
  to[R, l=$R_1$] (3,3)
  to[C, l=$20\,\mu\mathrm{F}$] (3,0)
  -- (0,0);
\end{circuitikz}
```

```{admonition} Importante
:class: warning
Kroki soporta TikZ, pero el servicio público de Kroki no garantiza tener disponible el paquete `circuitikz`. Para circuitos docentes robustos, en este proyecto se renderiza CircuitikZ localmente a imagen.
```

## 4. Wavedrom: señales de entrada y salida


Como muestra la {numref}`fig-diagrama-02-grados-grado-fisica-diagramas-kroki-03`, el diagrama queda versionado como imagen estática.

```{figure} ../../../_static/generated/diagrams/es/02_grados_grado_fisica_diagramas_kroki_03.svg
:name: fig-diagrama-02-grados-grado-fisica-diagramas-kroki-03
:alt: Diagrama: Wavedrom: señales de entrada y salida
:width: 90%
:align: center

Diagrama: Wavedrom: señales de entrada y salida.
```
Como muestra la {numref}`fig-diagrama-02-grados-grado-fisica-diagramas-kroki-04`, el diagrama queda versionado como imagen estática.

```{figure} ../../../_static/generated/diagrams/es/02_grados_grado_fisica_diagramas_kroki_04.svg
:name: fig-diagrama-02-grados-grado-fisica-diagramas-kroki-04
:alt: Diagrama: Ditaa: esquema rápido de banco experimental
:width: 90%
:align: center

Diagrama: Ditaa: esquema rápido de banco experimental.
```

- **Kroki** = explicación visual del sistema, bloques, flujos y cronogramas.
- **CircuitikZ** = circuito formal con símbolos normalizados y acabado LaTeX.
- **SchemDraw** = circuito programable desde Python, ideal para notebooks docentes.
