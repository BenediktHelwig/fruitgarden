# 0003. Tree as the fruit-owning aggregate, Basket owning harvested fruit

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

The core state of the game — how much fruit remains — currently lives in four module-level lists with no owner and no name. Nothing can be asked "how many apples are left?". Trees exist only as decoration: they are `Fruit("tree", ...)` instances, pure pictures with no behaviour. The basket likewise is a picture; harvested fruit is simply discarded by `list.pop()` and ceases to exist. The 2021 class diagram had already specified the alternative — a `Tree` owning `amount` with `decrement()` and `emptyTree()`, and a `Basket` with `amount` — and the author abandoned it with the note "Tree eventuell löschen" ("possibly delete Tree"). This abandonment is the root of most of the technical debt recorded in arc42 chapter 11.

## Decision Drivers

- Quality goal 1: state needs an owner with a name.
- Quality goal 2: the domain language of the real board game is trees, fruit, a basket and a raven; the model should speak it.
- The 2021 design was already right; the reasons for abandoning it were never recorded.

## Considered Options

- `Tree` owns its fruit, `Orchard` owns the four trees, `Basket` owns harvested fruit.
- `Orchard` owns the fruit directly, keyed by sort; no `Tree` in the domain, trees stay decoration.
- Keep the four lists but move them into a `GameState` container.

## Decision Outcome

Chosen option: "`Tree` owns its fruit, `Orchard` owns the four trees, `Basket` owns harvested fruit", because it revives the 2021 design that was already sound, puts a name to the core state, and makes the model speak the language of the board game instead of the language of lists.

Concrete interfaces:

- `Tree.__init__(fruits: list[Fruit])`, `remaining -> int`, `is_empty() -> bool`, `bears(face: DieFace) -> bool`, `pick() -> Fruit | None`
- `Orchard.__init__(trees: list[Tree])`, `is_empty() -> bool`, `tree_bearing(face) -> Tree | None`, `trees_with_fruit() -> list[Tree]`
- `Basket.add(fruit: Fruit)`, `contents -> tuple[Fruit, ...]`

Harvesting becomes: take a fruit from a tree, put it in the basket — exactly what the child does at the table. Winning becomes `orchard.is_empty()` instead of four separate emptiness checks.

Rejected option 2: flatter, but the tree — the most concrete object on the physical board — would have no representation in the model of the game. Rejected option 3: a container without behaviour is still four lists; it renames the problem.

### Positive Consequences

- One place answers "how much is left?".
- The model speaks the language of the board game.
- Giving the basket real contents makes a harvest observable and later displayable, and makes a move reversible in principle.

### Negative Consequences

- More objects than lists.
- The basket holds fruit that nothing currently displays — a small amount of state without a present consumer.

## More Information

Revives the design of `diagramm/Class.drawio` (October 2021). Resolves chapter 11 finding 1 in part. Related: [ADR-0001](0001-separate-domain-model-from-presentation.md), [ADR-0002](0002-one-class-per-file.md), [ADR-0006](0006-basket-roll-becomes-player-choice.md).
