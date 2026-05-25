# 3. Edición con IA

Este curso está enfocado para personas de cualquier nivel de experiencia de programación. La posibilidad que se ha abierto con los asistentes de IA es enorme ya que permiten a personas sin experiencia en programación crear contenido de forma sencilla y a personas con experiencia programar de forma más rápida y eficiente.

Puedes editar este libro de dos formas:

- **Manual**: editando los archivos Markdown (`.md`) o Notebooks (`.ipynb`) directamente con un editor de texto o un IDE como VS Code. Ejecutando scripts para compilar el libro y previsualizarlo. Haciendo commits con Git y push a GitHub para publicar los cambios.
- **Con IA**: usando un asistente de IA para que te ayude a escribir el contenido, generar código, revisar ortografía, crear gráficos, etc. Puedes pedirle a la IA que haga tareas específicas o que te ayude a mantener la estructura del libro mientras escribes. Ya no hablamos de un autocompletado de código, sino de un asistente que entiende el contexto del libro y te ayuda a crear contenido de calidad sin necesidad de saber programar.

Para que esto funcione bien, es importante que el proyecto esté bien estructurado y que la IA tenga toda la información necesaria para ayudarte. Por eso, esta plantilla está diseñada para ser fácil de usar con asistentes de IA, con una estructura clara y scripts sencillos para compilar y publicar el libro.

**Vibe Coding**: una metodología de desarrollo que enfatiza la experiencia fluida del programador mediante el uso de asistentes de IA integrados. Se trata de escribir código de forma intuitiva, dejando que agentes de IA editen el código y propongan soluciones mientras mantienes el control del flujo creativo. El principal problema de esta metodología es que puede llevar a una dependencia excesiva de la IA, lo que podría afectar a la calidad del código y a la capacidad del programador para resolver problemas por sí mismo. Sin embargo, cuando se usa de manera equilibrada, puede aumentar significativamente la productividad y la creatividad.

Como muestra la {numref}`fig-vibe-coding-karpathy-es`, el que acuñó el término fue Andrej Karpathy con una publicación que planteaba esta forma de trabajar como algo útil para proyectos rápidos y exploratorios.

```{figure} ../../_static/images/vibe_coding_karpathy_es.png
---
name: fig-vibe-coding-karpathy-es
alt: Publicación de Andrej Karpathy sobre vibe coding
width: 90%
align: center
---
Publicación de Andrej Karpathy en la que introduce el término *vibe coding*.
```

Además, personalidades como Linus Torvalds, asociadas al gusto por el código bien hecho, han mostrado interés en esta nueva forma de programar, aunque también han expresado preocupaciones sobre la calidad del código generado por IA y la necesidad de mantener un control humano sobre el proceso. En la {numref}`fig-linus-torvalds-ai-code-es` se observa esa combinación de interés práctico y criterio técnico.

```{figure} ../../_static/images/linus_torvalds_ai_code_es.png
---
name: fig-linus-torvalds-ai-code-es
alt: Comentario de Linus Torvalds sobre código asistido por IA
width: 90%
align: center
---
Comentario de Linus Torvalds sobre una integración realizada con ayuda de Google Antigravity.
```

## Cómo pedir ayuda a los asistentes de IA

Este template está diseñado para usarse con asistentes de IA como **GitHub Copilot** o **Antigravity**.

Puedes pedirle cosas como:
- "Explícame este código de Python"
- "Genera un gráfico de una función seno"
- "Revisa la ortografía de este párrafo"
- "Añade una ecuación matemática en formato LaTeX"

O incluso tareas más complejas como:

- A partir de una carpeta con tus recursos en el repositorio (PDF, imágenes, artículos, vídeos), que te ayude a escribir un capítulo completo del libro siguiendo la estructura y el estilo que has definido.
- Que traduzca ese nuevo capítulo que acabas de escribir a otro idioma, manteniendo el formato y la estructura del libro.
- Que ejecute todos los comandos necesarios para compilar el proyecto, desplegarlo en local para previsualizarlo, hacer commit con Git y push a GitHub para publicar los cambios.
- Generar de nuevo el PDF del libro en varios idiomas.
- Publicar el libro.

Como mencionábamos anteriormente, este proyecto contiene varias SKILLS. Puedes pensar en ellas como chuletas o mini-tutoriales para tareas concretas que los agentes de IA tienen a su disposición. Se encuentran en la carpeta `.github/skills/` y se mantienen sincronizadas en otras carpetas para que el proyecto sea compatible con otros agentes de IA como Claude, Codex, etc.

Rizando más el rizo, podéis crear vuestras propias SKILLS **pidiendo al asistente que las genere él mismo siguiendo el enfoque del proyecto**. Por ejemplo, si quieres una SKILL para generar gráficos con una biblioteca concreta de tu disciplina o para revisar la ortografía de un párrafo siguiendo unas normas concretas de la RAE, puedes pedirle a la IA que te genere esa SKILL siguiendo el formato de las SKILLS ya existentes en el proyecto. De esta forma, podrás tener un conjunto de SKILLS personalizadas que se adapten a tus necesidades y a las de tu proyecto.


