# Migration Roadmap

This roadmap sequences the eleven proposed architecture decisions (ADRs 0001–0011) into an order that can actually be walked. The ordering principle is simple: **the game must remain playable after every step**. This is a single-developer learning project with a four-year-old as its user, so a migration that leaves it broken for a week is a migration that will not be finished.

## Steps

### Step 1: Repository and Build Hygiene

**What is done:** 
- Add `.gitignore` and remove build artefacts (`build/`, `dist/`, `__pycache__/`, `.vs/`) from version control
- Bundle `pics/` in `main.spec` with `datas=[('pics', 'pics')]`
- Set `console=False` to hide the debug console
- Fix the stale `pathex` in main.spec
- Create `requirements.txt` with pinned pygame and pytest versions
- Rebuild the packaged executable

**ADRs realised:** ADR 0010

**Why here:** This step touches no logic, so the game remains runnable throughout. It makes every later diff readable (roughly 110 of 128 tracked files are build artefacts), revealing the actual changes. It fixes the one defect a user can see: the packaged `.exe` crashes on start when run from any directory without a `pics/` folder.

**Done when:** A fresh clone plus `pip install -r requirements.txt` runs the game, and the rebuilt bundle starts from an arbitrary directory without errors.

---

### Step 2: Build the Domain Model Alongside the Running Game

**What is done:**
- Create `domain/` package with `Game`, `Orchard`, `Tree`, `Fruit` (base + subclasses for Red, Yellow, Green, Blue), `Raven`, `Basket`, `Dice`, `DieFace` (enum), `GameStatus` (enum)
- Implement the rules: fruit harvesting, raven's five steps (as integers, not pixels), win/loss conditions
- Write pytest tests covering harvesting, the raven's complete path, win condition, loss condition
- Add an AST test proving no file under `domain/` imports pygame

**ADRs realised:** ADRs 0001, 0002, 0003, 0004, 0005, 0008

**Why here:** This adds files and changes none. `main.py` keeps running untouched throughout, so the game stays playable while the entire model is built and tested. This is the largest step and the one that carries the whole design. Separating it from presentation work means all tests run without a display.

**Done when:** `pytest` covers harvesting (pop a fruit from a tree), the raven's five rolls and steps, the win condition (all trees empty), the loss condition (raven at step 5), and an AST check proves no import of pygame under `domain/`.

---

### Step 3: Move the Presentation Onto the Domain

**What is done:**
- Rewrite rendering and input paths against the domain: `AssetCache` loads images and fonts once at startup, `Sprite` exposes bounds publicly, `Layout` becomes a data table of coordinates, `BoardView` renders the game state, `EndView` renders the end screen
- Delete the module-level lists (`redAppleList`, etc.) and the `draftResult` state machine
- Rename `main.py` to `app.py`; compose domain and presentation
- Remove German strings and the debug print
- Delete the rule block from main.py (now replaced by `domain.Game.apply_roll()`)

**ADRs realised:** ADR 0007 (completing ADR 0001)

**Why here:** Only possible once step 2 provides a domain to render. This is the only step during which the game is temporarily not playable, so it should be one focused sitting rather than several. After this step, pygame imports exist only under `presentation/` and `app.py`.

**Done when:** The game plays exactly as before, no `pygame` import exists outside `presentation/` and `app.py`, and images and fonts load once at startup rather than sixty times a second.

---

### Step 4: Delete module/objects.py

**What is done:**
- Delete `module/objects.py` (the orphaned sketch of a domain model)
- Delete the empty `module/` package
- Verify nothing imports them (nothing does today)

**ADRs realised:** ADR 0009

**Why here:** After step 2, once `domain/` actually fulfils what that sketch was reaching for. Trivial in effort, deliberately not first: deleting it earlier would remove the evidence of the idea before its replacement exists. Keeping it until now avoids the situation ADR 0009 exists to prevent (a domain model nothing imports).

**Done when:** The file and package are gone and git shows no import errors.

---

### Step 5: The Basket Roll Becomes a Player Choice

**What is done:**
- Add `AWAITING_FRUIT_CHOICE` state to `GameStatus`
- Make trees clickable (detect clicks on tree sprite bounds)
- Show visually which trees can be picked (highlight non-empty trees during the choice state)
- Delete the 44 lines of duplicated fallback chains
- Update win/loss conditions to account for the new state

**ADRs realised:** ADR 0006

**Why here:** Last, because it is the only intentional change of *behaviour*—everything before it is structural. Keeping it separate means that if the four-year-old finds something wrong after this step, the cause is unambiguous.

**Done when:** Rolling the basket waits for a click on a fruit-bearing tree, empty trees are rejected with visual feedback, and a full game can be played with the new rule.

---

## Dependencies

| Step | Depends On | Can Run In Parallel |
|------|-----------|-------------------|
| 1 | None | Independent; can run at any time |
| 2 | None | Independent of step 1; can run in parallel |
| 3 | Step 2 | Cannot start until domain is complete |
| 4 | Step 2 | Cannot start until domain exists; can run in parallel with step 3 if desired, but step 3 should complete first |
| 5 | Step 3 | Cannot start until presentation layer is rewritten |

Steps 2 and 3 together form a coherent block: a domain without a presentation that renders it reproduces the problem ADR 0009 addresses (a model nobody uses).

---

## What This Does Not Cover

- Restart after the end screen (the player still closes the window)
- Sound effects or music
- Menu or settings screen
- Score tracking or statistics
- Difficulty levels or variations

The end-screen German strings "Verloren"/"Gewonnen" and the leftover `print("Kleine Änderung")` at main.py:398 are cleaned up as part of step 3 rather than earning a step of their own.

---

## Risk

The largest risk is stopping halfway—specifically after step 2. A completed `domain/` package sitting beside a `main.py` that ignores it reproduces exactly the situation ADR 0009 exists to clear up: a domain model the application does not use, neither dead enough to delete nor alive enough to matter.

Steps 2 and 3 belong together. The timeline for step 2 and step 3 combined should be planned as a single engagement: build the model (week 1), rewrite the presentation against it (week 2), not "finish the model in May and get to rendering in September."
