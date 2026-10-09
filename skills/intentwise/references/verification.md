# Verification

## Statuses

- PASS — sufficient evidence demonstrates the criterion.
- FAIL — evidence demonstrates the criterion is not satisfied.
- UNPROVEN — implementation may exist, but required evidence could not be obtained.

## Evidence levels

- L0 Claim: an agent says it works.
- L1 Static: code/config inspection supports it.
- L2 Deterministic: tests, type checks, schemas, linters, assertions, or reproducible checks prove it.
- L3 Behavioral: the actual scenario is executed and the observable result is verified.

Contracts may specify a minimum evidence level per acceptance criterion.

Choose that minimum during drafting to match the promised property. Local deterministic behavior generally needs L2; a real deployment, integration, or platform-only promise may need L3. Optional future operational checks belong in follow-up or residual risks, not acceptance criteria for an unrelated task.

Deterministic checks may execute the real local CLI and assert its JSON, exit behavior, arithmetic, or source bytes at L2. Actual entry-point execution alone does not justify requiring L3. Set a higher minimum only when the promise needs observations those local checks cannot establish or the user explicitly requires it. Stronger evidence may still be recorded when actually obtained.

Never silently downgrade required evidence. If L3 is required and the environment cannot execute the scenario, report UNPROVEN.

## Contract-first verification

Assess criteria in contract order. For each criterion, record the status and concrete evidence in the contract. Implementation notes help locate evidence but are not themselves proof.

Record the strongest evidence actually obtained as `Observed evidence: NONE | L1 | L2 | L3`. `PASS` requires an observed level at or above the criterion's `Required evidence`; `FAIL` requires concrete observed evidence demonstrating the discrepancy. Use `NONE` when no independent evidence was obtained. An observed level below the requirement may inform the record but remains `UNPROVEN`.

Evidence levels are minimums:

- L0 Claim: an assertion without independent support. It can never justify PASS.
- L1 Static: inspection of code, configuration, or documentation.
- L2 Deterministic: a reproducible test, type check, schema check, linter, or assertion.
- L3 Behavioral: execution of the actual scenario and observation of the required outcome.

A validator can prove that a contract has the required structure (L2 for that structure). It cannot prove that the implemented product satisfies the contract.

Start with adequate existing checks. Identify the uncovered property before adding a test, baseline comparison, snapshot or supplementary assertion; methods covering the same property are alternatives rather than cumulative gates unless the user requires both. Evidence may serve several criteria. Stop once it covers the approved promises at their required levels. Repeat only for a change, failure or remaining gap. Reviewer preference for more tests, a benchmark, screenshots or a live environment does not create a new obligation.

## Variation and amendments

Judge the delivered behavior against the approved outcome and its allowed tolerances, not against an implementation forecast or illustrative snapshot. A different file tree, helper, visual arrangement, current population count, or test tool is not itself a failure unless that property was explicitly protected.

`Planned verification` is a starting method. Substitute fixtures, tools, or check sequence autonomously when the evidence still tests the same promised property and boundary at the required level or higher. Record a meaningful substitution and the actual assertions in `Evidence`; no new approval is needed. Do not replace actual platform behavior with a mock, omit required cases, or trade away a protected property under the name of flexibility.

When discovery requires a materially different outcome, compatibility promise, constraint, tolerance, or minimum evidence, propose a focused amendment: what changed, why, the consequence, and a recommendation. Ask independent amendment questions in a round and pause only dependent work. After explicit acceptance, record the prior commitment and the approved replacement, update affected criteria and plans, and verify the amended contract. Do not erase a failure or treat an amendment as implementation evidence.

If the user explicitly closes delivery with a remaining gap, record that disposition and the honest `FAIL` or `UNPROVEN` result; do not label it `VERIFIED`. Full verification means every current approved criterion passes, including any explicitly approved amendment.

## Remediation

When evidence demonstrates `FAIL`, return the discrepancy to implementation, fix it within the approved decision boundary, and verify the affected criterion again. Continue until every criterion passes, a required check remains `UNPROVEN`, a new consequential decision needs user approval, or progress is genuinely blocked. A failed check does not authorize lowering or rewriting the acceptance criterion.

## Delivery retrospective

Before `VERIFIED`, write a brief `Delivery Retrospective`: what changed, how it works, any meaningful trade-off, and residual risks. For ordinary work, a paragraph is sufficient. Explain only choices with material consequences or a useful non-obvious rationale; routine formatting, helper extraction and test placement do not need alternative/rejection essays. Keep statuses and proof in the criterion ledger and refer to it rather than repeat it. Omit chronology, exhaustive diffs and hidden reasoning.

Compact contracts need no retrospective subsections. Existing full contracts retain their five required headings, but each can be a short statement; use “No meaningful autonomous decision” rather than invent one. Keep `Actual Change Surface` accurate. Promote knowledge only when it adds durable value, without duplicating this record. The retrospective creates no new acceptance or approval gate.
