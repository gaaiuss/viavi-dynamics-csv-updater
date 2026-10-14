### Python Environment

This is a setup for a basic Python project.

---

### Explaining files

`/src`: folder for all the scripts/codes (python files, modules, config files).

`.env-example`: environment variables example file for base .env setup. Rename it to '.env' after changing it.

`.gitignore`: git ignored files list, names listed in the file will not be managed by git and consequently will not be posted on GitHub.

`python-version`: Python version used on this repository.

`pyproject.toml`: uv configuration file that lists and configures all the project dependencies (names, versions, linters, folder hierarchy).

---

### Initial requirements

1. [Python](https://www.python.org/downloads/)
2. [Git](https://git-scm.com/downloads)
3. [VS Code](https://code.visualstudio.com/)

On Windows, allow PowerShell to execute scripts (like virtual environments).

1. Open PowerShell **as admin**
2. Run this command:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Reboot if necessary.

---

### UV Manager

[uv](https://docs.astral.sh/uv/getting-started/)

```sh
# UV installation (Windows, Linux, Mac)
# Windows PowerShell:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS (curl)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```sh
# Creates the full project
directory: uv init project-name

# Initialize an existing project:
uv init
```

```sh
# Installs Python, creates venv and installs dependencies
uv sync
```

```sh
# Install packges
uv add requests ruff pyright

# Remove packages
uv remove requests
```

```sh
# Runs Python scripts without activating venv
uv run src/main.py

# Installs tools like ruff or pyright globally
uv tool install ruff
uvx ruff
uv tool uninstall ruff
```

---

### Git Config

```bash
# Initialize repository
git init # Don't need to do this if UV already done it.

# Configures Global User
git config --global user.name "gaaiuss"
git config --global user.email "caio.gui.castro@gmail.com"

# Standard branches to 'main'
git config --global init.defaultBranch main
git branch -m main

# Standard end of line for multiplatform
git config --global core.autocrlf input
git config --global core.eol lf

git config --list --global

# First commit
git add .
git commit -m "initial"

# Congigure repository
git remote add origin URL_REPO_SSH
git push origin main -u

# Future commits
git add .
git commit -m "MENSAGEM"
git push
```

---

### `.env` e `.env-example`

Default pattern for env variables, `python-dotenv` is already added as a project dependency:

```bash
uv sync
```

Copy `.env-example` to another file named `.env` to activate the env variables.
