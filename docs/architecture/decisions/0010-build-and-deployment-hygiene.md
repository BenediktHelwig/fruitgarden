# 0010. Build and deployment hygiene

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

Four separate defects around building and shipping the game; each is small, and together they mean the packaged game does not run and the source cannot be reproduced.

(a) **The packaged executable is broken.** `main.spec` declares `datas=[]`, so `pics/` is not bundled. The frozen executable loads `pics/raven.png` relative to its working directory. Run `dist/main/main.exe` from anywhere without a `pics/` folder beside it and the game crashes on the first image load, with no message explaining why. The artefact presents itself as self-contained and is not.

(b) **Generated artefacts are under version control.** `build/` and `dist/` are committed — the frozen CPython 3.9 interpreter, pygame `.pyd` extensions, the SDL2 DLLs. Of 128 tracked files, roughly 110 are regenerable build output. `__pycache__/` and the Visual Studio folder `.vs/` (including `.suo` and an SQLite workspace database) are tracked as well. The git history of a 398-line learning project is dominated by rebuilt binaries; searching that history for a change to a rule means searching past megabytes of noise.

(c) **No dependency declaration.** There is no requirements.txt and no pyproject.toml. The bundle was frozen against CPython 3.9; the developer's current interpreter is 3.14.4. Nothing records which pygame version the game was built and tested against. Returning to the project after six months, a failure cannot be attributed to a change or to a version.

(d) **Two spec defects.** `pathex` still points at `C:\Users\Umschueler\source\repos\fruitgarden` — a path from a different machine and user account. `console=True` opens a console window beside the game, which for a pre-school player (quality goal 3) is an unexplained black rectangle.

## Decision Drivers

- Quality goal 1 (Learnability / Maintainability): the repository should contain what a human wrote, not what a tool produced.
- Quality goal 2 (Correctness of the game rules): a game that crashes on start is not correct by any measure.
- Quality goal 3 (Usability for a pre-school child): no stray console window.
- These fixes are independent of the redesign and can be done first, at once.

## Considered Options

- Option 1: Fix all four together as one hygiene step.
- Option 2: Fix only the asset bundling — the one defect the player can actually see.
- Option 3: Move to a modern packaging setup (pyproject.toml, a lock file, a build workflow).

## Decision Outcome

Chosen option: "Option 1", because it addresses all quality goals simultaneously without adding unnecessary complexity for a solo developer.

Changes:
- `main.spec`: `datas=[('pics', 'pics')]`, `console=False`, and `pathex` corrected to the current repository or emptied.
- `.gitignore` for `build/`, `dist/`, `__pycache__/`, `*.pyc`, `.vs/`; those paths removed from tracking with `git rm --cached` (the working tree is untouched — the files stay on disk).
- `requirements.txt` with pinned versions — pygame at the version the game is verified against, plus pytest for [ADR-0008](0008-pytest-test-seam-without-display.md).
- Record the target Python version explicitly rather than leaving it implied by the old bundle.

Rejected option 2: leaves the repository unreadable and the environment unreproducible, for no saving worth having.

Rejected option 3: right for a project with more than one developer; here it adds tooling to learn that does not serve either of the top two quality goals.

### Positive Consequences

- The packaged game runs from any directory.
- The history becomes readable and the clone small.
- A returning developer can recreate the environment from a file.
- No console window in front of a four-year-old.

### Negative Consequences

- Removing tracked artefacts is a large one-off commit.
- The existing bundle in `dist/` disappears from the working copy of anyone who pulls without rebuilding.
- Pinned versions need occasional deliberate updating.

## More Information

Resolves chapter 11 findings 5, 7 and 8, and the secondary defects recorded in arc42 chapter 7. Independent of every other decision — it is the first step of the migration. Related: [ADR-0008](0008-pytest-test-seam-without-display.md).
