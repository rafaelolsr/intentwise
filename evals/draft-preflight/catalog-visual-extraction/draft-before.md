---
type: Intentwise Delivery Contract
schema: intentwise/v0.4
title: Catalog visual extraction
description: Map PBIP visual definitions into catalog visual usage records.
tags: [intentwise, catalog, power-bi]
timestamp: 2026-08-31T14:00:00Z
---

# Intentwise Delivery Contract

Status: DRAFT

## Intent

Deliver Task 3973869 by extracting visual usage from normalized PBIP report definitions.

## Outcome

Catalog extraction maps data-bound visuals and reports accounting for the OOS Compute report.

## Target Experience

```text
PBIP definitions -> recognize visual type -> usage records + accounting
```

Recognized data visuals become usage records; unsupported or incomplete visuals remain non-mapped.

## Interaction States

| Trigger or state | Observable result | Persistent meaning or evidence |
| --- | --- | --- |
| A recognized data visual is found | One visual usage record is emitted | Its binding remains inspectable |
| `visualType` is absent | The visual remains non-mapped with a warning | Accounting records the omission |
| Visibility is absent | The visual is treated as visible | Extraction continues |
| A malformed definition is found | That definition is skipped | A warning is recorded |

## Experience Rules

- Data-bound visuals are visuals recognized by the current mapper.
- Mapped visuals, non-mapped visuals, and warnings are counted against the 490-definition target.
- Preserve existing business-metric behavior compatibly.

## Success Scenario

The OOS Compute fixture contains 14 pages and 490 definitions; recognized visuals produce usage records and the remaining definitions and warnings are counted.

## Consequential Decisions

### D001 — Visual mapping boundary

Choice: Map supported visual definitions during catalog extraction and leave graph projection to later tasks.

Rationale: This task owns extraction rather than projection.

Evidence basis: Task 3973869 and the existing PBIP extraction path.

Sources: Task 3973869; repository PBIP extractor.

Applicability: Normalized definition material is already available at this boundary.

## Constraints

- Run implementation on managed branch `feat/graph-report-mapping`.
- Do not change graph, API, or UI behavior.
- Do not evaluate DAX.

## Delivery Strategy Expectations

- Protect existing business metrics while adding visual usage records.

## Learning Mode

Mode: COMPLETION

## Execution

Disposition: CONTINUE

## Maintainability Expectations

- Keep visual parsing behind the existing extraction boundary; verified by AC01 and AC06.

## Acceptance Criteria

### AC01 — Map data-bound visuals

Expected: Every data-bound visual emits one usage record when its visual type is supported by fixture data.

Required evidence: L2

Planned verification: Map standard visual fixtures when fixture data is available and assert one usage record per mapped visual.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC02 — Account for incomplete visuals

Expected: A visual without `visualType` is non-mapped and produces a warning, even when binding data is present.

Required evidence: L2

Planned verification: Run a missing-type fixture and assert a non-mapped disposition and warning.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC03 — Reconcile OOS Compute

Expected: Extraction reports 14 pages and totals mapped visuals, non-mapped visuals, and warnings to 490 definitions.

Required evidence: L3

Planned verification: Re-fetch OOS Compute and assert exactly 14 pages and 490 accounted definitions.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC04 — Isolate malformed definitions

Expected: A malformed definition is skipped with a typed warning.

Required evidence: L2

Planned verification: Run a malformed visual fixture and assert that it is skipped with a typed warning.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC05 — Preserve visibility

Expected: Source visibility is retained, and a visual without visibility is recorded as visible.

Required evidence: L2

Planned verification: Run visible, hidden, and missing-visibility fixtures and assert their stored Boolean values.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC06 — Preserve compatibility

Expected: Existing `PbipBusinessMetricRecord` output remains compatible.

Required evidence: L2

Planned verification: Run existing business-metric tests and assert that they continue to pass.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

## Agent Autonomy

Parser organization, warning types, and test placement remain delegated within the catalog extraction boundary.
