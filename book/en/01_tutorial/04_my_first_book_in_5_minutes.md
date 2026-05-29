# 4. My first book from scratch

This page shows a first complete workflow for creating a new book from this template: create the repository, open it on your computer, ask the agent for help, preview locally, generate PDFs, and publish the website.

The goal is not to learn Git, Python, LaTeX, or GitHub in depth before starting. The goal is to understand what is happening on each screen, what you can ask the agent to do, and where to look when you need to check that everything worked.

```{note}
The GIFs on this page are sped up so the process can be shown compactly. The initial environment setup and PDF generation can take much longer, especially the first time the LaTeX engine is installed.
```

## Step 0. Prepare the basic requirements

Before working with the template, check that the computer has the basic tools ready: a GitHub account, Python installed, Git available, and an editor with an AI agent, such as Antigravity or VS Code. As shown in {numref}`fig-first-book-04-00-en`, this step sets up the starting point before creating the repository.

GitHub will be the place where the book is stored on the internet. Python will run the scripts included in the template. Git is the tool that records the history of changes and sends them to GitHub. Antigravity or VS Code will be the workspace: you will open the book folder there, ask the agent to perform tasks, and review the files.

It is also important to configure Git for its first use. If you have never done it on that computer, open a terminal and run:

```powershell
git config --global user.name "Your name"
git config --global user.email "your.email@example.com"
```

These details are attached to commits. A commit is a snapshot of the project at a specific moment. You do not write a password or token here: only your name and email address. The email should be associated with your GitHub account if you want GitHub to recognize those changes as yours.

If you do not know whether Git is already configured, you can check it with:

```powershell
git config --global user.name
git config --global user.email
```

If those commands return your name and email, you can continue. If they return nothing, configure Git with the previous commands. This step usually only needs to be done once per computer.

```{figure} ../../_static/tutorial_gifs/first_book/04_00_requirements.gif
---
name: fig-first-book-04-00-en
alt: GIF with the basic requirements for creating the first book from scratch
width: 95%
align: center
---
Basic requirements: GitHub, Python, configured Git, and an editor with an AI agent.
```

## Step 1. Create a repository from the template

The next step is to open the template URL on GitHub and use **Use this template** to create your own repository. In this first walkthrough we will make it **public**, as shown in {numref}`fig-first-book-04-01-en`, because that simplifies the initial publication with GitHub Pages. Private repositories can be considered later.

A repository is the project folder inside GitHub. When you use the template button, GitHub does not modify the original repository: it creates an independent copy in your account. That copy will be your book. You can change the title, remove examples, add chapters, and publish the website without affecting anyone else.

When GitHub asks for the repository details, pay special attention to three fields:

- **Owner**: the account or organization where the book will be created.
- **Repository name**: the technical name of the repository. Avoid spaces and unusual characters; for example, `my-first-book`.
- **Public**: for this first exercise, public is recommended because GitHub Pages is easier to activate.

After creating the repository, GitHub will take you to a page whose address looks similar to:

```text
https://github.com/your-user/my-first-book
```

Keep that page in mind: it is the main GitHub page for your project. From there you can copy the clone URL, open **Settings**, inspect **Actions**, and check whether the website has been published correctly.

```{figure} ../../_static/tutorial_gifs/first_book/04_01_use_template.gif
---
name: fig-first-book-04-01-en
alt: GIF showing how to create a public repository from the template button
width: 95%
align: center
---
Creation of a new public repository using GitHub's template button.
```

## Step 2. Enable GitHub Actions and GitHub Pages

After creating the repository, allow GitHub to run the project workflows and publish the website. {numref}`fig-first-book-04-02-en` shows the **GitHub Pages** configuration using **GitHub Actions** as the source.

GitHub Actions is GitHub's automation system. In this template it does in the cloud what you could do on your computer: install the environment, check the project, generate the PDFs, build the website, and publish it. GitHub Pages is the service that takes that built website and makes it available at a public URL.

To configure it, open your GitHub repository and go to:

```text
Settings -> Pages -> Build and deployment -> Source -> GitHub Actions
```

If this is the first use of Actions in that account or repository, GitHub may ask for an additional confirmation to enable workflows. That detail may not appear in the GIF, but it must be accepted so the book can be built and published automatically.

The public website URL does not always appear immediately. It usually appears after the first successful deployment. There are two places where you can find it:

- In **Settings -> Pages**, GitHub usually shows a link to the published website once a successful deployment exists.
- In the **Actions** tab, open the deployment workflow run and look for the deployment summary. When everything is green, there is often a link to the published site.

The typical GitHub Pages URL for a project repository has this form:

```text
https://your-user.github.io/my-first-book/
```

If the repository belongs to an organization, the first part changes to the organization name. If you later use a custom domain, such as `libro.usal.es`, that URL can be different.

```{figure} ../../_static/tutorial_gifs/first_book/04_02_enable_pages_actions.gif
---
name: fig-first-book-04-02-en
alt: GIF showing how to enable GitHub Pages with GitHub Actions
width: 95%
align: center
---
Activation of GitHub Pages with GitHub Actions as the publication source.
```

## Step 3. Clone the repository in Antigravity

With the repository created on GitHub, copy its URL and clone it from Antigravity. {numref}`fig-first-book-04-03-en` shows the general flow: open the editor, choose the clone option, and paste the repository URL.

Cloning means downloading a complete copy of the repository to your computer. It is not just downloading a ZIP file: after cloning, the local folder remains connected to GitHub. That lets you work locally and, when you are satisfied, upload the changes with `commit` and `push`.

To find the URL you need, go back to the main page of the repository on GitHub and click the green **Code** button. In the **HTTPS** tab you will see an address similar to:

```text
https://github.com/your-user/my-first-book.git
```

Copy that URL and paste it into Antigravity's clone option. The editor will ask where on your computer you want to store the project. Choose a folder that is easy to find, such as `Documents`, `Desktop`, or a folder dedicated to your courses.

At this point GitHub may ask for authentication. That is expected: the editor needs permission to download the repository and, later, to push changes back. If a browser window or GitHub sign-in screen appears, follow the authentication flow. Do not paste passwords into project files.

```{figure} ../../_static/tutorial_gifs/first_book/04_03_clone_repository.gif
---
name: fig-first-book-04-03-en
alt: GIF showing how to clone the repository in Antigravity using the GitHub URL
width: 95%
align: center
---
Repository cloned from GitHub in Antigravity.
```

## Step 4. Ask the agent to configure the environment

When the project is opened for the first time, ask the agent to prepare the environment. It is sensible to use a low-cost model, for example **Gemini 3.1 Pro (Low)** if available, because this task is fairly mechanical and may require several interactions.

A useful prompt would be:

```text
Configure this project for the first time following the repository instructions.
Use the .venv environment and continue with the required installations.
```

The `.venv` environment is a local folder where the Python tools required by this book are installed. It prevents the project dependencies from being mixed with other programs on the computer. For a non-technical user, the key point is this: if the agent uses `.venv`, the project stays organized and the installation is easier to repeat on another machine.

As shown in {numref}`fig-first-book-04-04-en`, the agent will run commands and may ask several times whether it can continue. During this first setup, the usual answer is yes. It may ask for permission to install `uv`, create `.venv`, install dependencies, prepare LaTeX, or synchronize skills. Those questions are expected.

This step takes longer than the GIF. It depends on the connection, the computer, and whether Python, Git, or `uv` were already installed. During installation, avoid closing the editor or shutting down the computer. If it looks like nothing is happening for a few minutes, check whether the agent is waiting for confirmation in the terminal.

When it finishes, the project should normally have a `.venv` folder and the agent should be able to run the verification scripts. If something fails, do not try to fix it manually by copying random commands: ask the agent to read the error, review `AGENTS.md`, and run the setup again cleanly.

```{figure} ../../_static/tutorial_gifs/first_book/04_04_setup_environment.gif
---
name: fig-first-book-04-04-en
alt: GIF showing the initial environment setup with help from the agent
width: 95%
align: center
---
Initial project environment setup through the agent.
```

## Step 5. Make a first edit with the agent

When the environment is ready, ask for a first real change. In the example shown in {numref}`fig-first-book-04-05-en`, the agent is asked to hide the current template chapters and leave only a sample chapter about the **Central Limit Theorem**, written with LaTeX and MyST.

This first change helps you learn the workflow. You do not need to start by writing the whole book. It is better to request a small modification, check that it appears in the local website, and then publish it. That way you understand the full cycle before investing many hours in content.

The request should clearly state that the change must be made in both languages:

```text
Temporarily hide the current template chapters and leave only one sample chapter
explaining the Central Limit Theorem with LaTeX and MyST.
Do it in Spanish and English and keep the TOCs synchronized.
```

There are two important ideas in that prompt. The first is **hide**, not delete. The agent can remove sections from the menu by commenting or adjusting the TOCs, but it is useful to keep the example files because they may serve as references later. The second is **in Spanish and English**. This template is designed for multiple languages, so every visible change should have its equivalent in the configured languages.

It is also useful to ask the agent to validate the result:

```text
When you finish, check encoding, multi-language structure, and build the website.
```

If the agent modifies a Spanish page but forgets the English one, the book can become inconsistent. That is why the automatic checks are part of the normal workflow, not an extra for advanced users.

```{figure} ../../_static/tutorial_gifs/first_book/04_05_first_agent_edit.gif
---
name: fig-first-book-04-05-en
alt: GIF showing a first edit with the agent to leave a sample chapter
width: 95%
align: center
---
First assisted edit: hide example content and leave a minimal chapter in both languages.
```

## Step 6. View the local preview

After editing, ask the agent to launch a local preview. {numref}`fig-first-book-04-06-en` shows how the agent starts a server on the computer and then reports the URL where the book can be opened.

You can ask for it simply:

```text
I want to see a local preview of the book. Start the server and tell me the exact URL.
```

The URL is usually local, for example `http://127.0.0.1:8000` or `http://localhost:8000`. That means the website is not published on the internet yet: it is being served from your own PC so you can review changes before uploading them. That address only works on your computer while the local server is running.

It is important to distinguish these two URLs:

- `http://localhost:8000` or `http://127.0.0.1:8000`: local preview on your PC.
- `https://your-user.github.io/my-first-book/`: website published on GitHub Pages.

If port `8000` is already in use, the agent may choose another one, such as `8001` or `8080`. That is fine: open exactly the URL the agent gives you. If you see an old version, ask the agent to rebuild the book and restart the preview. In this template, the preview should be built with the same workflow as production, so you do not review an outdated website.

```{figure} ../../_static/tutorial_gifs/first_book/04_06_local_preview.gif
---
name: fig-first-book-04-06-en
alt: GIF showing how to launch the local preview and open the book in the browser
width: 95%
align: center
---
Local book preview through a server running on the user's own computer.
```

## Step 7. Generate the PDFs

When the local website looks right, ask the agent to generate the book PDFs. {numref}`fig-first-book-04-07-en` shows the flow in compressed form, but this process may take longer than the GIF, especially the first time.

You can ask:

```text
Generate the book PDFs in all languages and check that they were created correctly.
```

The template normally generates one PDF per language and places them in `book/_static/`, for example:

```text
book/_static/ElaboracionDeLibrosElectronicosMedianteCodigoYAsistentesDeInteligenciaArtificial.pdf
book/_static/CreatingElectronicBooksWithCodeAndArtificialIntelligenceAssistants.pdf
```

The reason for the initial wait is that the project needs a LaTeX engine to convert the book to PDF. LaTeX is the system that produces academic documents with good typography, equations, indexes, and references. You do not need to learn LaTeX to use the template, but the engine that compiles the document must be installed.

During the first generation it may look like many things are being installed. That is normal. Later runs are usually faster because the installation has already been prepared. If it fails, the important thing is to keep the error message and ask the agent to review it. It is not advisable to delete folders or reinstall tools manually without a diagnosis.

```{figure} ../../_static/tutorial_gifs/first_book/04_07_generate_pdfs.gif
---
name: fig-first-book-04-07-en
alt: GIF showing PDF generation and the initial LaTeX installation
width: 95%
align: center
---
Book PDF generation, including the initial LaTeX installation when required.
```

## Step 8. Publish the changes

Finally, ask the agent to publish the changes. As shown in {numref}`fig-first-book-04-08-en`, publishing in this template means a complete Git cycle: add files, create a commit, and push to GitHub.

A good request would be:

```text
Save the changes, commit, push, and check that the GitHub Pages deployment works.
```

The commit saves a specific version of the project with a descriptive message. The push uploads that version to GitHub. When it reaches GitHub, the deployment workflow starts. That workflow builds the book in the cloud, regenerates the PDFs, and publishes the website.

After the push, open your repository on GitHub and go to the **Actions** tab. There you will see a new workflow run. While it is running, it may appear in yellow or with a progress icon. When it finishes correctly, it appears in green. If it appears in red, the deployment failed and you need to open that run to read the error.

To find the published website URL, check these places:

- **Settings -> Pages**: after a successful deployment, GitHub usually shows the public site URL here.
- **Actions -> deployment run**: the run that published the website may include a deployment link.
- **Usual URL pattern**: if you do not use a custom domain, it will look similar to `https://your-user.github.io/my-first-book/`.

Keep in mind that the published website does not always update in the browser in the same second. If the workflow is green but you still see old content, wait a little and reload the page. You can also open a private browser window to avoid cache.

Because this template generates the PDFs first and then builds the website, the download buttons or links on the site should point to the updated PDFs. That is why manually uploading only HTML is not recommended: the full deployment keeps the website and printable documents synchronized.

```{figure} ../../_static/tutorial_gifs/first_book/04_08_publish_changes.gif
---
name: fig-first-book-04-08-en
alt: GIF showing publication through commit, push, and GitHub Actions
width: 95%
align: center
---
Book publication through commit, push, and automatic deployment with GitHub Actions.
```

At the end of this walkthrough you have the basic full cycle: create the repository, edit with the agent, review locally, generate PDFs, and publish the website. From that point on, daily work consists of repeating the same pattern with smaller changes: write, preview, validate, and publish.
