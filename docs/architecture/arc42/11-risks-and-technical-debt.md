# 11. Risks and Technical Debt

## Introduction

Nearly all findings below trace to a single architectural property: **the render model is the domain model.** There is no boundary between how the game is drawn and what the game is. Fruit counts live in lists because fruit is drawn by iterating lists. The raven's progress is a pixel coordinate because the raven is drawn at that coordinate. Win and loss conditions are implicit in the rendering code. This coupling makes every rule change difficult, every bug fix risky, and every test impossible without opening a window.

The findings are listed in order of impact on the ranked quality goals. Each entry states what is wrong, which quality goal it damages, and the direction a fix would take in one sentence.

Every finding below now carries a reference to the architecture decision that resolves it; all of those decisions currently have status `proposed`, so nothing here is fixed yet—the references say how, not when. See [migration-roadmap.md](../migration-roadmap.md) for the order in which these changes will be sequenced.

---

## 1. No Separation of Domain and Presentation

**What is wrong:** Game state is pixel coordinates and list lengths. There is no object that owns the rules. The raven's progress is `raven.picPosX` (a pixel coordinate). The fruit count is "count the non-empty lists." A rule change requires finding every place where rendering and state-checking are interleaved.

**Quality goal damaged:** Learnability / Maintainability (primary goal), Correctness (secondary)

**Scenario:** You want to change the game so the raven advances only every two rolls, not every one. You must search for every place that calls `raven.moveForward()` and understand whether it is safe to modify. The answer depends on understanding how the render loop uses `raven.picPosX` to draw the sprite—coupling that is spread across construction (lines 140–145), the move method (lines 46–48), the loss check (line 317), and the draw call (line 342).

**Direction:** Extract a rules object that owns fruit counts and raven steps (as integers, not pixels or lists), with rendering reading from it as a view.

**Resolved by:** [ADR 0001](../decisions/0001-separate-domain-model-from-presentation.md) — the layer rule; `Game` owns the rules

---

## 2. draftResult Is Never Reset

**What is wrong:** The module-level variable `draftResult` is set once when the die is rolled and persists until the next roll. The rule block (lines 265–313) sits at the same indentation level as the hit test (line 263), both inside the `MOUSEBUTTONDOWN` event handler—there is no guard. When a player clicks anywhere in the window, they trigger a `MOUSEBUTTONDOWN` event; if they miss the dice, the die is not rolled; but the rule block re-applies the stale `draftResult` anyway.

**Consequence:** once any roll has happened, every subsequent click anywhere re-applies that same result until the next successful die roll. A single lucky colour roll lets the player empty that fruit's tree by clicking; a single raven roll lets the player walk the raven to the gate by clicking.

**Quality goal damaged:** Correctness of the game rules (goal 2)

**Scenario:** A player rolls red (harvests one red apple) then mashes the mouse button 16 times without rolling the die again. With each click, the rule block re-applies "red", popping a fruit from `redAppleList`. After 4 clicks, the red apples are gone (the rest of the time the list is empty so nothing happens). Then they roll raven once, click 5 times, and the raven reaches the gate and the game is lost—all without ever meaningfully rolling the die.

**Direction:** Clear `draftResult` to `"none"` after the rule block applies it, or move the rule block inside the `if dice.overDice():` condition.

**Resolved by:** [ADR 0005](../decisions/0005-die-faces-as-enum-and-guarded-roll.md) — `Game.roll()` as the only mutation, `last_face` as a display value only

---

## 3. The Basket Rule Diverges from the Board Game

**What is wrong:** In the physical *Obstgarten*, rolling the basket lets the player *choose* which fruit to take. The digital game implements basket rolls as a random choice with a fallback chain (lines 276–313): pick a preferred stock; if empty, try the next; if empty, try the next. This is not player choice, and a child notices the difference immediately.

**Quality goal damaged:** Correctness of the game rules (primary goal), Usability for a pre-school child (tertiary goal)

**Scenario:** A child plays the digital game after playing the physical one. They roll the basket and expect to click a tree to choose fruit. Instead, the game gives them a random apple and moves on. They notice and ask "why can't I choose?"

**Direction:** Turn fruit into clickable elements; when a basket is rolled, allow the player to click a fruit to harvest it, rather than auto-selecting one.

**Resolved by:** [ADR 0006](../decisions/0006-basket-roll-becomes-player-choice.md) — an `AWAITING_FRUIT_CHOICE` state and clickable trees

---

## 4. module/objects.py Is Orphaned and Broken

**What is wrong:** `module/objects.py` is never imported by any other file in the repository. It is a sketch of a domain model—an earlier attempt at building a `Tree` class that would have owned fruit state. The sketch contains bugs: `Tree.__init__` calls `super.__init__(self, name)` using `super` as a builtin, not `super()`, which would raise `AttributeError` on construction. `Element.getPicture()` references an undefined global `screen`. The file contributes nothing to the runtime.

**Quality goal damaged:** Learnability / Maintainability (primary goal)

**Scenario:** A developer reading the repository for the first time finds `module/objects.py` and tries to understand it. They run it and get an error. They wonder if it is supposed to be used. It is confusion and technical debt.

**Direction:** Delete it, or promote it by fixing the bugs and making it the real domain module, replacing the module-level lists and rules in `main.py`.

**Resolved by:** [ADR 0009](../decisions/0009-retire-module-objects-py.md) — deleted once `domain/` fulfils its intent

---

## 5. pics/ Is Not Bundled in the PyInstaller Package

**What is wrong:** The `main.spec` build definition declares `datas=[]`, excluding all additional files from the bundle. When PyInstaller packages the game, `pics/` is not included. The packaged executable attempts to load `pics/raven.png` relative to its working directory at runtime. If the user runs the `.exe` from a directory that does not contain a `pics/` folder, the game crashes with a file-not-found error. The executable advertises itself as self-contained (it is an `.exe` in `dist/main/`) but is actually dependent on an external asset folder.

**Quality goal damaged:** Correctness of the game rules (goal 2); also Deployability, which is outside the ranked goals

**Scenario:** A user downloads the packaged game from `dist/main/main.exe` and tries to run it from their Desktop. The window opens, then crashes when trying to load the first image. No error message tells them to copy `pics/` alongside. They are confused and assume the application is broken.

**Direction:** Declare `pics/` in `datas` in `main.spec` so it is copied into the bundle.

**Resolved by:** [ADR 0010](../decisions/0010-build-and-deployment-hygiene.md) — `datas=[('pics', 'pics')]` in main.spec

---

## 6. Encapsulation Bypassed by Name Mangling

**What is wrong:** Python name mangling (prefixing private attributes with `_ClassName__`) is meant to prevent accidental use of private state from outside the class. The `Dice.overDice()` method (line 72) reads `self._Element__pictureWidth` and `self._Element__pictureHeight` directly, reaching into the parent class's private namespace. This is technically possible but semantically wrong: the code says "I am reaching past the encapsulation boundary to access something I should not." It is a code smell indicating that `Element` should expose its bounds, not hide them.

**Quality goal damaged:** Learnability / Maintainability (primary goal)

**Scenario:** A future developer reads `Dice.overDice()` and sees `self._Element__pictureWidth`. They do not understand why the name is mangled. They look for documentation on the attribute and find none. They wonder if this is a bug or intentional. They do not change it because it works and they do not understand it.

**Direction:** Expose a public method or property on `Element` (e.g., `get_bounds()` or `.rect`) that returns the sprite's bounds; use it from `Dice.overDice()`.

**Resolved by:** [ADR 0007](../decisions/0007-layout-and-assets-as-data.md) — `Sprite` exposes its bounds publicly

---

## 7. Generated Artefacts Under Version Control

**What is wrong:** The `build/` and `dist/` directories are committed to git. These are PyInstaller output: temporary intermediates and the final bundled executable (8.2 MB + 29 MB respectively). They contain the frozen Python 3.9 interpreter, pygame `.pyd` extensions, and SDL2 DLLs. Meanwhile, `.git` is 18 MB. Committing regenerable artefacts means the repository's history is dominated by compiled output rather than the 454 lines of source code the author is trying to learn from.

**Quality goal damaged:** Learnability / Maintainability (goal 1)

**Scenario:** When reading the git log to understand how the code evolved, most commits have large binary diffs in `dist/` and `build/`. When searching git history for a change to a rule, the results are buried in noise from rebuilds. The author's learning artefact is obscured by its own deployment pipeline.

**Direction:** Remove `build/` and `dist/` from version control and add them to `.gitignore`.

**Resolved by:** [ADR 0010](../decisions/0010-build-and-deployment-hygiene.md) — `.gitignore` plus `git rm --cached`

---

## 8. No Dependency Declaration, and Version Drift

**What is wrong:** The repository contains no `requirements.txt` or `pyproject.toml`. The dependencies are implicit: pygame and (transitively) SDL2. The PyInstaller bundle was built against CPython 3.9 (visible in `cp39-win_amd64.pyd` and `python39.dll`). The developer's current Python interpreter is 3.14.4. Nothing in the repository records which pygame version was used to build and test the game, or whether the current version in the developer's environment matches it.

**Quality goal damaged:** Learnability / Maintainability (goal 1), Correctness of the game rules (goal 2) if an old pygame bug matters

**Scenario:** The developer returns to this project in six months, having worked on other systems. They clone the repository and try to run `main.py` to make a change. pygame may or may not import, depending on what they have installed globally. If it does, they do not know if it is the same version the game was originally built with. If they change a rule and test it, they cannot know if a failure is their change or a version mismatch.

**Direction:** Create `requirements.txt` with explicit versions (e.g., `pygame==2.0.0`) pinning the dependencies to what the system was developed and tested with.

**Resolved by:** [ADR 0010](../decisions/0010-build-and-deployment-hygiene.md) — a pinned `requirements.txt`

---

## 9. No Test Seam

**What is wrong:** Every game rule is inline in the main event loop (lines 265–313). There is no function, no class, no way to exercise a rule in isolation. To test whether the raven moves correctly, you must run the game in a window, click the dice, and watch the screen. To test whether fruit is harvested, you must do the same. There is no programmatic access to the rules.

**Quality goal damaged:** Learnability / Maintainability (primary goal)

**Scenario:** You want to add a feature: "every fifth roll is a bonus roll, giving the player two turns." You modify the rule block and test manually by clicking 25 times. It looks right. You commit. Later, a player reports that the bonus does not work reliably. You cannot run a unit test to debug it. You must trace through the code and guess.

**Direction:** Follows from finding 1: extract a rules object with methods like `apply_roll(result, game_state)` that return a new state, testable without pygame.

**Resolved by:** [ADR 0008](../decisions/0008-pytest-test-seam-without-display.md) — pytest against `domain/`, no display required

---

## 10. Roughly 40 Lines of Duplicated Fallback Chains

**What is wrong:** The basket branch of the rule block (lines 276–313) contains four near-identical `if…elif…elif…elif` chains, one for each fruit type as the "preferred" stock. Each chain tries the preferred stock, then falls back to the other three in a fixed order. The code differs only in the order of the `if` branches. This is textbook duplication: four times the same logic, four times a place where a bug might hide, four times a place to change when the rule changes.

**Quality goal damaged:** Learnability / Maintainability (primary goal)

**Scenario:** You want to change the fallback order (e.g., "if the preferred fruit is empty, pick any non-empty fruit at random, not in a fixed order"). You edit the first chain. You edit the second. You edit the third. Halfway through the fourth, you make a typo. The code still runs (Python is forgiving). A player discovers it is broken.

**Direction:** Build a single loop over an ordered list of fruit stocks; on a basket roll, iterate the list until finding a non-empty stock, then pop from it.

**Resolved by:** [ADR 0006](../decisions/0006-basket-roll-becomes-player-choice.md) — the fallback chains are deleted, not refactored

---

## 11. Positional Coupling in World Construction

**What is wrong:** Objects are built in five near-identical `for i in range(0,4)` loops (lines 85–241), each containing an `if i == 0: … elif i == 1: … elif i == 2: … elif i == 3:` position table. The coordinates are embedded in the conditional branches. To change a position, you must find the correct `if i == N` branch and edit the coordinate expression. To add a new object, you must add a new loop and a new position table. This pattern does not scale and is error-prone.

**Quality goal damaged:** Learnability / Maintainability (goal 1)

**Scenario:** You want to move the first red apple from its current position. You find the `redAppleList` loop at lines 147–169. In the `if i == 0:` branch (line 149), the position is `posX = WINDOWWIDTH / 3` and `posY = 0`. You change it to `posX = WINDOWWIDTH / 3.2` to shift it slightly. A week later, you want to adjust all four red apples slightly to the right. You must edit the same `posX` expression in all four conditional branches—or risk getting out of sync. By the fourth branch, it is easy to miss one or make a typo. The error goes unnoticed until the apple appears in the wrong place during testing.

**Direction:** Move the coordinates into a data structure (a list of tuples or a list of dictionaries) and build the objects in one loop over that data.

**Resolved by:** [ADR 0007](../decisions/0007-layout-and-assets-as-data.md) — coordinates move into a data table

---

## 12. Per-Frame Disk I/O

**What is wrong:** The render pass (line 329) calls `pygame.image.load("pics/" + draftResult + ".png")` to load the image for the rolled result sprite, executing this 60 times per second. Similarly, the end-game sequence constructs a new `pygame.font.SysFont("comicsansms", 40)` object at lines 370 and 387, both inside the render loop, so the font is built 60 times per second. Both are wasteful—images and fonts should be loaded once at startup and cached.

**Quality goal damaged:** Learnability / Maintainability (goal 1), operational efficiency

**Scenario:** The author returns to modify the rendering logic months later. Profiling the code, they see 60 image loads and 60 font creations per second. They wonder why; tracing the code, they find these load calls scattered in the render pass. Removing them is straightforward, but they were never intended—they are residue of the immediate-mode rendering philosophy applied without optimization.

**Direction:** Load all images and fonts at startup; store them in module-level dictionaries; look them up in the render pass instead of loading from disk each frame.

**Resolved by:** [ADR 0007](../decisions/0007-layout-and-assets-as-data.md) — `AssetCache` loads images and fonts once at startup

---

## 13. Residue: Mixed Languages and Debug Output

**What is wrong:** The codebase is otherwise in English (function names, variable names, comments). The end-game screen, however, displays German strings: `"Verloren"` (lost, line 371) and `"Gewonnen"` (won, line 388). This is a mixed-language interface that is confusing and hard to maintain. Additionally, line 398 contains a leftover debug print: `print("Kleine Änderung")` ("Small change")—not used, not part of the game, a residue from development. The game does not offer a restart; after the end screen, the only option is to close the window and run the `.exe` again.

**Quality goal damaged:** Learnability / Maintainability (goal 1); Usability for a pre-school child (goal 3)

**Scenario:** A developer reads the code and assumes the game is fully English. They add a new message in English. The German strings confuse them. They ask if there is a plan to support multiple languages. There is not; the German is just left over.

**Direction:** Choose one language (English recommended, to match the codebase). Remove the debug print at line 398. Consider adding a restart button instead of forcing the player to close the window.

**Resolved by:** [ADR 0007](../decisions/0007-layout-and-assets-as-data.md) — cleaned up when the presentation layer is rewritten (see the migration roadmap, step 3)
