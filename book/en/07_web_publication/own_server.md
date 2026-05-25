# Own Server

Publishing to an own server lets you deploy the same book under an institutional domain, for example `libro.usal.es`, using SFTP. This option is useful when the website must integrate with university infrastructure or when you need control over the final domain.

## What the server needs

The server must allow SFTP access with username and password, and it must provide a public directory where the generated website can be copied. In many hosting setups this directory is called `public_html`, although the exact name depends on the institutional configuration.

The SFTP deployment does not configure the domain by itself. There are two separate pieces:

- **Server**: receives the HTML, CSS, JavaScript, image, and PDF files.
- **Domain**: points an address such as `libro.usal.es` to the correct server.

The template builds and uploads the files. DNS and hosting configuration depend on the institution's web service.

## Required secrets

The `.github/workflows/sftp-deploy.yml` workflow uses GitHub Actions secrets. They must be configured in **Settings → Secrets and variables → Actions**:

| Secret | Purpose |
|---|---|
| `SFTP_SERVER` | SFTP server name or connection domain. |
| `SFTP_USERNAME` | SFTP username. |
| `SFTP_PASSWORD` | SFTP password. |
| `SFTP_PORT` | SFTP port. Optional; if missing, `22` is used. |

```{warning}
Do not write these values in `.yml` files, Markdown, notebooks, or scripts. They must exist only as repository secrets.
```

## Running the deployment

The own-server deployment is manual. To run it:

1. open the **Actions** tab in GitHub;
2. select **sftp-deploy-book**;
3. click **Run workflow**;
4. enter the remote directory, `public_html` by default;
5. confirm the run.

The workflow builds the complete book, generates the PDFs, and uploads `book/_build/html` to the selected remote directory.

## Remote directory cleanup

The SFTP deployment synchronizes the server with cleanup: remote files that no longer exist in the local build are deleted. This prevents old pages from remaining published by accident.

Before deployment, the workflow validates that the remote directory is not a dangerous path such as `/`, `.`, `..`, or an absolute path. Even so, check the `remote_dir` value carefully, because that directory will be made to match `book/_build/html`.

## When to use an own server

Use an own server when:

- you need to publish under an institutional domain;
- the book must integrate with an existing website;
- the university provides SFTP hosting;
- you want to separate final publication from the GitHub domain.
