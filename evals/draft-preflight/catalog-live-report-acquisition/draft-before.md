---
type: Intentwise Delivery Contract
schema: intentwise/v0.4
title: Catalog live-report acquisition
description: Acquire configured Power BI reports directly into the catalog pipeline.
tags: [intentwise, catalog, power-bi]
timestamp: 2026-08-31T12:00:00Z
---

# Intentwise Delivery Contract

Status: DRAFT

## Intent

Deliver Task 3973868 by adding live Power BI report acquisition to the catalog pipeline without persisting transient report content.

## Outcome

The catalog can acquire configured reports through the existing fetcher, normalize their definitions in memory, and pass the material to downstream extraction while preserving existing local PBIP behavior.

## Target Experience

```text
Power BI URL -> existing fetcher -> normalized in-memory PBIP -> downstream extraction
```

Operators can configure live reports instead of preparing a local PBIP directory, and individual report failures remain explicit.

## Interaction States

| Trigger or state | Observable result | Persistent meaning or evidence |
| --- | --- | --- |
| Local PBIP is configured | Existing local acquisition continues | Existing local behavior remains protected |
| Live reports are configured | Reports are fetched with bounded concurrency | Report content remains transient |
| Some live reports fail | Successful reports continue and failures are categorized | Partial failure remains explicit |
| Every live report fails | The batch cannot appear successful | Categorized failures remain available |

## Experience Rules

- Reuse the existing report fetcher without a feature flag.
- Keep live report content transient and avoid temporary PBIP directories.
- Preserve stable cache provenance and bounded deterministic concurrency.
- Defer graph, API, UI, and dedicated projection work.

## Success Scenario

With valid credentials and access, a configured report is fetched from its supplied Power BI URL, normalized as in-memory PBIP material, and passed to downstream extraction without creating a temporary PBIP directory.

## Consequential Decisions

### D001 — Acquisition boundary

Choice: Reuse the existing report fetcher and normalize its result at the catalog live-acquisition boundary.

Rationale: This preserves the established authentication and definition-fetching path without adding a second integration.

Evidence basis: Existing fetcher behavior and the Task 3973868 acquisition requirement.

Sources: Repository report fetcher, catalog acquisition boundary, and Task 3973868.

Applicability: The fetcher already returns report definition material that can be normalized without persistence.

## Constraints

- Do not persist live report content or create temporary PBIP directories.
- Do not add a feature flag.
- Keep page and visual accounting outside Task 3973868.

## Delivery Strategy Expectations

- Preserve local PBIP behavior while adding independently testable live acquisition.

## Learning Mode

Mode: COMPLETION

## Execution

Disposition: DEFERRED

## Maintainability Expectations

- Reuse the existing fetcher and keep live-source normalization behind one catalog acquisition boundary; verified by AC01 and AC04.

## Acceptance Criteria

### AC01 — Preserve acquisition modes

Expected: Existing local `--pbip-root` acquisition remains unchanged, and configured live reports can enter the same downstream extraction pipeline.

Required evidence: L2

Planned verification: Run deterministic tests for local-only acquisition and live-only acquisition, and assert that each reaches the existing extraction boundary.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC04 — Retain report identity

Expected: Normalized definition material retains extracted page and visual identity for downstream extraction while page and visual accounting remains outside this task.

Required evidence: L2

Planned verification: Normalize a report fixture and assert that its page and visual identity is exposed to the downstream extractor without persistence.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC05 — Report failures explicitly

Expected: Each failed live report produces a categorized, redacted failure while successful reports continue. A batch with no successes cannot appear successful.

Required evidence: L3

Planned verification: Execute mixed-success and all-failure batches, assert categorized redacted failures, and assert that the all-failure batch does not report successful live acquisition.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC08 — Live report reaches extraction

Expected: With valid credentials and access, the live-acquisition boundary fetches a configured report from its supplied Power BI URL. The result preserves the selected page ID, reports source format PBIP, contains non-empty normalized in-memory PBIP files, and creates no temporary PBIP directory.

Required evidence: L3

Planned verification: Fetch any accessible configured report through a supplied Power BI URL and assert its selected page ID, PBIP source format, non-empty normalized files, and absence of a temporary PBIP directory.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

## Agent Autonomy

Concurrency primitives, normalization helpers, module placement, and test organization remain delegated within the established acquisition boundary.
