# 0004. Raven progress as an explicit step count

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

The raven's progress is stored as a pixel coordinate. It starts at `ravenPosStart = 10`, `moveForward()` adds 130 pixels (main.py:47), and the loss threshold is `raven.picPosX > (WINDOWWIDTH/10 + WINDOWWIDTH/2)` = 648 pixels (main.py:317). The sequence is 10 → 140 → 270 → 400 → 530 → 660, so the game is lost after exactly five raven rolls. **That number appears nowhere in the source.** It is an emergent property of the window width, the tile width and the raven's starting offset. Changing the window size, the sprite size or the start position silently changes the difficulty of the game.

## Decision Drivers

- Quality goal 1: a game rule must be readable as a rule, not derived from geometry.
- Quality goal 2: the number of raven steps is a rule of Obstgarten (the physical game has a fixed path length); it must not depend on the window.
- Follows from ADR-0001: the domain must not know about pixels.

## Considered Options

- `Raven` holds `steps_taken: int` and a named constant `STEPS_TO_ORCHARD = 5`; presentation derives the pixel position.
- Keep the pixel coordinate but extract the threshold into a named constant.
- Model the path as a list of tiles the raven occupies.

## Decision Outcome

Chosen option: "`Raven` holds `steps_taken: int` and a named constant `STEPS_TO_ORCHARD = 5`; presentation derives the pixel position", because it makes the rule explicit in code and places it where it belongs — in the domain — and separates the game rule from the display geometry.

`Raven.move_forward()` increments an integer; `Raven.has_reached_orchard()` is `steps_taken >= STEPS_TO_ORCHARD`. The view computes `x = start_x + steps_taken * TILE_WIDTH` when drawing. The difficulty of the game is now a declared number that a maintainer can change on purpose.

Rejected option 2: better than today, but the domain would still measure a rule in pixels and still could not be tested without a display. Rejected option 3: correct but heavier than the game needs — five identical tiles carry no information a counter does not.

### Positive Consequences

- The rule "five raven rolls and you lose" is stated once, in one place, in words.
- Window and sprite sizes become free to change.
- The raven is unit-testable.

### Negative Consequences

- The view now needs the layout constant that used to be implicit in the sprite position.

## More Information

The five steps match the five path tiles drawn on the board (four `field` sprites plus the `gate`). Resolves the "loss condition is implicit in geometry" observation of arc42 chapter 6. Related: [ADR-0001](0001-separate-domain-model-from-presentation.md), [ADR-0005](0005-die-faces-as-enum-and-guarded-roll.md).
