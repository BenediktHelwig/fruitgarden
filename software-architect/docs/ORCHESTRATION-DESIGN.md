# Orchestration Design: Software Architect

## Problem

The client needs a senior software architect as an agent system. It must do four things:

1. Survey and document the architecture of existing systems
2. Propose an architecture for new projects from their requirements, complete enough that the
   software can be built from it
3. Produce UML diagrams as draw.io files, usable as build instructions rather than decoration
4. Record every architecture-relevant change together with the reasons behind it — the normal
   professional practice of a software architect

The package is copied into the target project's repository and works on the real code.

## Role split

Four roles, because the work divides cleanly along one line: judgement versus rendering.

**`architect` — the main session, not a subagent.** He talks to the user, so he cannot be a
subagent: subagents receive a prompt and return a report, with no conversational partner. They
could neither run the grill-me clarification nor ask for a permission mode switch and wait for
the answer. His persona is therefore the package `CLAUDE.md`.

**`codebase-analyst`** exists because reconstructing an as-is architecture fills a context window
with code that the architect does not need to see — he needs the conclusion. Deliberately given
no write tools, which lets him run in Plan Mode alongside the clarification phase.

**`diagram-writer`** and **`doc-writer`** are separate because their output formats have nothing
in common. mxGraph XML demands coordinate arithmetic and structural precision; arc42 prose
demands filling a fixed template. One prompt covering both would serve neither well.

No separate reviewer role: the architect reviews his own team's output. A dedicated reviewer
would pay for the same judgement work twice on the same model.

## Model choice

| Agent | Model | Reasoning |
| --- | --- | --- |
| `architect` | opus | Decides under uncertainty, weighs quality goals against each other, judges whether a report is good enough |
| `codebase-analyst` | sonnet | Interprets facts that are *present* rather than deciding under uncertainty — pattern recognition over given material. Reads large codebases far more cheaply than Opus |
| `diagram-writer` | sonnet | Structural work, not stamping: coordinates, edge endpoints and UML semantics have to line up, and broken XML only shows up when the file is opened |
| `doc-writer` | haiku | Fixed template, content supplied — pure execution |

`sonnet` was added at the client's suggestion, and it was the right call: the consultant template
only offered `opus` and `haiku`, which is too coarse for both middle roles.

## Flow

Four workflows, all sharing the same shape: clarify → analyse/design → **mode gate** → write →
review.

- **W1 Document existing:** grill-me → `codebase-analyst` → architect interprets → gate →
  `diagram-writer` + `doc-writer` → review
- **W2 New design:** grill-me → architect designs → gate → `diagram-writer` +
  `doc-writer` → review against "could a developer build from this?"
- **W3 Document a change:** architect reads `git log`/`git diff`, filters for architecture
  relevance → gate → `doc-writer` writes ADRs, `diagram-writer` updates diagrams
- **W4 Improvements:** builds on W1 → gate → each proposal as an ADR with status `proposed`

`diagram-writer` and `doc-writer` are independent and may run in parallel.

**Escalation:** on an insufficient report the architect re-delegates with a concrete defect list,
at most twice, then asks the user a precise question instead of guessing further.

## Mode and model control

The model switches by itself — each subagent carries `model:` in its frontmatter, so delegation
moves to Sonnet or Haiku and back to Opus automatically. The architect never asks for a model
change.

The permission mode cannot be changed by an agent, so the architect asks — **exactly once per
assignment**, immediately before the first write delegation. He never asks to switch back:
review only reads, and after a failed review he must be able to re-delegate straight away.

`.claude/settings.json` sets `model: opus` and `defaultMode: plan`, so a session started in this
folder begins in the right state. The startup check in `CLAUDE.md` covers the case where the
session was started elsewhere.

## Deliberately not included

- **No production code changes.** The architect designs and justifies; a developer implements.
  This also removes any risk of a subagent overwriting code.
- **No commit hook for ADRs.** Considered and rejected: it would run unasked on every commit,
  cost tokens on trivial changes, and reach into the target repository's configuration, which
  weakens portability. ADRs are produced on request, with the architect filtering `git log` for
  relevance himself.
- **No PlantUML or Mermaid alongside draw.io.** Two sources for one diagram drift apart. draw.io
  was chosen, so draw.io is the only source.
- **No orchestration directory and no config file.** The flow lives in the architect's prompt;
  delegation happens through the Agent tool.

## Language

The entire package is in English — files, prompts, artefacts and the dialogue with the user.

This deliberately diverges from the repository convention in the root `CLAUDE.md` ("Deutsch in
Dokumentation und Agent-Definitionen"). It was an explicit client decision, for two reasons:
a prompt and its output in the same language avoid the drift that occurs when a
German-language prompt is asked to produce English documents; and English is the safer choice
for a package meant to be copied into arbitrary repositories.

The one exception is the row added to the agent table in the root `README.md`, which stays
German — it belongs to the repository, not to the package.
