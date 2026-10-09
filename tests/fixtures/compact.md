---
type: Intentwise Delivery Contract
schema: intentwise/v0.4
format: compact
title: Local input error handling
---

# Intentwise Delivery Contract

Status: APPROVED

## Intent

Report invalid input bytes without a traceback.

## Outcome

The CLI rejects a decoding error through its ordinary input-error result.

## Constraints

Keep supported manifest behavior and the existing JSON fields.

## Execution

Disposition: CONTINUE

## Acceptance Criteria

### AC01 — Read error

Expected: Invalid UTF-8 produces an input-error result with exit 2 in both CLI modes.
Sources: User-supplied IW-301 input-error request.
Required evidence: L2
Planned verification: Run deterministic CLI tests on invalid bytes; assert text or JSON error results, exit 2 and no traceback.
Observed evidence: NONE
Result: UNPROVEN
Evidence: Not yet collected.

## Agent Autonomy

Unspecified mechanisms and equivalent checks remain delegated.
