---
type: Intentwise Delivery Contract
schema: intentwise/v0.4
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

## Target Experience

Show the final state in the smallest visual form that materially improves understanding. Prefer Mermaid when supported or a fenced `text` diagram otherwise. Use a user journey, data/control flow, state transition, or before/after mapping as the task requires. Show the default state first, label important incomplete or uncertain paths explicitly, and omit implementation sequencing.

```text
<starting state> -> <observable behavior> -> <expected result>
```

<one concise explanation of what the user or operator sees by default and what is in scope>

## Interaction States

Use actions for interactive work and events or conditions for system behavior. Include only states that materially distinguish the expected result.

| Trigger or state | Observable result | Persistent meaning or evidence |
| --- | --- | --- |
| <action, event, or condition> | <what changes or becomes visible> | <what remains true or inspectable> |

## Experience Rules

- <externally visible behavior or invariant that must remain true>

## Success Scenario

<one representative end-to-end scenario from the starting condition through the important action or system flow to the observable result; include a degraded or incomplete-evidence case when it is central to the task>

## Consequential Decisions

### D001 — <decision>

Choice: <selected consequence or outcome>

Rationale: <why this choice best supports the intent>

Evidence basis: <repository, connected organizational, current primary-source, or explicitly disclosed model basis>

Sources: <precise project-relative paths and symbols/tests, stable connected record IDs, user-supplied task identifiers, or authoritative URLs; never “repository” alone>

Applicability: <why this evidence fits the current system and constraints>

## Constraints

- <constraint>

## Delivery Strategy Expectations

Advisory outcome-level guidance only; implementation order remains delegated.

- <early evidence, deployability, compatibility, or rollout expectation; or state that no special strategy expectation exists>

## Learning Mode

Mode: COMPLETION

Use `COMPLETION`, `CHECKPOINTS`, or `OFF`.

## Execution

Disposition: CONTINUE

Use `CONTINUE` when approval should start implementation immediately. Use `DEFERRED` when approval should make the contract build-ready under `.intentwise/ready/` and stop.

## Maintainability Expectations

- <concrete repository-derived expectation and the acceptance criterion that verifies it; or state that repository conventions are sufficient>

## Acceptance Criteria

Write acceptance criteria only after completing the temporary source-derived semantic readiness worksheet from the draft preflight. Preserve every material source commitment in a criterion clause, including conditions, exceptions, and protected compatibility properties. Group clauses for readability without replacing them with broad labels; each clause needs a corresponding verification assertion. Sources locate authority and do not implicitly import omitted requirements. Each `Planned verification` must identify a concrete scenario or artifact, the action or check, and the observable assertions that can reach the required evidence level. It must not depend on “if available,” “when data is available,” or similar escape clauses. It is a verification plan, not evidence already obtained.

### AC01 — <criterion>

Expected: <observable behavior>

Sources: <precise authority locators for the normative commitments covered by this criterion>

Required evidence: L1 | L2 | L3

Planned verification: <specific scenario or artifact, check to run, and observable assertions>

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

Use the same `<contract-id>.md` filename through every lifecycle directory. Prefer `<issue-or-task-id>-<short-slug>.md` when an external ID exists. Otherwise use `<UTC-YYYYMMDD-HHMMSS>-<short-slug>-<six-random-hex>.md`. Never overwrite an existing file.

- `.intentwise/drafts/` + `DRAFT` while consequential decisions or approval remain open.
- `.intentwise/ready/` + `APPROVED` when the user accepted the contract with `Disposition: DEFERRED` and implementation has not started.
- `.intentwise/active/` + `APPROVED` while implementation is underway, then `IMPLEMENTED` when implementation is complete but verification is not.
- `.intentwise/completed/` + `VERIFIED` only when every acceptance criterion is `PASS` at its required evidence level and the actual change surface, delivery retrospective, and knowledge-promotion record are complete.

Each session owns only the contract it created or was explicitly asked to resume. Do not edit, validate as part of the current task, move, or close other contracts.

After every criterion passes and the completed record validates, set `VERIFIED` and move the same filename from `active/` to `.intentwise/completed/<contract-id>.md`. Keep a failed or unproven contract active unless the user explicitly closes it. Existing contracts under `.intentwise/active/` and a legacy `.intentwise/active.md` may be resumed in place when explicitly identified; never migrate them automatically.
