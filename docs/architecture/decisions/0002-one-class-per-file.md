# 0002. One class per file, mirroring the inheritance hierarchy

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

Once `domain/` exists (ADR-0001) its internal file layout must be decided. Today all four sprite classes live together in main.py. In Python the conventional unit of encapsulation is the *module*, not the file — a domain of this size would idiomatically be one `domain.py` or two or three cohesive modules. The competing consideration is that the primary quality goal of this project is learnability for its own author.

## Decision Drivers

- Quality goal 1: the code is a teaching artefact for its author's future self.
- Discoverability: the developer should be able to see the model without reading code.
- Against: Python convention, import verbosity, many very small files.

## Considered Options

- One class per file, file name = snake_case of the class name.
- One `domain.py` holding the whole model — idiomatic Python.
- Grouping by concept: `fruit.py` (all fruit classes), `board.py` (Tree, Orchard), `play.py` (Dice, Game).

## Decision Outcome

Chosen option: "One class per file, file name = snake_case of the class name", because it makes the model legible from the file tree alone, before any code is read, which optimises for the learnability goal that outranks Python idiom here.

`domain/fruit.py` holds the abstract base class `Fruit`; `domain/red_apple.py`, `domain/green_apple.py`, `domain/plum.py`, `domain/pear.py` each hold one subclass. The inheritance hierarchy becomes visible in the directory listing. This is a deliberate departure from Python convention, chosen explicitly because quality goal 1 outranks idiom here, not out of ignorance of the idiom.

Apply the same principle to `presentation/`. Enums (`DieFace`, `GameStatus`) each get their own file for the same reason.

Rejected option 2: idiomatic, but the model stays invisible until the file is opened — it optimises for the experienced Python reader, not for the learner this project serves. Rejected option 3: a middle ground that would need a rule for which concept a class belongs to, and that rule would itself need explaining.

### Positive Consequences

- The model is legible from the file tree.
- Each file is small enough to read at a glance.
- Adding a fruit sort is a new file, obviously parallel to the existing ones.

### Negative Consequences

- Unidiomatic for Python and will surprise experienced Python readers.
- Roughly 13 small files under `domain/`.
- More import lines.

## More Information

Related: [ADR-0001](0001-separate-domain-model-from-presentation.md), [ADR-0003](0003-tree-as-fruit-owning-aggregate.md).
