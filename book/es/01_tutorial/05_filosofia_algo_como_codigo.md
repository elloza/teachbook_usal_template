# 5. La Filosofía del "X como código"

Una de las ideas importantes que queremos que os llevéis de este curso es la posibilidad de editar y generar artefactos docentes a través de lenguajes de programación y lenguajes de marcado. Esto es lo que llamamos la filosofía del "X como código" o "X as code". Se trata de usar el código como un medio para describir y generar recursos educativos de forma que nos beneficiemos de que los LLMs pueden entender y manipular ese código para ayudarnos a crear materiales de calidad sin necesidad de editar cada artefacto de forma manual.

## ¿Qué es "X como código"?

Cuando hablamos de "X como código", nos referimos a la idea de que un recurso educativo (X) puede ser descrito y generado a través de un lenguaje de programación o un lenguaje de marcado. En lugar de crear un diagrama, una gráfica, una animación o un cuestionario directamente en una herramienta visual, lo describimos con código. Luego, ese código se compila o se ejecuta para generar el artefacto final.

La idea es usar lenguajes de programación y lenguajes de marcado como **lenguajes intermedios** para generar artefactos docentes: imágenes, diagramas, animaciones, vídeos, simulaciones, cuestionarios, tablas, notebooks y PDFs.

Dicho de otra forma: trabajar con **X as code**.

- *Diagrams as code*: diagramas escritos como texto.
- *Figures as code*: gráficas y figuras generadas desde datos o fórmulas.
- *Animations as code*: vídeos educativos renderizados desde una escena programada.
- *Quizzes as code*: preguntas, soluciones y bancos de ejercicios definidos en texto estructurado.
- *Books as code*: un libro completo compilado desde archivos Markdown, notebooks y configuración.

```{admonition} Idea clave
Un artefacto docente generado desde código no se edita “a mano” al final del proceso. Se describe con un lenguaje intermedio, en el que los asistentes de IA pueden entender la estructura y el contenido, y luego se genera el resultado final a través de un proceso de compilación o ejecución.
```

## ¿Por qué es interesante esta filosofía?

Uno de los problemas de generar contenidos con herramientas de IA es que el resultado final suele ser una imagen, un PDF o un vídeo que no se puede editar fácilmente. Si quieres cambiar algo, tienes que volver a generar el artefacto desde cero o editarlo manualmente, lo que puede ser complicado y llevar mucho tiempo.

Al final, esa ventaja que ofrece la IA para generar contenido de forma rápida se pierde si el resultado no es editable. En cambio, si el artefacto se genera desde código, puedes pedirle a la IA que edite ese código para hacer cambios, generar nuevas versiones o adaptar el contenido a diferentes contextos.

Tener este lenguaje intermedio en ocasiones es clave para que la IA pueda ayudarte a generar contenido de calidad. Por ejemplo, si quieres generar un diagrama de flujo, puedes describirlo con código Mermaid o Kroki. La IA puede entender esa descripción y ayudarte a modificarla, traducirla o adaptarla sin necesidad de editar la imagen final.

## El código como puente hacia el resultado final

Cuando dibujas un diagrama directamente en una herramienta visual, el resultado queda encerrado en esa interfaz. Si quieres cambiar diez flechas, traducir etiquetas o adaptar el estilo, tienes que volver a editar manualmente.

Cuando describes ese mismo diagrama con código, aparece una capa intermedia:

Como muestra la {numref}`fig-diagrama-01-tutorial-05-filosofia-codigo-docente-01`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/01_tutorial_05_filosofia_codigo_docente_01.svg
:name: fig-diagrama-01-tutorial-05-filosofia-codigo-docente-01
:alt: Diagrama: El código como puente hacia el resultado final
:width: 90%
:align: center

Diagrama: El código como puente hacia el resultado final.
```

La tabla siguiente resume los elementos principales de esta sección.

**Tabla. ¿Qué artefactos pueden generarse desde código?.**

| Artefacto final | Lenguaje intermedio | Ejemplo de uso docente |
|---|---|---|
| Diagrama | Mermaid/Kroki, GraphViz, PlantUML | Mapa conceptual, flujo de un experimento, esquema de un proceso |
| Gráfica científica | Python + matplotlib | Representar datos reales o simulados |
| Circuito eléctrico | Schemdraw o CircuitikZ | Generar esquemas consistentes para problemas de Física |
| Animación o vídeo | Herramienta externa + MP4 | Explicar una transformación, una onda o una demostración paso a paso sin cargar la instalación base |
| Tabla o dataset | Python + pandas | Crear tablas limpias desde datos brutos |
| Cuestionario | MyST, JupyterQuiz, Markdown estructurado | Preguntas de repaso con soluciones desplegables |
| Notebook ejecutable | Jupyter Notebook | Simulación, cálculo reproducible, práctica guiada |
| Libro web y PDF | Jupyter Book/TeachBooks | Publicar el mismo material en web, descarga y versión imprimible |

## Por qué esto encaja tan bien con IA

La IA no “entiende” una imagen final como entiende una descripción en código. Si le das una captura de un diagrama, puede sugerir cambios; si le das el código Mermaid o Kroki que lo genera, puede **hacer** esos cambios.

```{admonition} La ventaja práctica
:class: tip
No le pedimos a la IA que edite píxeles. Le pedimos que edite instrucciones. Después, el sistema recompila esas instrucciones y produce el artefacto final.
```

Esto permite pedir cosas como:

- “Convierte este diagrama de flujo en un diagrama de estados”.
- “Genera una versión en inglés manteniendo la misma estructura”.
- “Cambia el ejemplo para que use datos de Biología en vez de Física”.
- “Prepara el guion visual de una animación de 20 segundos que muestre esta función creciendo”.
- “Crea tres variantes del cuestionario con distinta dificultad”.

La clave es que el resultado final no se fabrica de forma artesanal cada vez. Se fabrica desde una receta editable.

## Reproducibilidad, no solo automatización

Trabajar “as code” no significa hacer las cosas más complicadas. Significa que cada artefacto tiene una receta clara:

1. **Entrada**: datos, fórmulas, texto o una idea docente.
2. **Lenguaje intermedio**: Markdown, Python, Mermaid, LaTeX, etc.
3. **Compilación**: el sistema transforma esa descripción.
4. **Salida**: imagen, vídeo, web, PDF, notebook o cuestionario.

Si cambias la receta, regeneras el artefacto. Si algo falla, corriges la receta. Si otro profesor quiere adaptarlo, no empieza desde cero: modifica la receta.

## El cambio de mentalidad

La pregunta deja de ser: “¿con qué programa dibujo esto?”

La pregunta pasa a ser: “¿qué lenguaje intermedio describe mejor este artefacto?”

No todos los materiales necesitan código. Pero cuando un recurso se va a revisar, traducir, versionar, reutilizar o generar con ayuda de IA, conviene preguntarse si puede expresarse como **X as code**.

Esa es la filosofía del código docente: usar el código no como fin, sino como **medio generativo** entre la intención didáctica y el artefacto final.
