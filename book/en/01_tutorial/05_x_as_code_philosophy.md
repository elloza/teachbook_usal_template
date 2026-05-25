# 5. The "X as code" Philosophy

One of the important ideas we want you to take from this course is the possibility of editing and generating teaching artifacts through programming languages and markup languages. This is what we call the "X as code" philosophy. It means using code as a medium to describe and generate educational resources, so that we can benefit from the fact that LLMs can understand and manipulate that code to help us create quality materials without manually editing every artifact.

## What is "X as code"?

When we talk about "X as code", we mean the idea that an educational resource (X) can be described and generated through a programming language or a markup language. Instead of creating a diagram, plot, animation, or quiz directly in a visual tool, we describe it with code. Then that code is compiled or executed to generate the final artifact.

The idea is to use programming languages and markup languages as **intermediate languages** for generating teaching artifacts: images, diagrams, animations, videos, simulations, quizzes, tables, notebooks, and PDFs.

In other words: working with **X as code**.

- *Diagrams as code*: diagrams written as text.
- *Figures as code*: plots and figures generated from data or formulas.
- *Animations as code*: educational videos rendered from a programmed scene.
- *Quizzes as code*: questions, solutions, and exercise banks defined as structured text.
- *Books as code*: a complete book compiled from Markdown files, notebooks, and configuration.

```{admonition} Key idea
A teaching artifact generated from code is not edited "by hand" at the end of the process. It is described with an intermediate language, where AI assistants can understand the structure and content, and then the final result is generated through a compilation or execution process.
```

## Why is this philosophy interesting?

One of the problems with generating content using AI tools is that the final result is often an image, PDF, or video that cannot be edited easily. If you want to change something, you have to regenerate the artifact from scratch or edit it manually, which can be complicated and time-consuming.

In the end, the advantage AI offers for generating content quickly is lost if the result is not editable. In contrast, if the artifact is generated from code, you can ask the AI to edit that code to make changes, generate new versions, or adapt the content to different contexts.

Having this intermediate language is sometimes key for AI to help you generate quality content. For example, if you want to generate a flowchart, you can describe it with Mermaid or Kroki code. The AI can understand that description and help you modify, translate, or adapt it without needing to edit the final image.

## Code as a bridge to the final result

When you draw a diagram directly in a visual tool, the result is locked inside that interface. If you want to change ten arrows, translate labels, or adapt the style, you have to edit it manually again.

When you describe that same diagram with code, an intermediate layer appears:

As shown in {numref}`fig-diagram-01-tutorial-05-teaching-code-philosophy-01`, the diagram is versioned as a static image.

```{figure} ../../_static/generated/diagrams/en/01_tutorial_05_teaching_code_philosophy_01.svg
:name: fig-diagram-01-tutorial-05-teaching-code-philosophy-01
:alt: Diagram: Code as a bridge to the final result
:width: 90%
:align: center

Diagram: Code as a bridge to the final result.
```

The following table summarizes the main elements of this section.

**Table. What artifacts can be generated from code?.**

| Final artifact | Intermediate language | Teaching use case |
|---|---|---|
| Diagram | Mermaid/Kroki, GraphViz, PlantUML | Concept map, experiment flow, process schema |
| Scientific plot | Python + matplotlib | Represent real or simulated data |
| Electrical circuit | Schemdraw or CircuitikZ | Generate consistent schematics for Physics problems |
| Animation or video | External tool + MP4 | Explain a transformation, a wave, or a proof step by step without loading the base installation |
| Table or dataset | Python + pandas | Create clean tables from raw data |
| Quiz | MyST, JupyterQuiz, structured Markdown | Review questions with collapsible solutions |
| Executable notebook | Jupyter Notebook | Simulation, reproducible calculation, guided practice |
| Web book and PDF | Jupyter Book/TeachBooks | Publish the same material as a website, download, and printable version |

## Why this fits so well with AI

AI does not "understand" a final image the way it understands a code-based description. If you give it a screenshot of a diagram, it can suggest changes; if you give it the Mermaid or Kroki code that generates it, it can **make** those changes.

```{admonition} The practical advantage
:class: tip
We do not ask AI to edit pixels. We ask it to edit instructions. Then the system recompiles those instructions and produces the final artifact.
```

This makes it possible to ask for things like:

- "Turn this flowchart into a state diagram".
- "Generate an English version while keeping the same structure".
- "Adapt the example so it uses Biology data instead of Physics data".
- "Prepare the visual script for a 20-second animation showing this function growing".
- "Create three versions of the quiz with different difficulty levels".

The key is that the final result is not handcrafted every time. It is produced from an editable recipe.

## Reproducibility, not just automation

Working "as code" does not mean making things more complicated. It means every artifact has a clear recipe:

1. **Input**: data, formulas, text, or a teaching idea.
2. **Intermediate language**: Markdown, Python, Mermaid, LaTeX, etc.
3. **Compilation**: the system transforms that description.
4. **Output**: image, video, website, PDF, notebook, or quiz.

If you change the recipe, you regenerate the artifact. If something fails, you fix the recipe. If another teacher wants to adapt it, they do not start from scratch: they modify the recipe.

## The mindset shift

The question stops being: "Which program should I use to draw this?"

The question becomes: "Which intermediate language best describes this artifact?"

Not every material needs code. But when a resource will be revised, translated, versioned, reused, or generated with AI support, it is worth asking whether it can be expressed as **X as code**.

That is the teaching-as-code philosophy: using code not as an end in itself, but as a **generative medium** between the teaching intention and the final artifact.
