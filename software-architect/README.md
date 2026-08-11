# Software Architect

A four-role agent system that documents existing architectures, designs new ones from
requirements, produces UML diagrams as editable draw.io files, and records architecture
decisions with their reasoning — arc42 for the documentation, MADR for the decisions.

It reads production code but never changes it. Everything it writes goes to
`docs/architecture/`.

## Agents

| Agent | Model | Task |
| --- | --- | --- |
| `architect` (main session, this folder's `CLAUDE.md`) | opus | Talks to you, clarifies the assignment, decides the architecture, delegates, reviews |
| `codebase-analyst` | sonnet | Reconstructs the as-is architecture from code, reports back |
| `diagram-writer` | sonnet | Writes `.drawio` files as valid mxGraph XML |
| `doc-writer` | haiku | Fills arc42 chapters and MADR decision records |

The architect is the session itself, not a subagent — he has to talk to you. The other three are
subagents he calls; you never start them yourself.

## Starting it

```bash
cd agents/software-architect
claude
```

`.claude/settings.json` puts the session on Opus in Plan Mode. You will be asked once to switch
to Normal Mode before documents are written — the model switches happen on their own.

## Using it in another repository

Copy this folder into the target repository and start a session in it. That is all — the
`grill-me` skill ships with it under `.claude/skills/`.

Tell the architect what you want:
- *"Document the architecture of this system."*
- *"Design an architecture for the following requirements: …"*
- *"Document the architecture-relevant changes since the last release."*
- *"Where should we improve this architecture?"*

## Output

```
docs/architecture/
├── arc42/        # 01-introduction-and-goals.md … 12-glossary.md
├── diagrams/     # *.drawio — open in draw.io or the VS Code extension
└── decisions/    # NNNN-title.md in MADR format
```

## Dependencies

| Skill | Origin | Purpose |
| --- | --- | --- |
| `grill-me` | shipped under `.claude/skills/grill-me/` | The architect's assignment clarification |

## Language

This package is entirely in English, including the dialogue — deliberately diverging from the
repository convention. See `docs/ORCHESTRATION-DESIGN.md`.
