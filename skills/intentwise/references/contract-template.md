---
type: Intentwise Delivery Contract
title: <short task title>
description: <one-sentence intended outcome>
tags: [intentwise, delivery]
timestamp: <ISO 8601 UTC>
---

# Intentwise Delivery Contract

Status: DRAFT

## Intent

<original user intent>

## Outcome

<observable state that must become true>

## Consequential Decisions

### D001 — <decision>

Choice: <selected consequence or outcome>

Rationale: <why this choice best supports the intent>

Evidence basis: <repository, connected organizational, current primary-source, or explicitly disclosed model basis>

Sources: <verifiable repository paths, connected records, or authoritative URLs>

Applicability: <why this evidence fits the current system and constraints>

## Constraints

- <constraint>

## Delivery Strategy Expectations

Advisory outcome-level guidance only; implementation order remains delegated.

- <early evidence, deployability, compatibility, or rollout expectation; or state that no special strategy expectation exists>

## Learning Mode

Mode: COMPLETION

Use `COMPLETION`, `CHECKPOINTS`, or `OFF`.

## Maintainability Expectations

- <concrete repository-derived expectation and the acceptance criterion that verifies it; or state that repository conventions are sufficient>

## Acceptance Criteria

### AC01 — <criterion>

Expected: <observable behavior>

Required evidence: L1 | L2 | L3

Observed evidence: NONE | L1 | L2 | L3

Result: UNPROVEN

Evidence: <not yet collected>

## Agent Autonomy

All implementation decisions not constrained above remain delegated to the implementation agent.

## Anticipated Change Surface

Advisory forecast only. This is not an implementation plan or approval boundary and may evolve without user approval unless a change crosses the consequential decision frontier.

```text
<project-relative tree with [create], [modify], or [delete] annotations>
```

## Actual Change Surface

Complete after implementation with the project-relative files actually created, modified, or deleted.

```text
<actual project-relative tree with [created], [modified], or [deleted] annotations>
```

## Delivery Retrospective

Complete before setting `Status: VERIFIED`. Keep it concise and explanatory; omit routine activity and hidden reasoning.

### Implementation Summary

<what changed and what capability now exists>

### How It Works

<important entry points, component interactions, data or control flow, and fit with the existing system>

### Autonomous Decisions

#### <meaningful implementation decision>

Decision: <what was chosen>

Why: <why it fit the contract and repository>

Alternative considered: <strongest realistic alternative>

Rejected because: <why that alternative was less suitable>

Drawbacks: <costs or limitations introduced by this choice>

### Drawbacks and Residual Risks

<remaining limitations, operational consequences, compatibility concerns, or unproven behavior; state when none are known>

### Verification Summary

<acceptance-criterion statuses and strongest supporting evidence>

## Knowledge Promotion

Complete before setting `Status: VERIFIED`.

- Task-local knowledge retained only in this contract: <summary or none>
- Knowledge concepts created or updated: <project-relative paths or none>
- Assets created or updated: <project-relative paths or none>

## Lifecycle

Keep each current contract at `.intentwise/active/<contract-id>.md` and use one status value. Prefer `<issue-or-task-id>-<short-slug>.md` when an external ID exists. Otherwise use `<UTC-YYYYMMDD-HHMMSS>-<short-slug>-<six-random-hex>.md`. Never overwrite an existing file.

- `DRAFT` while consequential decisions remain open.
- `APPROVED` only after the user has explicitly accepted the outcome, decisions, constraints, criteria, and evidence requirements. The drafting agent may record that acceptance but must not self-approve.
- `IMPLEMENTED` when implementation is complete but verification is not.
- `VERIFIED` only when every acceptance criterion is `PASS` at its required evidence level and the actual change surface, delivery retrospective, and knowledge-promotion record are complete.

Each session owns only the contract it created or was explicitly asked to resume. Do not edit, validate as part of the current task, or close other active contracts.

After every criterion passes and the completed record validates, set `VERIFIED` and move the same filename to `.intentwise/completed/<contract-id>.md`. A successful delivery is not closed while its verified contract remains under `active/`. Keep a failed or unproven contract active unless the user explicitly closes it. A legacy `.intentwise/active.md` may be resumed when explicitly identified, but new contracts must use the concurrent-safe directory convention.
