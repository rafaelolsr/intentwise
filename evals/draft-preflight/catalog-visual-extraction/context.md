# Catalog Visual-Extraction Evaluation Context

Use the Intentwise draft-readiness preflight to review `draft-before.md`. Treat the following as authoritative source commitments for the evaluation:

- Task 3973869 extracts visual usage from normalized PBIP definition material and must remain within the catalog extraction boundary.
- A visual is data-bound when at least one supported direct Column or Measure binding is recoverable from projections, slicer state, or scoped filters. An unfamiliar or custom `visualType` does not disqualify it.
- A data-bound visual with recoverable identity and bindings emits one record even when `visualType` is absent. Its type is nullable or explicitly unknown and a typed warning records the gap.
- Every visual definition has exactly one primary disposition: structural group, data-bound usage, decorative, malformed or unrecoverable, or orphaned. Those totals reconcile to the current visual-definition count; warnings are additional annotations and do not inflate the total.
- A malformed page or visual does not abort valid definitions or other reports. Only an affected definition with no safely recoverable record is skipped, with typed warning and accounting.
- The analyzed OOS Compute snapshot contained 14 pages and 490 visual definitions. Those counts are a baseline, not a fixed acceptance target; live validation reports current totals and drift.
- Preserve visibility when normalized input represents it. Otherwise retain explicit unknown visibility and a warning or evidence gap; never infer visible without source evidence.
- With deterministic input and a fixed clock, existing `PbipBusinessMetricRecord` content, selection, ordering, and resulting canonical business metrics remain identical.
- Usage records retain source provenance. Static titles remain static, while measure-driven titles preserve binding identity without evaluating DAX.
- Extraction is independent of visual type when a supported binding schema is present and must be demonstrated with standard and unfamiliar or custom visual fixtures.
- Managed branch, target, and worktree state must be obtained from the repository-designated status authority immediately before presentation. The intended implementation context must be confirmed or the agent stops.
