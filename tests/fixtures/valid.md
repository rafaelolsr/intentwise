---
type: Intentwise Delivery Contract
schema: intentwise/v0.4
title: Diagnostic event retention
description: Retain recent diagnostic events without storing payload bodies.
tags: [intentwise, delivery]
timestamp: 2026-08-21T12:00:00Z
---

# Intentwise Delivery Contract

Status: APPROVED

## Intent

Add diagnostic event retention.

## Outcome

Operators can inspect recent diagnostic events.

## Target Experience

```text
Diagnostic event -> privacy filter -> 30-day event store -> operator query
```

An operator sees recent diagnostic metadata through the existing event-store boundary; payload bodies never enter the retained record.

## Interaction States

| Trigger or state | Observable result | Persistent meaning or evidence |
| --- | --- | --- |
| A diagnostic event is emitted | Its metadata becomes queryable | The stored record contains no payload body |
| An event becomes older than 30 days | It no longer appears in queries | The retention boundary remains explicit |

## Experience Rules

- Retained events remain queryable for 30 days.
- Payload bodies are never retained.

## Success Scenario

An operator queries a diagnostic event emitted during the previous 30 days, finds its metadata, and confirms that the stored result contains no payload body.

## Consequential Decisions

### D001 — Retention

Choice: Keep 30 days.

Rationale: This balances diagnosis and privacy.

Evidence basis: Repository retention conventions and the stated privacy constraint.

Sources: `src/events/`; repository privacy documentation.

Applicability: The existing event-store boundary already owns retention and payload filtering.

## Constraints

- Do not retain payload bodies.

## Delivery Strategy Expectations

- Keep the retention change independently testable without prescribing implementation order.

## Learning Mode

Mode: COMPLETION

## Execution

Disposition: CONTINUE

## Maintainability Expectations

- Preserve the repository's existing event-store boundary; verified by AC03.

## Acceptance Criteria

### AC01 — Query recent events

Expected: An operator can query events from the previous 30 days.

Required evidence: L3

Planned verification: Query deterministic events just inside and outside the 30-day boundary and assert that only the recent event is returned to the operator.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC02 — Exclude payloads

Expected: Stored events contain no payload body.

Required evidence: L2

Planned verification: Run the event-persistence tests with a payload-bearing fixture and assert that the stored record contains metadata but no payload body.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC03 — Preserve the event-store boundary

Expected: Retention is implemented through the repository's existing event-store boundary, with deterministic tests covering retention configuration.

Required evidence: L2

Planned verification: Run the retention configuration tests and inspect the changed call path to assert that retention remains behind the existing event-store boundary.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

## Agent Autonomy

All implementation decisions not constrained above remain delegated to the implementation agent.
