# GitHub Pages

GitHub Pages is the default deployment route for this template. It is the simplest flow because it does not require an own server: GitHub Actions builds the book and GitHub Pages serves the resulting website.

## What the workflow does

The `.github/workflows/deploy.yml` file runs when changes are pushed to `main` and can also be started manually from the **Actions** tab. In each run it:

1. prepares Python 3.12;
2. installs the project environment with `scripts/setup_env.py`;
3. checks UTF-8 encoding and static assets;
4. installs the lightweight LaTeX toolchain;
5. generates the PDFs for all languages;
6. builds the multi-language HTML site;
7. publishes `book/_build/html` to GitHub Pages.

This order matters: PDFs are generated first and the website is built afterwards, so download links always point to current files.

## Initial activation

In a new repository created from the template, the recommended setup is:

1. open **Settings** in GitHub;
2. go to **Pages**;
3. choose **Source: GitHub Actions**;
4. save the configuration;
5. push the first change to `main`.

After the first `push`, GitHub runs the `deploy-book` workflow. If it finishes successfully, the public URL appears on the GitHub Pages settings page and in the action summary.

## Public and private repositories

The workflow is configured to read repository contents with minimum permissions. In private repositories, publication depends on the GitHub Pages features available for the account or organization. If GitHub Pages is not available for that repository, the book can still be built, but it will not be published through this route.

## When to use GitHub Pages

Use GitHub Pages when:

- you want to publish quickly without requesting a server;
- the book can live under a GitHub URL;
- each change in `main` should update the website automatically;
- you are using the template for the first time and need the lowest-configuration path.
