# 9. Architecture Decisions

Architecture decisions are recorded in the `docs/architecture/decisions/` directory using the MADR (Markdown Architecture Decision Record) format. Every record currently has status `proposed` — the decisions describe the target architecture, not the system as built.

| ADR | Title | Status | Decides |
|---|---|---|---|
| [0001](../decisions/0001-separate-domain-model-from-presentation.md) | Separate the domain model from the presentation layer | proposed | Domain code never imports pygame; dependency flows one way: input → domain → state → presentation. |
| [0002](../decisions/0002-one-class-per-file.md) | One class per file, mirroring the inheritance hierarchy | proposed | File names are snake_case class names; inheritance is visible in the directory structure (Python idiom overridden for learnability). |
| [0003](../decisions/0003-tree-as-fruit-owning-aggregate.md) | Tree as the fruit-owning aggregate, Basket owning harvested fruit | proposed | Revive the 2021 design: Tree owns fruit list, Orchard owns trees, Basket holds harvested fruit; "is it won?" becomes `orchard.is_empty()`. |
| [0004](../decisions/0004-raven-progress-as-step-count.md) | Raven progress as an explicit step count | proposed | Five steps declared and named; raven moves in game units, not pixels; render derives pixel position from steps. |
| [0005](../decisions/0005-die-faces-as-enum-and-guarded-roll.md) | Die faces as an enum; rolls applied through a guarded game state | proposed | DieFace enum; rolls change state only when die hit is confirmed; stale-roll defect becomes structurally impossible. |
| [0006](../decisions/0006-basket-roll-becomes-player-choice.md) | The basket roll becomes a player choice | proposed | On basket roll, trees bearing fruit become clickable; player's click determines which fruit is harvested (not random fallback chains). |
| [0007](../decisions/0007-layout-and-assets-as-data.md) | Layout coordinates and assets as data, loaded once | proposed | Coordinates live in tables, not conditional branches; images loaded once at startup and cached; eliminates per-frame disk I/O. |
| [0008](../decisions/0008-pytest-test-seam-without-display.md) | A pytest test seam that runs without a display | proposed | Rules testable via pytest against domain layer; no pygame required; random source injected for determinism. |
| [0009](../decisions/0009-retire-module-objects-py.md) | Retire module/objects.py | proposed | Delete orphaned broken sketch; ADR 0001 and 0003 fulfil its purpose (abandoned 2021 domain model attempt). |
| [0010](../decisions/0010-build-and-deployment-hygiene.md) | Build and deployment hygiene | proposed | Bundle pics/ in PyInstaller output; ignore build artefacts in git; pin dependencies; hide console window on Windows. |
| [0011](../decisions/0011-long-lived-architecture-documentation-branch.md) | A long-lived architecture documentation branch | proposed | Architecture records and diagrams live on a documentation branch that is merged to main as the design is implemented. |

## Reading Order

Start with [ADR-0001](../decisions/0001-separate-domain-model-from-presentation.md), because every other decision except 0010 and 0011 depends on it. Once the layer rule is clear, the rest follow: domain models (0003), domain behaviour (0004, 0005, 0006), data-driven layout (0007), and test strategy (0008). ADRs 0009, 0010, and 0011 stand alone and address housekeeping, deployment, and documentation infrastructure respectively.
