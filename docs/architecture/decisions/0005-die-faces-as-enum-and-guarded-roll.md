# 0005. Die faces as an enum and guarded roll

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

Two problems stem from a single cause: `Dice.rollDice()` returns a bare string — "red", "green", "yellow", "blue", "raven", "basket". This string is compared by equality throughout the rule block and is also concatenated into a file path during rendering: `pygame.image.load("pics/" + draftResult + ".png")`. A typo in a comparison is silent; the set of legal values is written down nowhere.

The dominant correctness defect: the module-level variable `draftResult` holds the last roll and is never reset. The rule block sits inside the `MOUSEBUTTONDOWN` branch at the same indentation level as the hit test. The rules therefore run on every mouse press, not only on a successful die hit, and they re-apply the stale value of `draftResult`. Consequence: after a single roll of "red", clicking anywhere in the window four times empties the red apple tree. After a single roll of "raven", clicking five times loses the game. The player never needs to roll the die again.

The initial value `"none"` is not a sentinel — it is the name of a real asset (pics/none.png, a blank display image). The string does double duty as rule token, asset name, and null marker.

## Decision Drivers

* Quality goal 2 (correctness) — the defect makes the game trivially cheatable
* Quality goal 1 (learnability) — a one-line guard would fix the symptom while leaving the problematic design intact
* Resetting `draftResult` after use is a patch; the structure should make the fault impossible

## Considered Options

* Make `DieFace` an enum and route every state change through `Game.roll()`, which is called only on a die hit; keep the displayed value separate from the rule trigger
* Reset `draftResult = "none"` after the rule block runs
* Move the rule block inside the `if dice.overDice(...)` branch

## Decision Outcome

Chosen option: "Make `DieFace` an enum and guard state changes through `Game.roll()`", because this prevents the fault structurally rather than patching symptoms.

* `domain/die_face.py`: `class DieFace(Enum): RED, GREEN, YELLOW, BLUE, RAVEN, BASKET`. The legal values now exist as a declaration. The asset name is derived from the face by the presentation layer, not by string concatenation in the domain.
* `domain/dice.py`: `Dice.roll(rng: random.Random) -> DieFace` — the random source is injected, making the die testable (see [ADR-0008](0008-pytest-test-seam-without-display.md)).
* `domain/game.py`: `Game.roll(rng)` is the only method that mutates game state. `app.py` calls it only when the click actually hits the die. `Game.last_face -> DieFace | None` is a pure display value that never triggers a rule — the two roles the old `draftResult` conflated are now two separate members with different jobs.

The rejected options work as one-line fixes but neither prevents the next variant of the same fault, because both leave the rules inline in the event handler where indentation is load-bearing. This project's first quality goal is learnability; the lesson worth keeping is that state changes belong behind a method, not at an indentation level.

### Positive Consequences

* The defect becomes structurally impossible rather than fixed
* The set of die faces is declared once
* Typos in face comparison become `AttributeError` instead of silent no-ops
* The die is testable with a seeded RNG

### Negative Consequences

* The presentation layer needs a mapping from `DieFace` to asset name
* `None` must be handled where `"none"` used to be a convenient blank image

## More Information

Resolves chapter 11 findings 2 and the "rule block runs on every mouse button event" observation in chapter 6. Related: [0001](0001-separate-domain-model-from-presentation.md), [0006](0006-basket-roll-becomes-player-choice.md), [0008](0008-pytest-test-seam-without-display.md).
