# 8. Cross-cutting Concepts

This chapter describes the concepts that apply to the target architecture of Fruit Garden, as proposed in the eleven architecture decisions. The concepts are not yet implemented; they describe the system as planned.

## The Layer Rule

The load-bearing invariant of the target architecture: **no file under `domain/` may import pygame.** Everything else follows from it.

The dependency direction is one-way:

```
input → domain → state → presentation
```

The `domain/` package contains plain Python models and rules with no pygame dependencies. The `presentation/` package contains all pygame code and reads the domain as a view. The `app.py` module composes both and holds the game loop. The direction is machine-checkable: a test walks the abstract syntax tree of every file under `domain/` and fails if it encounters `import pygame`.

This separation makes rules testable without opening a window and forces all rendering concerns away from the decision logic.

![Target Building Block View](../diagrams/target-building-blocks.drawio)

The diagram shows the three layers, the one-way dependency from input through domain and state to presentation, and the external `pics/` and pygame/SDL2 dependencies of the presentation layer.

**Reference:** [ADR-0001: Separate the domain model from the presentation layer](../decisions/0001-separate-domain-model-from-presentation.md), enforced by [ADR-0008: A pytest test seam that runs without a display](../decisions/0008-pytest-test-seam-without-display.md).

## One Class Per File

File name is the snake_case of the class name; the inheritance hierarchy is visible in the directory listing.

For example: `domain/fruit.py` contains class `Fruit`; `domain/red_apple.py` contains class `RedApple(Fruit)`; `domain/tree.py` contains class `Tree`. This is a deliberate departure from Python convention, chosen because learnability is the first ranked quality goal. When a developer returns to the code after months away, the file structure tells them what exists without reading imports.

![Target Class Model](../diagrams/target-class-model.drawio)

The class model of the target domain: one box per class and therefore one box per file, with `Fruit` abstract and `RedApple`, `GreenApple`, `Plum` and `Pear` inheriting from it.

**Reference:** [ADR-0002: One class per file, mirroring the inheritance hierarchy](../decisions/0002-one-class-per-file.md).

## The Asset Naming Contract

Every visual element name maps directly to `pics/<name>.png`. This contract the current codebase has always relied on implicitly (today via `"pics/" + name + ".png"` at main.py:32).

In the target design, the domain layer carries the asset name as a simple string attribute. For example: `Fruit.asset_name = "redApple"`. The presentation layer then resolves this to a file path: `AssetCache.load("redApple")` → `pics/redApple.png`.

The 15 existing PNG file names are the vocabulary of the system: `basket`, `blue`, `dice`, `field`, `gate`, `green`, `greenApple`, `none`, `pear`, `plum`, `raven`, `red`, `redApple`, `tree`, `yellow`. Note that `none.png` is a blank display image (used when no roll result is ready to show), not a sentinel value or error state.

**Reference:** [ADR-0007: Layout coordinates and assets as data, loaded once](../decisions/0007-layout-and-assets-as-data.md).

## Asset Lifetime and the Display-First Ordering

All images and fonts are loaded once, after the display exists, and served from `AssetCache`. This makes explicit a coupling that today is invisible and fragile: the `.convert_alpha()` method requires an initialised pygame display, so `pygame.display.set_mode(...)` at main.py:25 must run before any element is constructed. This is an ordering constraint that lives only in the developer's head.

Today's implementation loads images per-frame in the render pass (main.py:329: `pygame.image.load(...)` 60 times per second) and constructs fonts per-frame in the end sequence (main.py:370, 387: `pygame.font.SysFont(...)` 60 times per second). The target design replaces both with a named initialisation step: `AssetCache.load_all()` runs once before the game starts, returning a cache that the presentation layer reads from.

**Reference:** [ADR-0007: Layout coordinates and assets as data, loaded once](../decisions/0007-layout-and-assets-as-data.md).

## Layout As Data

Coordinates live in a table, not in conditional branches. Today, world construction uses five near-identical `for i in range(0,4)` loops, each containing an `if i == 0: … if i == 1: … if i == 2: … if i == 3:` block with position values (main.py:85–241). The target design moves this into a data structure: a list of tuples or dictionaries with position values. One loop then builds sprites from the table.

For example:
```python
LAYOUT = [
  {"name": "redApple", "tree": 0, "x": 100, "y": 200},
  {"name": "redApple", "tree": 0, "x": 150, "y": 200},
  # ... more entries
]

for entry in LAYOUT:
    sprite = Sprite(entry["name"], entry["x"], entry["y"])
```

This eliminates positional coupling and makes adding or moving visual elements a data change, not a code change.

**Reference:** [ADR-0007: Layout coordinates and assets as data, loaded once](../decisions/0007-layout-and-assets-as-data.md).

## Game State and the State Machine

`GameStatus` has four values: `RUNNING`, `AWAITING_FRUIT_CHOICE`, `WON`, `LOST`. The only method that mutates state is `Game.roll()`, and it is called only when a confirmed die hit occurs. `Game.last_face` is a display value that captures which face was rolled most recently; it is read by the presentation layer but never triggers a rule.

This separation of the two roles — state change and display information — makes the stale-roll defect of chapter 11 finding 2 structurally impossible. The stale roll occurs today because `draftResult` persists and the rule block runs on every mouse click, not just on die hits. In the target design, the rule block is guarded: the click must hit the die before `Game.roll()` is called. Once called, it consumes the roll and changes state atomically.

![Target Runtime: One Turn](../diagrams/target-runtime-dice-roll.drawio)

One full turn in the target design, including the basket branch in which the game waits for the player to choose a tree, and the case of a click that hits nothing — which in the current system is the one that re-applies the previous roll.

**Reference:** [ADR-0005: Die faces as an enum; rolls applied through a guarded game state](../decisions/0005-die-faces-as-enum-and-guarded-roll.md) and [ADR-0006: The basket roll becomes a player choice](../decisions/0006-basket-roll-becomes-player-choice.md).

## Rules in Domain Units, Never Pixels

The raven counts steps (`STEPS_TO_ORCHARD = 5`), it does not accumulate pixels. When the view renders the raven, it derives the pixel position from the step count. The orchard is won or lost when `raven.steps >= STEPS_TO_ORCHARD`, not when `pixel_x > 648`.

Today, the five steps are an emergent property of the window geometry: the raven starts at pixel 10 and moves +130 pixels per roll, so after five raven rolls it reaches pixel 660, which crosses the threshold 648 (main.py:317). This number is never declared in the code; it is buried in the loss check. Changes to window geometry silently change the difficulty of the game.

**Reference:** [ADR-0004: Raven progress as an explicit step count](../decisions/0004-raven-progress-as-step-count.md).

## Test Strategy

pytest runs against `domain/` only; no display is required. The random source is injected into `Dice.roll(rng)` so that rolls are deterministic and testable with exact sequences (roll red, roll basket, roll raven, etc.). The layer rule itself is a test: an AST walk that fails if `domain/` imports pygame.

What is deliberately not covered: rendering and hit testing. The presentation layer is not tested automatically; it is verified by human play.

**Reference:** [ADR-0008: A pytest test seam that runs without a display](../decisions/0008-pytest-test-seam-without-display.md).

## Language

All code, identifiers, documentation and user-facing text are in English. Today the codebase is mostly English, but the end screen shows German text: `"Verloren"` (lost) and `"Gewonnen"` (won) at main.py:371 and 388. Additionally, line 398 contains a debug print in German: `"Kleine Änderung"` ("Small change"), not part of the game and never used. The target design removes both, choosing English throughout.

**Reference:** Chapter 11, finding 13.

## Diagrams in This Chapter

| Diagram | Shows | Decided by |
| --- | --- | --- |
| Target Building Block View | The three layers and their one-way dependencies, with external dependencies of the presentation layer | [ADR-0001: Separate the domain model from the presentation layer](../decisions/0001-separate-domain-model-from-presentation.md) |
| Target Class Model | Domain classes: abstract `Fruit` base class with concrete subclasses `RedApple`, `GreenApple`, `Plum`, `Pear` | [ADR-0002: One class per file, mirroring the inheritance hierarchy](../decisions/0002-one-class-per-file.md) |
| Target Runtime: One Turn | Full game turn including basket interaction, tree selection, and miss handling | [ADR-0005: Die faces as an enum; rolls applied through a guarded game state](../decisions/0005-die-faces-as-enum-and-guarded-roll.md) and [ADR-0006: The basket roll becomes a player choice](../decisions/0006-basket-roll-becomes-player-choice.md) |

The diagrams in this chapter document the proposed target architecture and are not yet implemented. Diagrams referenced in chapters 3, 5, 6 and 7 document the system as it exists today.
