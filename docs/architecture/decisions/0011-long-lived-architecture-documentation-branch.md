# 0011. Long-lived architecture documentation branch

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

The architecture documentation under `docs/architecture/` has a different rhythm from the code. It is written in bursts during design work, it is reviewed as prose, and it must be able to run ahead of the implementation — these records describe a target architecture that does not exist yet, and their status is `proposed` precisely because of that. Committing that directly onto `main` would mix documentation of an intended future with code describing the present, and every documentation edit would sit in the same history as every code change.

## Decision Drivers

- Documentation of a *proposed* architecture must be shareable and reviewable before any code follows it.
- The author works alone; the workflow has to be worth remembering six months from now, which means it has to be simple.
- Documentation and code changes should be separable when reading history.

## Considered Options

- Option 1: One long-lived branch, `Software-Architecture-Branch`, holding only changes under `docs/architecture/**`, merged into `main` and never deleted.
- Option 2: A short-lived feature branch per documentation change, deleted after each merge.
- Option 3: Commit documentation straight onto `main`.

## Decision Outcome

Chosen option: "Option 1, with the following rules", because it balances the need to draft proposed architecture separately from implementation while keeping the workflow simple for a solo developer.

Rules of the branch:
- It contains **only** changes under `docs/architecture/**`. Code changes — the refactoring itself, `.gitignore`, `main.spec`, `requirements.txt` from [ADR-0010](0010-build-and-deployment-hygiene.md) — go on their own branches off `main`.
- All future documentation work starts here and reaches `main` by merging **from** this branch **into** `main`.
- It is **never deleted**. After a merge, work continues on the same branch; it is not a feature branch with an expiry.
- Before starting new documentation work, bring it up to date with `main` so that the two do not drift.

Rejected option 2: the conventional flow, but it means a new branch for every ADR, and for a solo author that ceremony is friction without a reviewer to justify it.

Rejected option 3: no place to draft a proposed architecture before it is agreed.

### Positive Consequences

- `git log main..Software-Architecture-Branch` shows exactly what documentation is pending.
- Proposed architecture can be drafted, read and revised before any code moves.
- Documentation and code histories stay separable.

### Negative Consequences

- A long-lived branch drifts from `main` if it is not refreshed — the discipline of merging in both directions has to be kept.
- The branch never disappearing means it can quietly go stale, so it must be brought up to date at the start of each documentation session rather than only at the end.

## More Information

The branch was created from `main` at commit `ebcd41a`, with the existing as-is arc42 chapters as its first commit. Related: [ADR-0010](0010-build-and-deployment-hygiene.md).
