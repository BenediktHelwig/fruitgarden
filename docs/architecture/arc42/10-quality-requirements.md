# 10. Quality Requirements

## Quality Tree

```
Fruit Garden
├─ 1. Learnability / Maintainability
│  ├─ Modifiability
│  ├─ Testability
│  └─ Analysability
├─ 2. Correctness of the Game Rules
│  ├─ Rule Fidelity to Physical Game
│  └─ Deterministic Behaviour
└─ 3. Usability for a Pre-school Child
   ├─ Operability Without Reading
   ├─ Single Obvious Click Target
   └─ No Unexplained UI Elements
```

## Evaluation Scenarios

| ID | Quality Goal | Stimulus | Expected Response | Addressed By |
|---|---|---|---|---|
| **Q1.1** | Learnability / Maintainability | A rule changes: the raven advances only every second raven roll, not every one. | The change is made in `domain/game.py` alone; no presentation file is touched. A pytest test proves the new rule works without opening a window. | [ADR-0001](../decisions/0001-separate-domain-model-from-presentation.md), [ADR-0004](../decisions/0004-raven-progress-as-step-count.md), [ADR-0008](../decisions/0008-pytest-test-seam-without-display.md) |
| **Q1.2** | Learnability / Maintainability | A fifth fruit sort is added to the game. | One new file under `domain/` (a new subclass of `Fruit`), one new row in the layout table (data), one new PNG file in `pics/`; no existing rule code changes. | [ADR-0002](../decisions/0002-one-class-per-file.md), [ADR-0003](../decisions/0003-tree-as-fruit-owning-aggregate.md), [ADR-0007](../decisions/0007-layout-and-assets-as-data.md) |
| **Q1.3** | Learnability / Maintainability | A developer returning after six months wants to know how much fruit remains in the orchard. | They can ask `orchard.remaining` (or similar query) directly, rather than counting four lists and summing the results. The API is discoverable and named. | [ADR-0003](../decisions/0003-tree-as-fruit-owning-aggregate.md) |
| **Q1.4** | Learnability / Maintainability | A rule is changed and the developer wants to know whether anything broke, without playing the game. | `pytest` runs in seconds without opening a window, executing all domain rules against known inputs, and reports pass/fail. | [ADR-0008](../decisions/0008-pytest-test-seam-without-display.md) |
| **Q2.1** | Correctness of the Game Rules | The player rolls the basket. | The game waits (does not auto-apply a rule). The trees bearing fruit become clickable (visual feedback). The player's click on a tree determines which fruit is harvested — exactly as in the physical *Obstgarten*. | [ADR-0006](../decisions/0006-basket-roll-becomes-player-choice.md) |
| **Q2.2** | Correctness of the Game Rules | The player rolls once, then clicks the mouse button repeatedly anywhere in the window without rolling the die again. | Nothing happens; the roll is not applied a second time. Game state changes only when a click confirms a hit on the die. (Today this is the dominant defect; chapter 11 finding 2.) | [ADR-0005](../decisions/0005-die-faces-as-enum-and-guarded-roll.md) |
| **Q2.3** | Correctness of the Game Rules | The window size is changed or the game is run on a display with different resolution. | The number of raven steps to the orchard remains five; the difficulty of the game is independent of geometry. | [ADR-0004](../decisions/0004-raven-progress-as-step-count.md) |
| **Q3.1** | Usability for a Pre-school Child | A four-year-old starts the packaged game by double-clicking `main.exe` on their Desktop. | The game window opens. No console window appears. No missing-asset crash occurs. The game is ready to play. | [ADR-0010](../decisions/0010-build-and-deployment-hygiene.md) |
| **Q3.2** | Usability for a Pre-school Child | The game is waiting for a fruit choice after a basket roll. | Which trees can be clicked is visible without reading any text — via visual feedback such as highlighting, cursor change, or proximity to the mouse. | [ADR-0006](../decisions/0006-basket-roll-becomes-player-choice.md) |

## Note on Trade-offs

Quality goal 1 (Learnability / Maintainability) was ranked first and is the primary driver of the architecture. [ADR-0002](../decisions/0002-one-class-per-file.md) (one class per file) follows that ranking against Python convention and idiom. The cost is a file count unusual for a project this size: approximately 15–20 files in `domain/` and `presentation/` compared to the current single `main.py`. This cost is accepted deliberately because the learning benefit outweighs the overhead for a practice project where the author is the sole developer and the code is the artefact being learned from.
