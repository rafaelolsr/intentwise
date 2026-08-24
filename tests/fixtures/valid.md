---
type: Intentwise Delivery Contract
schema: intentwise/v0.2
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

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC02 — Exclude payloads

Expected: Stored events contain no payload body.

Required evidence: L2

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC03 — Preserve the event-store boundary

Expected: Retention is implemented through the repository's existing event-store boundary, with deterministic tests covering retention configuration.

Required evidence: L2

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

## Agent Autonomy

All implementation decisions not constrained above remain delegated to the implementation agent.
