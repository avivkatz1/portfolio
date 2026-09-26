# Publishing Checklist

Run through this before making any repo public (or adding it to the portfolio index).

## Safety — do these first

- [ ] **No student or personal data** anywhere: code, sample files, screenshots, notebook outputs, commit history.
- [ ] **No secrets**: search the repo — `git grep -iE "api[_-]?key|secret|password|token"`.
- [ ] If a secret *was* ever committed: rotate the key now. Deleting the file doesn't remove it from history.
- [ ] `.env` is ignored; `.env.example` lists variable names only.
- [ ] Coursework: only my own work; course policy allows sharing; course has ended.

## Quality

- [ ] README has: one-line description, demo image/GIF or live link, features, tech stack, how to run.
- [ ] Someone else could clone it and run it by following the README (test in a fresh folder).
- [ ] `LICENSE` file present (Apache 2.0).
- [ ] Dependencies pinned.
- [ ] No leftover debug code, commented-out blocks, or `test2_final_FINAL.py` files.
- [ ] Notebooks cleared or trimmed; no giant outputs.
- [ ] Large files (>50 MB) and datasets are not committed — link or use Git LFS / DVC.

## On GitHub

- [ ] Repo **About** section: description, topics (e.g. `react`, `machine-learning`, `education`), website link.
- [ ] Added to `portfolio/projects/README.md`.
- [ ] If it's a highlight: pinned on profile and listed in `profile/README.md`.
- [ ] `avivkatz1` placeholders replaced.
