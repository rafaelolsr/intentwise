# Expected Approval-Readiness Findings

The preflight should report `NEEDS REVISION`, not `READY`, and preserve these behavioral corrections:

1. **Managed state is asserted without current authority.** Re-query the repository-designated managed-state command immediately before presentation. Remove stale branch claims; if the intended implementation context is not confirmed, stop rather than assume it.
2. **“Data-bound visual” is circular.** Define it by a recoverable supported direct Column or Measure binding in projections, slicer state, or scoped filters. An unfamiliar `visualType` must not disqualify it.
3. **Missing `visualType` contradicts complete extraction.** A data-bound visual with recoverable identity and bindings still emits one record with nullable or unknown type plus a typed warning.
4. **Accounting overlaps and does not reconcile.** Give every definition exactly one primary disposition—structural group, data-bound usage, decorative, malformed or unrecoverable, or orphaned—and reconcile those totals to the current definition count. Warnings remain additional.
5. **Partial-failure behavior is incomplete.** A malformed page or visual must not abort valid definitions or other reports. Skip only an affected definition for which no safe record is recoverable, with typed warning and accounting.
6. **The analyzed baseline is treated as an invariant.** Re-fetch OOS Compute, reconcile the current totals, and report drift from 14 pages and 490 definitions instead of requiring those historical counts.
7. **Unknown visibility is silently defaulted.** Preserve represented visibility; otherwise record explicit unknown plus a warning or evidence gap. Do not infer visible or require upstream conversion without evidence.
8. **Compatibility is too vague.** With deterministic inputs and a fixed clock, require identical existing `PbipBusinessMetricRecord` content, selection, ordering, and resulting canonical business metrics.
9. **Provenance and title semantics are absent.** Add criteria for source provenance and for static versus measure-driven titles; retain dynamic binding identity without evaluating DAX.
10. **Evidence is conditional and too narrow.** Reject “when fixture data is available.” Require fixtures that demonstrate extraction from supported binding schemas for both standard and unfamiliar or custom visual types.

The reviewer may phrase the findings differently, but it must preserve their behavioral consequence and avoid unrelated implementation requirements.
