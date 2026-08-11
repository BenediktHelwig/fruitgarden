# 0008. pytest test seam without display

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

There is no way to exercise a rule of this game except by running it. Every rule is inline in the mouse-event branch of the game loop; there is no function to call and no object to inspect. Verifying that the raven moves correctly means opening a window, clicking a die until the raven face comes up, and watching. Verifying the win condition means playing to the end. `random.randint` is called directly inside `rollDice()`, so even the die cannot be driven to a known outcome.

The repository has no tests, no test dependency and no test directory. The practical consequence: a change to a rule can only be checked by the change's author, by hand, once. A regression introduced today is found by the four-year-old playing the game.

## Decision Drivers

* Quality goal 1 (learnability and maintainability) is the primary goal, and "can I still run this after I change it" is the core of maintainability
* Quality goal 2 (correctness): the rules are exactly what must not silently break
* The separation in [0001] makes this cheap — a pygame-free domain needs no display to test

## Considered Options

* pytest against `domain/` only, with the random source injected; no display required
* End-to-end tests driving pygame with a dummy video driver (SDL_VIDEODRIVER=dummy) and synthetic events
* No automated tests; continue manual verification

## Decision Outcome

Chosen option: "pytest against domain only with injected random source", because it is the cheapest, fastest, and tests what matters most — the rules.

Create `tests/` and add a pinned `pytest` dependency. The tests cover the rules and nothing else:

* `Dice.roll(rng)` takes an injected `random.Random`, so a seeded instance yields a known sequence of faces and every rule can be driven deterministically
* Harvest: rolling a colour removes one fruit from the matching tree and adds it to the basket; rolling a colour whose tree is empty changes nothing
* Raven: five `move_forward()` calls reach the orchard, four do not (see [0004])
* Win: emptying the last tree sets `GameStatus.WON`. Loss: the raven arriving sets `LOST`
* Basket choice (see [0006]): a basket roll enters `AWAITING_FRUIT_CHOICE`; `choose()` on a bearing tree harvests and returns to `RUNNING`; `choose()` on an empty tree is rejected
* The layer rule itself: a test walks the AST of every file under `domain/` and fails if any of them imports pygame. This is what keeps [0001] true over time rather than merely intended

Rejected option 2: valuable later for the input layer, but it tests the thing least likely to break through a driver that is itself a source of failures. Rejected option 3: this is the status quo, and it is the reason a rule change cannot be made with confidence.

### Positive Consequences

* A rule change is verifiable in a second, without a window
* The layer separation is enforced by a machine rather than by discipline
* The tests document the rules of the game in executable form — which serves the learning purpose of the project directly

### Negative Consequences

* A test dependency and a test suite to maintain
* The presentation layer stays untested by this decision, so rendering and hit-testing defects still surface only by playing

## More Information

Follows from [0001] and is the reason the injected RNG in [0005] is worth the small extra parameter. Related: [0001](0001-separate-domain-model-from-presentation.md), [0004](0004-raven-progress-as-step-count.md), [0005](0005-die-faces-as-enum-and-guarded-roll.md), [0006](0006-basket-roll-becomes-player-choice.md).
