# Contributing

## 🎉 Thanks for wanting to contribute

Flask-AuthX is my hobby project, but I take care of it as if it were professional.

Having someone like you here is already a lot. No matter your level, you are welcome.

> Este documento también está disponible en [Español](CONTRIBUTING.spanish.md) (This document is also available in Spanish).

## 🐞 Report bugs

Open an issue with the ["Bug report" template](https://github.com/kronnor919/flask-authx/issues/new?template=bug_report.md) and fill in all fields.

Not sure if it's a bug?

First create a Discussion in the "Help" category. We'll discuss it there and if it's a bug, we'll move it to issues.

## 💡 Propose features

Open an issue with the ["Feature request" template](https://github.com/kronnor919/flask-authx/issues/new?template=feature_request.md).

You can also share your idea in Discussions (category "Ideas") before publishing it. This way you get fast feedback and we improve it together.

## 🛠 Environment setup

```bash
git clone https://github.com/kronnor919/flask-authx
cd flask-authx
```

### With UV (recommended)

```bash
uv sync
```

Works on Linux, macOS and Windows.

### With pip

1. Create virtual environment:

    ```bash
    python -m venv .venv
    ```

    (use `python3` if necessary)

2. Activate:

    - Linux / macOS: `source ./.venv/bin/activate`
    - Windows: `./.venv/Scripts/activate`

3. Install dependencies (including dev dependencies):

    ```bash
    pip install .
    pip install . --group dev
    ```

## ✅ Linting

Formatting and linting: Ruff (default configuration)

Before each commit, Ruff runs automatically.
If something doesn't follow the rules, it fixes it automatically.
Add the changes again (`git add .`) and repeat the commit. That easy.

## 🧪 Tests

- Run tests: `pytest tests/`

- No minimum test coverage yet

- All tests must pass to make a commit

## 📝 Conventional Commits

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

Format: `<type>(<scope>): description`

Common types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, semicolons, etc.
- `refactor`: Code restructuring
- `test`: Add or modify tests

Example: `feat(auth): add email validation`

## 📚 Documentation

### Rules

1. **Translation** - If you contribute to documentation, you must keep both English and Spanish versions synchronized:

    - English version: `name.ext` (e.g.: `README.md`, `CONTRIBUTING.md`)
    - Spanish version: `name.spanish.ext` (e.g.: `README.spanish.md`, `CONTRIBUTING.spanish.md`)

2. **Bilingual reference** - Before starting with the relevant content of the English file, make it clear that there is a Spanish version. This specification must be in both languages and include a direct reference to the Spanish version. It can be at the beginning or after a brief introduction. Spanish files do not need this reference.

    Expected format:

    ```markdown
    > [Your clarification in Spanish (Reference to the file)] ([Your clarification in English])
    ```

    Example:

    ```markdown
    > Este documento también está disponible en [Español](CONTRIBUTING.spanish.md) (This document is also available in Spanish).
    ```

3. **Identical format** - Both files must use the same syntax (.md or .rst)

4. **Consistent structure** - Same hierarchy of headings, lists and code

5. **Emoji decoration** - Keep the same emojis in the same positions

6. **Content** - As identical as possible in structure, with language-adapted text

7. **Tone** - Can be friendly and a little colloquial, but never disrespecting anyone or anything

## 🔁 Pull Request flow

1. Fork the repository to your account.

2. Clone locally:

    ```bash
    git clone https://github.com/your-username/your-fork.git
    cd your-fork
    git remote add upstream https://github.com/kronnor919/flask-authx
    ```

3. Create branch:

    ```bash
    git checkout -b descriptive-name
    ```

4. Make clear and atomic commits:

    ```bash
    git commit -m "fix: error validating email"
    ```

5. Keep your branch updated:

    ```bash
    git fetch upstream
    git rebase upstream/main
    ```

6. Push changes to your fork:

    ```bash
    git push origin branch-name
    ```

7. Open a Pull Request from your fork to this repository.

    - Clear title
    - Description that explains what changes and why
    - Reference the issue if it exists (`Closes #42`)

8. Review:

    - I may request changes or make comments
    - You add more commits to the same branch
    - They are automatically seen in the PR

9. Merge:
    Merge policy: normal merge with `--no-ff`.
    I review, approve and merge.
    The branch is deleted manually.
    My availability is very variable, but I assure you that I will review and respond to each PR.

## ❓ Need help?

The only community forum is [GitHub Discussions](https://github.com/kronnor919/flask-authx/discussions).

Open a Discussion in the "Help" category.
