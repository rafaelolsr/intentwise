---
type: Intentwise Delivery Contract
schema: intentwise/v0.4
title: Catalog lineage relationship regression
description: Restore visible relationship inspection in focused Catalog lineage.
tags: [intentwise, catalog, lineage]
timestamp: 2026-09-01T12:00:00Z
---

# Intentwise Delivery Contract

Status: DRAFT

## Intent

Restore persistent relationship inspection in focused Catalog lineage while preserving current behavior.

## Outcome

Catalog displays unlabeled collapsed connections. Selecting one opens a persistent right-side panel, and Bronze tables without recognized source metadata begin the graph without an unknown external origin.

## Target Experience

```text
Bronze table -- unlabeled connection --> downstream table | selected details panel
```

The graph remains compact and details appear only after selection.

## Interaction States

| Trigger or state | Observable result | Persistent meaning or evidence |
| --- | --- | --- |
| User selects a connection | A right-side relationship panel opens | Loaded evidence remains visible |
| Bronze source is unknown | The graph starts at Bronze | No external source is displayed |

## Experience Rules

- Collapsed connections have no visible label.
- The Catalog transform toggle remains hidden.
- Unknown external origins are omitted.

## Success Scenario

A user selects an unlabeled relationship, reads its evidence in the right-side panel, and sees no source node for an unknown Bronze origin.

## Consequential Decisions

### D001 — Prefer current renderer behavior

Choice: Treat current Catalog rendering and tests as authority for unlabeled edges, hidden transformation expansion, and omitted unknown origins.

Rationale: These behaviors are present in the current implementation.

Evidence basis: Repository implementation and tests.

Sources: `apps/webclient/src/features/agent/lineage/LineageGraph.tsx`; `apps/webclient/src/features/catalog/CatalogLineageExplorer.test.tsx`

Applicability: These files render the focused Catalog lineage surface.

## Constraints

- Preserve Agent/chat behavior.
- Do not add network requests for relationship selection.

## Delivery Strategy Expectations

Advisory outcome-level guidance only; implementation order remains delegated.

- Keep the panel change Catalog-specific.

## Learning Mode

Mode: COMPLETION

## Execution

Disposition: DEFERRED

## Maintainability Expectations

- Reuse the existing Catalog lineage boundary; verified by AC01.

## Acceptance Criteria

### AC01 — Selected relationship opens beside the graph

Expected: Selecting an unlabeled collapsed Catalog relationship opens a persistent right-side panel using loaded evidence.

Required evidence: L3

Planned verification: Render the focused Catalog scenario, select the actual connection, and assert that the graph and persistent right-side panel remain visible without another request.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

### AC02 — Unknown source is omitted

Expected: A Bronze table with an unknown origin receives no external source node.

Required evidence: L2

Planned verification: Run the Catalog source projection for an unknown-origin Bronze fixture and assert that the graph starts at Bronze.

Observed evidence: NONE

Result: UNPROVEN

Evidence: Not yet collected.

## Agent Autonomy

All implementation decisions not constrained above remain delegated to the implementation agent.
