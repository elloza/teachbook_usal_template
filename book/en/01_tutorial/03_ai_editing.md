# 3. Editing with AI

This course is aimed at people with any level of programming experience. The possibilities opened up by AI assistants are enormous, because they allow people with no programming experience to create content more easily and people with programming experience to work faster and more efficiently.

You can edit this book in two ways:

- **Manually**: by editing Markdown files (`.md`) or Notebooks (`.ipynb`) directly with a text editor or an IDE such as VS Code. This also involves running scripts to build and preview the book, committing changes with Git, and pushing them to GitHub to publish updates.
- **With AI**: by using an AI assistant to help you write content, generate code, review spelling, create graphs, and so on. You can ask the AI to perform specific tasks or help you maintain the structure of the book while you write. We are no longer talking about code autocompletion, but about an assistant that understands the context of the book and helps you create quality content without needing to know how to program.

For this to work well, the project must be well structured and the AI must have all the information it needs to help you. That is why this template is designed to be easy to use with AI assistants, with a clear structure and simple scripts for building and publishing the book.

**Vibe Coding**: a development methodology that emphasizes a fluid programming experience through integrated AI assistants. It consists of writing code intuitively, letting AI agents edit the code and propose solutions while you keep control of the creative flow. The main problem with this methodology is that it can lead to excessive dependence on AI, which could affect code quality and the programmer's ability to solve problems independently. However, when used in a balanced way, it can significantly increase productivity and creativity.

As shown in {numref}`fig-vibe-coding-karpathy-en`, the term was coined by Andrej Karpathy in a post that framed this way of working as useful for quick, exploratory projects.

```{figure} ../../_static/images/vibe_coding_karpathy_en.png
---
name: fig-vibe-coding-karpathy-en
alt: Andrej Karpathy post about vibe coding
width: 90%
align: center
---
Andrej Karpathy's post introducing the term *vibe coding*.
```

In addition, figures such as Linus Torvalds, closely associated with well-crafted code, have shown interest in this new way of programming, while also raising concerns about the quality of AI-generated code and the need to keep human control over the process. {numref}`fig-linus-torvalds-ai-code-en` illustrates that combination of practical interest and technical judgement.

```{figure} ../../_static/images/linus_torvalds_ai_code_en.png
---
name: fig-linus-torvalds-ai-code-en
alt: Linus Torvalds comment about AI-assisted code
width: 90%
align: center
---
Linus Torvalds' comment on an integration done with help from Google Antigravity.
```

## How to Ask the AI for Help

This template is designed for use with AI assistants such as **GitHub Copilot** or **Antigravity**.

You can ask it things like:
- "Explain this Python code to me"
- "Generate a graph of a sine function"
- "Review the spelling of this paragraph"
- "Add a mathematical equation in LaTeX format"

Or even more complex tasks, such as:

- Starting from a folder with your resources in the repository (PDFs, images, articles, videos), helping you write a complete book chapter that follows the structure and style you have defined.
- Translating the new chapter you have just written into another language while preserving the book's format and structure.
- Running all the commands needed to build the project, deploy it locally for preview, commit the changes with Git, and push them to GitHub to publish the updates.
- Regenerating the book PDF in several languages.
- Publishing the book.

As mentioned earlier, this project contains several SKILLS. You can think of them as cheat sheets or mini-tutorials for specific tasks that AI agents have available. They are located in the `.github/skills/` folder and are kept synchronized in other folders so that the project is compatible with other AI agents such as Claude, Codex, and others.

Taking this idea one step further, you can create your own SKILLS **by asking the assistant to generate them itself following the project's approach**. For example, if you want a SKILL for generating graphs with a library specific to your discipline, or for reviewing the spelling of a paragraph according to a particular style guide, you can ask the AI to generate that SKILL using the format of the existing project SKILLS. This way, you can build a set of custom SKILLS adapted to your needs and to the needs of your project.
