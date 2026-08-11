# 0006. Basket roll becomes player choice

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

In the physical Obstgarten, rolling the basket lets the player choose which fruit to take — for many children it is the best moment of the game. The digital version instead picks for them: `random.randint(1,4)` selects a "preferred" fruit stock, and if that stock is empty it falls through to the others in a fixed order. The rule is implemented as four near-identical `if/elif/elif/elif` chains that differ only in the order of their branches — the same logic written four times, four places for a bug to hide.

This implementation choice damages two things simultaneously: quality goal 2, because the game no longer behaves like the board game, and quality goal 1, through 44 lines of duplication that obscure the actual rule.

## Decision Drivers

* Quality goal 2 is explicit on this point; arc42 chapter 1 names it as the scenario for the goal: "Rolling the basket results in the player choosing which fruit to take, not a random selection."
* Quality goal 3 (usability for a pre-school child): choosing is a click on a big colourful tree — well within reach of a four-year-old, and more engaging than watching the game decide
* The duplication disappears as a side effect of introducing proper state

## Considered Options

* Introduce a waiting state: on a basket roll the game asks the player to click a tree
* Keep the random pick but collapse the four chains into one loop over an ordered list of stocks
* Keep the random pick and leave the code as it is

## Decision Outcome

Chosen option: "Introduce a waiting state for player fruit choice", because this matches the physical game and eliminates duplication.

* `domain/game_status.py`: `class GameStatus(Enum): RUNNING, AWAITING_FRUIT_CHOICE, WON, LOST`
* `Game.roll()` on `DieFace.BASKET` sets the status to `AWAITING_FRUIT_CHOICE` instead of harvesting
* `Game.choose(tree: Tree)` is valid only in that status; it harvests one fruit from the chosen tree into the basket and returns the status to `RUNNING`. Choosing an empty tree is rejected and the game keeps waiting
* The view makes trees clickable while the status is `AWAITING_FRUIT_CHOICE` and signals that the game is waiting (for a non-reading player this must be visual — for example highlighting the trees that still bear fruit)
* Edge case: if the orchard is empty the game is already won, so the waiting state cannot be entered with nothing to choose

The rejected options either keep the wrong rule (violating quality goal 2) or leave the duplication problem.

### Positive Consequences

* The digital game matches the physical one at its most memorable moment
* 44 lines of duplicated fallback chains are deleted, not refactored
* The game gains an explicit state machine, which is also what a later restart or menu will need

### Negative Consequences

* The input model grows — the view now has two click targets (die and trees), and must show which one is live
* A new failure mode to handle: the click that lands on nothing while the game waits

## More Information

Resolves chapter 11 findings 3 and 10 together. Depends on the waiting state being visible to a pre-school player. Related: [0003](0003-tree-as-fruit-owning-aggregate.md), [0005](0005-die-faces-as-enum-and-guarded-roll.md).
