# Delivery contract formats

Use `intentwise/v0.4` with `format: compact` by default. This keeps the agreement and evidence inspectable without requiring separate views of the same behavior. Multiple modes or failure cases alone do not require the full layout; describe them in criteria or a small optional state table. Use the [full layout](full-contract-template.md) when substantial interface, migration/rollout or architectural complexity makes the compact record hard to review, or the user requests it. Keep an existing contract's format when resuming it; never migrate it just to satisfy validation.

The codebase establishes current behavior, not permission to add obligations or carve requested behavior out of scope. Prefix `Sources:` with `Agent-proposed:` for a criterion the user did not request but concrete evidence implies; the user keeps or drops it at approval. Trace each material criterion and exclusion to authority. Put each fact in one place; link to exact binding source sections instead of repeating them. A diagram, decision record, learning mode, forecast file tree, or knowledge note is optional unless it materially helps this task.

Use this compact layout, replacing placeholders and removing template instructions:

```markdown
---
type: Intentwise Delivery Contract
schema: intentwise/v0.4
format: compact
title: <short task title>
description: <one-sentence intended outcome>
tags: [intentwise, delivery]
timestamp: <ISO 8601 UTC>
---

# Intentwise Delivery Contract

Status: DRAFT

## Intent

<original request or precise task locator>

## Outcome

<observable result; include a short example or state mapping only when useful>

## Constraints

<protected properties, source-authorized exclusions and material allowed variation; no additional constraints if none apply>

## Execution

Disposition: CONTINUE

## Acceptance Criteria

### AC01 — <material outcome>

Expected: <observable behavior and any agreed tolerance>
Sources: <precise authority locators for the normative commitments covered by this criterion>
Required evidence: L1 | L2 | L3
Planned verification: <existing adequate check, or a focused check for an uncovered property; scenario and assertions>
Observed evidence: NONE
Result: UNPROVEN
Evidence: Not yet collected.

## Agent Autonomy

Unspecified implementation mechanisms and equivalent verification methods remain delegated.
```

Use `CONTINUE` when approval starts implementation, or `DEFERRED` when approval only makes the contract ready. Learning mode defaults to `COMPLETION`; add `## Learning Mode` with `Mode: CHECKPOINTS` or `Mode: OFF` only when selected. If a consequential choice needs preserving, add a short `## Consequential Decisions` record with `### D001 — title`, `Choice`, `Rationale`, and precise `Sources`; do not document routine mechanisms as product decisions.

Choose the lowest evidence sufficient for each promise. A plan is a starting method, not an additional guarantee: an existing suite plus a focused uncovered-case check may cover several criteria. Do not list overlapping suites, baseline replays, snapshots and independent assertions as cumulative gates. Equivalent or stronger methods may replace the plan while preserving the same property and boundary. Required real-platform evidence stays required.

At closure, add `## Actual Change Surface` with the actual files and `## Delivery Retrospective` with a brief explanation of what changed, how it works, meaningful trade-offs if any, and residual risks. Keep criterion evidence in the ledger rather than repeat it here. Routine formatting, helper placement and test-file choices need no decision essay. Promote knowledge only when it has durable value beyond this record; cite any promoted paths in the retrospective or an optional `## Knowledge Promotion` section.

Keep the same filename through `drafts/DRAFT`, `ready/APPROVED` with `DEFERRED`, `active/APPROVED` or `IMPLEMENTED` with `CONTINUE`, and `completed/VERIFIED`. Only explicit acceptance approves a draft. Move to `completed` only when every criterion passes at its required level and the actual surface and retrospective are complete; otherwise retain honest FAIL or UNPROVEN results in `active`. Update only this session's selected contract. Preserve prior commitments when the user explicitly approves an amendment.
