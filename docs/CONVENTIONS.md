# Conventions

The rules I follow so every repo looks and works the same.

## Naming

| Thing | Format | Example |
| --- | --- | --- |
| Repos | `kebab-case`, descriptive | `register-app`, `sketch-3d-pipeline` |
| Course folders | `CODE-NUM-short-name` | `DSC-445-machine-learning` |
| Assignment folders | `hwNN-topic` / `labNN-topic` | `hw03-decision-trees` |
| Python files | `snake_case.py` | `train_model.py` |
| Notebooks | `NN-description.ipynb` (run order) | `01-eda.ipynb`, `02-train.ipynb` |

## Every project repo has

1. **README.md** — what it is, a demo (GIF/screenshot/live link) near the top, how to run it, tech stack.
2. **LICENSE** — Apache 2.0.
3. **.gitignore** — secrets, environments, data, and build output stay out.
4. **docs/demo/** — screenshots and GIFs the README uses (keep each under ~5 MB).
5. **.env.example** — names of required environment variables, never real values.
6. **CHANGELOG.md** — short dated notes on notable changes.

## Commits

- Small, focused commits with present-tense messages: `Add coach dashboard filters`, `Fix change calculation rounding`.
- Work on a branch for anything big; merge to `main` when it works.
- `main` should always run.

## Code quality

- Pin dependencies (`requirements.txt` / `package-lock.json`).
- Clear notebook outputs before committing unless the output *is* the point (then keep it small).
- Add at least a few tests for core logic in `tests/`.
- Use a formatter: `black`/`ruff` for Python, `prettier` for JavaScript.

## Demos

- Record a short GIF (5–15 seconds) of the main feature. On macOS: `Cmd+Shift+5` to record, then convert to GIF.
- If the app is deployed, link it at the top of the README.
- Use fake/sample data in every screenshot.

## Privacy (non-negotiable)

- **No real student data, ever.** No names, IEP content, grades, photos, or anything identifying.
  Use synthetic sample data for demos and tests.
- No API keys, passwords, or tokens in code or history. Use `.env` (ignored) + `.env.example`.
