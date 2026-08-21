---
type: Intentwise Delivery Contract
title: Evidence-level integrity
description: Prevent recorded evidence below an acceptance criterion's requirement from producing PASS.
tags: [intentwise, verification, evidence]
timestamp: 2026-08-21T15:00:00Z
---

# Intentwise Delivery Contract

Status: VERIFIED

## Intent

Make Intentwise delivery records distinguish required evidence from the evidence actually obtained.

## Outcome

A completed contract cannot structurally claim `PASS` when its recorded observed evidence is absent or below the criterion's required evidence level.

## Consequential Decisions

### D001 — Evidence representation

Choice: Record one explicit observed evidence level beside every criterion while retaining concrete evidence as explanatory text.

Rationale: A machine-checkable level protects internal consistency without pretending that a structural validator can judge whether the underlying evidence is truthful.

Evidence basis: Existing validator behavior and Intentwise's documented separation between structural and behavioral proof.

Sources: `skills/intentwise/scripts/validate_contract.py`; `skills/intentwise/references/verification.md`.

Applicability: The validator already parses criterion fields, so level comparison strengthens the same boundary without adding semantic evidence evaluation.

### D002 — Verified record location

Choice: Treat a successful delivery as closed only after its validated contract is moved from `active/` to `completed/`.

Rationale: Durable knowledge can then use one stable provenance location instead of guessing whether a verified record was archived.

Evidence basis: Intentwise's completed-contract provenance model and the relative links used by durable knowledge concepts.

Sources: `skills/intentwise/references/knowledge-and-assets.md`; `.intentwise/knowledge/architecture/intentwise-evidence-validation.md`.

Applicability: A single completed location keeps provenance links stable while active contracts remain isolated by task.

## Constraints

- Keep the validator dependency-free and structural only.
- Do not add locks, queues, or execution control.

## Delivery Strategy Expectations

- Preserve validator compatibility for draft and unproven contracts while strengthening successful and failed results.

## Learning Mode

Mode: COMPLETION

## Maintainability Expectations

- Keep evidence ordering in one validator constant and cover boundary behavior with focused unit tests; verified by AC01 and AC02.
- Keep lifecycle and provenance rules consistent across the skill, template, and documentation; verified by AC03.

## Acceptance Criteria

### AC01 — Reject insufficient evidence

Expected: A criterion requiring L3 cannot be recorded as PASS with observed L2 evidence.

Required evidence: L2

Observed evidence: L2

Result: PASS

Evidence: `test_pass_rejects_observed_evidence_below_required_level` passes in the validator unit suite.

### AC02 — Require observed evidence

Expected: PASS and FAIL results cannot be recorded with observed evidence set to NONE.

Required evidence: L2

Observed evidence: L2

Result: PASS

Evidence: Focused validator tests cover PASS without sufficient evidence and FAIL with observed evidence set to NONE.

### AC03 — Preserve durable provenance

Expected: Successful closure moves the contract to `completed/`, and promoted knowledge links back to that immutable record.

Required evidence: L1

Observed evidence: L1

Result: PASS

Evidence: The lifecycle guidance requires completed placement, and the promoted architecture concept links to this completed contract.

### AC04 — Validate the complete record

Expected: This completed golden contract passes the deterministic Intentwise structural validator.

Required evidence: L2

Observed evidence: L2

Result: PASS

Evidence: `test_golden_completed_contract_is_valid` validates this file as part of the unit suite.

## Agent Autonomy

Field parsing, comparison mechanics, test organization, example naming, and diagram implementation remained delegated.

## Anticipated Change Surface

```text
skills/intentwise/
├── SKILL.md                                      [modify]
├── references/contract-template.md               [modify]
├── references/knowledge-and-assets.md            [modify]
├── references/verification.md                    [modify]
└── scripts/validate_contract.py                  [modify]
tests/
├── fixtures/valid.md                             [modify]
└── test_validate_contract.py                     [modify]
examples/golden-delivery/.intentwise/             [create]
README.md                                         [modify]
docs/principles.md                                [modify]
```

## Actual Change Surface

```text
skills/intentwise/
├── SKILL.md                                      [modified]
├── references/contract-template.md               [modified]
├── references/knowledge-and-assets.md            [modified]
├── references/verification.md                    [modified]
└── scripts/validate_contract.py                  [modified]
tests/
├── fixtures/valid.md                             [modified]
└── test_validate_contract.py                     [modified]
examples/
├── foundry-telemetry.md                          [modified]
├── webhook-retries.md                            [modified]
└── golden-delivery/.intentwise/                  [created]
README.md                                         [modified]
docs/principles.md                                [modified]
```

## Delivery Retrospective

### Implementation Summary

Intentwise contracts now record the strongest observed evidence separately from the minimum required evidence. Structural validation rejects successful results with absent or insufficient observed evidence, and successful closure has one canonical completed location.

### How It Works

Each acceptance criterion carries `Required evidence`, `Observed evidence`, `Result`, and concrete `Evidence`. The validator compares the two levels for PASS, while the skill independently judges the evidence and archives a fully verified record. The linked [evidence validation concept](../knowledge/architecture/intentwise-evidence-validation.md) and its [diagram](../assets/diagrams/evidence-flow.svg) explain the durable model.

### Autonomous Decisions

#### Represent no evidence explicitly

Decision: Use `NONE` as the pre-verification observed value.

Why: It makes the absence of evidence explicit and machine-checkable while keeping the Markdown readable.

Alternative considered: Omit the observed field until verification.

Rejected because: Optional structure would make incomplete and malformed criteria indistinguishable.

Drawbacks: Authors must update one additional field during verification.

### Drawbacks and Residual Risks

The validator checks recorded consistency, not the truth or relevance of evidence text. Concurrent changes to the same knowledge concept remain convention-based and require reconciliation rather than locking.

### Verification Summary

All four criteria pass. AC01, AC02, and AC04 have deterministic validator-test evidence; AC03 has static lifecycle and provenance-link evidence.

## Knowledge Promotion

- Task-local knowledge retained only in this contract: the choice of `NONE` as the explicit initial observed-evidence value.
- Knowledge concepts created or updated: `.intentwise/knowledge/architecture/intentwise-evidence-validation.md`.
- Assets created or updated: `.intentwise/assets/diagrams/evidence-flow.svg`.

## Lifecycle

This record is immutable provenance under `.intentwise/completed/`. Current explanations may evolve in the linked knowledge concept without rewriting this delivery record.
