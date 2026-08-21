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

## Remediation

When evidence demonstrates `FAIL`, return the discrepancy to implementation, fix it within the approved decision boundary, and verify the affected criterion again. Continue until every criterion passes, a required check remains `UNPROVEN`, a new consequential decision needs user approval, or progress is genuinely blocked. A failed check does not authorize lowering or rewriting the acceptance criterion.

## Delivery retrospective

Before marking a contract `VERIFIED`, persist a compact teaching record in its `Delivery Retrospective` section. Write for a developer who understands the project but did not watch the implementation. Explain observable behavior and architecture in plain language, cite relevant files or tests when useful, and distinguish verified facts from residual uncertainty. Do not include a chronological activity log, exhaustive diff, routine edits, hidden chain-of-thought, or unsupported claims.

Include:

- **Implementation Summary:** what changed and what capability now exists.
- **How It Works:** the important entry points, component interactions, data or control flow, and how the change fits the existing system.
- **Autonomous Decisions:** only meaningful implementation choices not dictated by the contract or repository. For each, record **Decision**, **Why**, **Alternative considered**, **Rejected because**, and **Drawbacks**. State when no such decision exists.
- **Drawbacks and Residual Risks:** limitations, operational consequences, compatibility concerns, deferred risks, and anything still `UNPROVEN`. State when none are known.
- **Verification Summary:** acceptance-criterion statuses and the strongest evidence supporting them.

Keep the existing `Actual Change Surface` accurate so the reader can connect the explanation to files created, modified, or deleted. The retrospective teaches the delivered system; it does not create new requirements, implementation tasks, or approval gates.
