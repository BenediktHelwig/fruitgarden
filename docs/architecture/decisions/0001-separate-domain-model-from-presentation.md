# 0001. Separate the domain model from the presentation layer

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

The render model IS the domain model. There is no boundary between how the game is drawn and what the game is. Concretely: the amount of fruit remaining is the length of four module-level Python lists (`redAppleList`, `greenAppleList`, `plumList`, `pearList`, built at main.py:147-241) — fruit is drawn by iterating those lists, so the lists became the storage. The raven's progress towards the orchard is a pixel coordinate, `raven.picPosX`. The win condition is `not redAppleList and not greenAppleList and not plumList and not pearList` (main.py:321). The loss condition is `raven.picPosX > ((WINDOWWIDTH/10) + (WINDOWWIDTH/2))` (main.py:317). Every game rule sits inline in the mouse-event branch of the game loop (main.py:265-313).

Consequences today: no object can be asked for the state of the game; no rule can be exercised without opening a window and clicking; a rule change means finding every place where rendering and state-checking are interleaved.

## Decision Drivers

- Quality goal 1 (Learnability/Maintainability) is the primary goal and is the one most damaged.
- Chapter 11 findings 1 and 9 both trace to this single property.
- The author wants to learn software design; the layered separation is the lesson the codebase currently cannot teach.

## Considered Options

- Extract a `domain/` package that never imports pygame, with `presentation/` reading it as a view.
- Keep the single file and merely tidy it — fix bugs, remove duplication, keep state in module-level lists.
- Full rewrite on pygame.sprite.Group with a scene/state machine.

## Decision Outcome

Chosen option: "Extract a `domain/` package that never imports pygame, with `presentation/` reading it as a view", because it teaches the design pattern that is the primary learning goal, keeps the existing working code as a learning artefact, and makes the rules testable without a display.

Introduce two packages with a strictly directed dependency:

- `domain/` — plain Python, models the game of Obstgarten: Fruit, Tree, Orchard, Raven, Basket, Dice, DieFace, GameStatus, Game. It contains the rules and the state.
- `presentation/` — pygame lives here and nowhere else: AssetCache, Sprite, Layout, BoardView, EndView.
- `app.py` — composes both and holds the loop.

The load-bearing invariant, stated as one rule: **no file under `domain/` may import pygame.** It is machine-checkable (walk the AST of every file under `domain/`, fail on an `import pygame`) and that check belongs in the test suite.

Rejected option 2 because it leaves the rules untestable and the state ownerless — the root cause survives. Rejected option 3 because it discards the existing code and with it the learning artefact, at high risk, for a game that works today.

### Positive Consequences

- Rules become testable without a display.
- "Is the game won?" becomes `orchard.is_empty()`.
- A rule change is local to `domain/`.
- The dependency direction is explicit and enforceable.

### Negative Consequences

- More files and one indirection more than a 398-line script.
- The developer must maintain the discipline of the layer rule.
- A one-off migration cost.

## More Information

Resolves chapter 11 findings 1 and 9. Prerequisite for ADR-0003, ADR-0005, ADR-0006, ADR-0008. Related: [ADR-0002](0002-one-class-per-file.md), [ADR-0003](0003-tree-as-fruit-owning-aggregate.md), [ADR-0008](0008-pytest-test-seam-without-display.md).
