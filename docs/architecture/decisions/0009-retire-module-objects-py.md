# 0009. Retire module/objects.py

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

`module/objects.py` is not imported by any file in the repository. It is a 57-line sketch of a domain model from an earlier attempt — classes `Element`, `Tree`, `Fruit`, `Raven`, `Basket`, `Dice`, several with `pass` bodies and German comments ("Liste plus eins", "Inhalt anzeigen"). It does not work: `Tree.__init__` calls `super.__init__(self, name)`, using the builtin `super` as if it were an object, which raises AttributeError on construction; `Element.getPicture()` blits to an undefined global `screen`; `Dice.__init__` assigns its six faces to local variables that are discarded when the constructor returns. Its `Dice.rollTheDice()` returns `random.randint(0,5)` — a number, where the running game uses names.

The file is a fossil: the same idea as the 2021 class diagram, in code, abandoned earlier and further along. A reader finding it cannot tell whether it is dead or merely unfinished, and running it only produces an error.

## Decision Drivers

- Quality goal 1 (Learnability / Maintainability): an orphaned, broken file in a small teaching repository costs more attention than it is worth.
- Its purpose — a domain model that owns the rules — is exactly what [ADR-0001](0001-separate-domain-model-from-presentation.md) and ADR-0003 now deliver properly.
- Deleted code is recoverable from git history; this is not a loss.

## Considered Options

- Option 1: Delete `module/objects.py` (and the now-empty `module/` package) once `domain/` exists.
- Option 2: Repair it and promote it into the real domain module.
- Option 3: Leave it and add a comment marking it as dead.

## Decision Outcome

Chosen option: "Option 1, sequenced after `domain/` is in place", because the file's intent is not being discarded — it is being fulfilled. `Tree` finally owns its fruit, `Basket` finally has contents, the die finally returns named faces. Delete it once `domain/` provides all of that, not before, so the record shows the replacement rather than a removal.

Rejected option 2: repairing it means rewriting every class in it, against a design ([ADR-0001](0001-separate-domain-model-from-presentation.md), ADR-0003) it does not share — it would be a new file wearing an old name.

Rejected option 3: a comment saying "this is dead" is a file that still has to be read to learn it need not be read.

### Positive Consequences

- The repository stops containing two competing, incompatible sketches of the same model.
- Nothing in the tree is broken-on-purpose any more.

### Negative Consequences

- A historical record of the author's earlier thinking leaves the working tree — mitigated by git history and by this record naming what the file contained and why it did not survive.

## More Information

Resolves chapter 11 finding 4. Sequenced after [ADR-0001](0001-separate-domain-model-from-presentation.md). Related: [ADR-0001](0001-separate-domain-model-from-presentation.md).
