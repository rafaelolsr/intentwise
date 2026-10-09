# Draft-Readiness Preflight

Run this preflight in two phases: establish the source-derived semantics, then adversarially audit the completed `DRAFT`. This order prevents plausible draft wording from anchoring its own review. The preflight is an authoring and review check, not approval, implementation verification, or proof that cited evidence is true.

## Minimum for small changes

For a small change (one behavior, one or two criteria, no cross-boundary, data, security or compatibility concern), the preflight is: read the request and the affected code, confirm each criterion traces to the request or a protected constraint, and confirm each planned check would fail on a materially wrong result. Skip the worksheet, the case-by-property matrix and any second audit pass. Use the full sections below only when the evidence triggers they name.

## Modes and verdicts

- **Authoring mode:** create or revise the draft. Silently correct every source-resolved defect before presenting it, using a bounded audit loop without exposing a known-fix draft merely because another pass is needed.
- **Review-only mode:** inspect an existing draft without editing it. Report every material finding and the source-established correction unless the user explicitly asks for revisions.

Return one verdict:

- `READY`: structural validation passes and no material semantic finding remains.
- `NEEDS REVISION`: one or more defects have corrections already established by authoritative sources. In authoring mode, apply those corrections before presentation whenever the file is safely editable; this verdict is primarily for review-only mode or a correction that cannot be applied within the current request.
- `BLOCKED`: approval depends on an unresolved user-owned choice that materially changes the outcome, risk, compatibility, or commitment, or context is missing that is required to determine what should be built. Easy reversal does not authorize choosing product behavior for the user.

Do not use `BLOCKED` for a defect with a known correction, a delegated implementation choice, difficult work, unavailable observed evidence, a verification environment that may later yield `UNPROVEN`, or uncertainty that can remain explicit without changing the approved outcome. The preflight must preserve both safety and progress.

## Review inputs

Re-read the strongest available source material rather than reviewing the draft in isolation:

1. The authoritative request, issue, or task and any acceptance text or discussion supplied for it.
2. Applicable approved or verified contracts discovered by searching `.intentwise/ready/`, `.intentwise/active/`, and `.intentwise/completed/` for the task ID and affected behavior, plus related tasks when they establish ownership or explicit exclusions.
3. Repository code, tests, configuration, documentation, and instructions relevant to the behavior.
4. Connected organizational or current primary evidence used by consequential decisions.
5. The draft contract during the final-audit phase only.

Treat claims in the draft as assertions to verify, not as source evidence. Never fill a gap from model memory when an available source could establish it.

## Proportional discovery

Use the smallest evidence set that establishes the approval decision without weakening it. The mandatory proof core is:

1. The exact authoritative request and acceptance commitments.
2. The relevant current behavior and execution path.
3. The observable gap between the current and intended behavior.
4. The components and contracts confirmed to participate in that gap.
5. A concrete proof target for the intended result.
6. Any material contradiction, unresolved consequential choice, or explicit evidence limitation.

Stop discovery at evidence saturation: additional inspection is unlikely to change the intended outcome, the observed gap, participating scope, consequential decisions, or proof target. This is a semantic stopping rule, not a file, source, section, or time limit. Never stop while material evidence remains unresolved merely to keep the draft short.

Expand beyond the core only when discovered evidence indicates at least one of these conditions:

- behavior crosses a component or ownership boundary;
- a shared API, schema, persisted format, identity, or compatibility contract may change;
- security, privacy, authorization, data integrity, or destructive consequences are material;
- migration, rollout, coexistence, or backward compatibility is part of the requested outcome or required by the current path;
- normative sources conflict or a related work item establishes ownership, an exclusion, or an applicable prior decision;
- partial, total, retry, fallback, or other failure semantics can materially alter the observable outcome.

Do not perform a general architecture survey, enumerate every layer, inspect every related item, attachment, commit, or historical discussion, or introduce modernization, cleanup, abstraction, migration, or future-support requirements without one of those evidence links. Treat adjacent or possible scope as a lead to test, never as required scope by default. Reuse one focused evidence packet through drafting; do not reproduce an exhaustive analysis inside the contract or implementation handoff.

## Source authority and supersession

Classify each material source before reconciling it:

- **Normative:** explicit current user requirements, current issue or task acceptance text, approved or verified contracts, and explicit organizational decisions. These constrain what the product should do.
- **Descriptive:** code, tests, logs, snapshots, and current runtime behavior. These establish what exists, what is feasible, and where a regression may be; they do not authorize a product change by themselves.
- **Advisory:** external guidance and model knowledge. These may support a recommendation but do not override repository-specific product authority.

An explicit current normative source may supersede an older decision only when it intentionally addresses the same behavior. A newer timestamp, changed implementation, failing test, or proposed draft is not supersession. If descriptive evidence conflicts with an applicable approved or verified decision, preserve the decision and classify the implementation as a possible regression. If one normative source clearly resolves a draft defect, the correction is source-resolved: repair it in authoring mode or return `NEEDS REVISION` in review-only mode. Use `BLOCKED` when normative sources genuinely conflict or leave a material user-owned outcome undecided.

## Phase 1: source-derived semantic readiness

Before writing criteria or evidence plans, build a temporary worksheet from the sources. Keep it compact, but make each applicable item concrete:

For each proposed obligation, identify the explicit requirement or the concrete connection to the requested outcome or an existing protected constraint. A hypothetical future risk, generic best practice, adjacent code smell, or available tool is insufficient. If that connection is absent, remove the obligation or leave it as optional guidance. The worksheet is a reasoning aid, not another deliverable or proof requirement; a few outcome-and-check notes are enough for a small change.

| Concern | What the worksheet must establish |
| --- | --- |
| Source commitment | The authoritative statement, a precise locator, and the contract behavior it constrains |
| Authority and supersession | Whether each source is normative, descriptive, or advisory; overlapping approved or verified decisions; and any explicit supersession |
| Operational semantics | Definitions for terms that decide inclusion, exclusion, classification, success, failure, or compatibility |
| States and failures | Material inputs and zero, one, partial, total, conflicting, malformed, missing, and unknown cases |
| Invariants and accounting | Lasting rules, classification partitions, reconciliation formulas, and whether warnings are primary outcomes or additional annotations |
| Scope and context | Owner, exclusions, dependencies, and any volatile branch, target, worktree, environment, or service state that must be confirmed |
| Proof target | The concrete scenario or artifact, action, and observable result capable of reaching the intended evidence level |

Do not persist this worksheet unless the user explicitly requests an audit artifact. It must be derived independently of the proposed wording; do not use the draft to fill missing cells.

Use project-relative paths and a symbol or test name when practical for repository sources, stable record identifiers for connected sources, authoritative URLs for external sources, and identify task text supplied directly by the user as user-supplied. Labels such as “repository,” “codebase,” or “documentation” alone are not evidence locators.

### Preserve commitments through compression

Before grouping criteria, split the normative sources into independently falsifiable commitments. Keep each condition, exception, precedence rule, quantifier, protected property, and explicit exclusion attached to its source locator. A broad label such as “replay-safe,” “backward compatible,” or “all errors handled” is not a substitute for those obligations.

Use the temporary worksheet to map each material commitment to its criterion clause and verification assertion. Check both directions: required commitments are covered, and added obligations or exclusions have authority. A citation does not import unrelated requirements. Conventions, examples and recommendations are not automatic acceptance obligations. Current bugs or uncaught exceptions do not authorize narrowing the requested outcome. When the request requires handling failed items and continuing, a routine read, decode or parse failure belongs in that policy; rejecting bad input does not require supporting a new input format. Repair a source-resolved gap instead of inventing a carve-out or asking another product question. A genuinely different scope needs a focused choice presented prominently before approval, not buried in a draft.

Group related commitments without dropping material distinctions. State them once or bind an exact source section with its applicable obligations and exclusions. Do not copy an entire previous contract or inherit its PASS labels. Carry forward applicable outcomes and reuse adequate checks with evidence applicable to the current implementation; add only uncovered assertions.

For example, a requirement to preserve CLI behavior may protect output bytes, output stream, diagnostic order, and exit code independently. A criterion saying only “the CLI stays compatible” loses those distinctions. Preserve just the properties the sources actually protect; do not generalize this example into mandatory CLI or pipeline rules for unrelated tasks.

Apply the following checks only when the sources or current path make them relevant, or when omitting one would allow a materially wrong observable result to satisfy the contract. Do not manufacture hypothetical state combinations or contract sections for inapplicable concerns.

### Operational definitions

Define every term whose interpretation changes whether an entity is included, classified, counted, emitted, skipped, successful, compatible, or failed. Prefer observable predicates over labels. An unfamiliar subtype or missing optional discriminator must not silently disqualify an entity when the required behavior can be established from other supported evidence.

### State, failure, and classification completeness

Enumerate material input modes and failure granularity. Define conflicting inputs and unsupported combinations explicitly rather than allowing silent precedence. For fan-out work, distinguish item, group, batch, and total failure and state whether valid siblings continue.

When the task classifies or accounts for a population, require exactly one primary disposition per input unless overlap is explicitly intended. Make the dispositions mutually exclusive and collectively exhaustive, reconcile their sum to the current input total, and keep warnings or secondary annotations from inflating that total.

Check the domain of quantified rules. A policy for “all records invalid” does not establish the outcome of an empty input merely because a universal predicate is vacuously true. When sources define nonempty success/failure cases but leave zero inputs unspecified, keep that outcome explicitly unspecified unless another authoritative source resolves it. Preserve any established zero-count/no-effect invariants without inventing a failure or success label; escalate only if that missing outcome crosses the decision frontier.

For derived collections or aggregates required to match a current source population, equality covers membership as well as values. Plan the transition that removes the last contributing source item and assert removal of the now-absent output group, unless retention of empty groups is explicitly required. Distinguish a legitimate zero-valued group with members from a stale group with no members. “Totals are correct” alone can permit obsolete output rows to survive.

### Missing and unknown values

Distinguish missing, unknown, malformed, unsupported, and absent-by-design states when their consequences differ. Preserve an unknown value or expose a warning/evidence gap unless a source authorizes a default; do not infer a convenient value merely to complete the flow.

### Baselines and invariants

Treat observed counts, snapshots, identifiers, and current examples as baselines unless the source explicitly makes them fixed acceptance targets. Live or mutable validation must report the current result and any drift from the baseline rather than failing solely because the snapshot changed.

### Acceptance boundaries and allowed variation

Criteria should describe the smallest set of observable outcomes and protected constraints that establishes success. Avoid exact output, zero deviation, exhaustive guarantees, mandatory tools, or additional cleanup unless the sources require them or they protect a material risk. Keep advisory delivery and maintainability guidance outside blocking criteria.

Where variation matters to acceptance, state the allowed range or equivalence in `Expected` or the relevant constraint: for example, latency at most an agreed limit, required fields with ordering delegated, or layout that preserves the agreed interactions. Do not invent a tolerance for an explicit exact requirement. Resolve an undecided material tolerance in a question round. Do not enumerate harmless implementation freedoms individually; unspecified mechanisms remain delegated.

Choose the lowest evidence level sufficient for the actual promise. Deterministic evidence may establish local logic; real platform execution is needed for a platform-only guarantee. Do not demand a live deployment for every task merely because one could exist. Flag a known environment dependency before approval and distinguish necessary acceptance proof from optional operational follow-up.

A deterministic subprocess check through the real local CLI can satisfy an L2 requirement for JSON, exit behavior, arithmetic, or source preservation. Calling the actual entry point does not itself make L3 the necessary minimum. Require L3 when acceptance depends on observing conditions that those local checks cannot establish, such as real deployment, integration, or an interactive experience; preserve explicit user-required evidence.

Use the smallest checks that can distinguish success from a materially wrong result. Reuse adequate existing evidence and test infrastructure; do not require another test suite, benchmark, screenshot, audit artifact, or independent reviewer just because it might add assurance. Expand proof only for an uncovered material property, an observed failure, or an explicit requirement. A tool failure is not a product failure; choose an equivalent suitable method before declaring proof unavailable.

### Compatibility and provenance

Replace vague promises such as “compatible,” “unchanged,” or “preserved” with the exact observable properties that must remain identical or intentionally differ, including content, selection, ordering, identity, timing, or canonical outputs when applicable. Identify required source provenance. When behavior may be static or dynamically driven, preserve the binding or expression identity without claiming to evaluate it unless evaluation is in scope.

### Scope ownership and volatile context

Separate preserving information for downstream work from interpreting or materializing it now. Verify that every behavior belongs to this task or is explicitly excluded.

Treat branch, target, worktree, deployment, credential, and service state as volatile. If it matters to approval or execution, query the authority named by repository instructions immediately before presentation; never infer managed state from Git or copy an earlier observation as current fact. A mismatch between intended and reported execution context is a blocker, not a draft assumption.

## Phase 2: final adversarial audit

Write the contract from the ready worksheet, then re-read the raw sources and audit the result. First run the structural validator. Record every structural error, but continue the semantic audit unless the draft or authoritative sources are unreadable; a structural failure must not hide additional approval gaps. Structural success is only the start of this phase.

### Acceptance counterexamples

For each criterion, construct the smallest materially incorrect implementation or result that could still satisfy its wording. Tighten the criterion when a wrong target, partial behavior, silent fallback, or out-of-scope substitute could pass. Preserve agreed concrete identifiers and scenarios when they are part of the required behavioral proof; do not hard-code an example that was only illustrative.

Also test a materially correct implementation that differs from the forecast, example, or chosen test method. If the draft rejects it without an authorized reason, remove the unnecessary restriction or make the allowed variation explicit. Audit for both missed obligations and invented obligations.

### Evidence readiness

Every current-schema criterion must include a concrete `Planned verification` that names the scenario or artifact, the action or check, and the observable assertions. Confirm that the plan can reach the declared level:

- `L1`: identified static code, configuration, or documentation inspection.
- `L2`: identified deterministic test, type check, schema check, linter, or assertion.
- `L3`: execution of the actual scenario with its observable result verified.

For a criterion containing several commitments, the plan must cover each material distinction, not just one happy-path example. Name the input classes or artifacts, action, and assertion together. “Add comprehensive tests” and “verify compatibility” do not identify what would fail if the behavior were wrong.

When a change adds an output mode, adapter, endpoint, or other interface over existing behavior, compare the same material input partitions through both the old boundary and the new boundary. Testing edge cases only in the shared implementation and happy paths only in the new interface leaves the translation unverified. Assert the promised relationships between results, errors, ordering, and side effects at the actual boundaries.

For several modes or outcomes, use a temporary case-by-property matrix to catch omissions: each source-required case is a row and each protected observable is a column. Include required absences such as an empty error stream, no duplicate publication, or no mutation when the source requires them. Cover each applicable cell in both the criterion and its plan; one explicit universal statement may cover several rows. Do not manufacture a Cartesian product of unrelated cases, persist another worksheet, or infer a guarantee from a citation alone.

Choose proof that matches the promise. Exact compatibility needs a comparison to the protected baseline or public API; ordering and identity need assertions on order and identity; a schema promise needs names, types, ordering, and nullability only when those are protected. A finite fixture list establishes its cases, not an unlimited grammar: for a universal supported-input claim, plan a justified partition or generated/property checks and inspect the shared decision path. Do not silently weaken the source requirement to fit the available tests, or promise exhaustive proof from a sample.

A new test or fixture may be planned before it exists. Describe how it will be constructed and what it must assert; do not invent an existing test name as evidence. A platform-only guarantee needs a concrete run and observed assertions on that platform, with cleanup when the run creates resources. Local doubles do not satisfy that guarantee.

The plan must identify a feasible starting method. Prefer existing checks that cover the promised properties; add a focused test or assertion only for a gap. A baseline extraction, second suite, snapshot or independent assertion is an alternative or gap-filling method, not automatically an additional gate. Do not promise multiple checks of the same property merely to strengthen the appearance of proof. Reject availability escape clauses; establish how a needed fixture can be made. Equivalent or stronger methods may replace the plan without approval when they preserve its property and boundary. An explicitly required platform or scenario remains binding; a mock cannot replace it. Missing necessary evidence is `UNPROVEN`. A plan is not observed evidence: keep `Observed evidence: NONE`, `Result: UNPROVEN`, and `Evidence: Not yet collected.` until qualifying evidence exists.

### Contract and lifecycle consistency

First compare the draft with applicable approved and verified lifecycle contracts and any explicit superseding requirement. Then confirm that the intent, outcome, target experience, interaction states, experience rules, decisions, constraints, maintainability expectations, acceptance criteria, and evidence plans tell one compatible story. Trace every source commitment and every material worksheet rule to at least one contract statement and criterion. Look specifically for silently reversed prior decisions, contradictions between inclusion rules and fallback states, primary accounting and warnings, partial-failure behavior and batch success, or exact compatibility and a weaker criterion. Do not turn the contract into an implementation task list.

## Revision boundary

In authoring mode, automatically revise every defect whose answer is already established by approved user decisions or verified sources. Do not create a new consequential product decision, invent evidence, broaden scope, or lower an evidence level to make the draft pass. Use a bounded audit loop, normally one or two passes, but do not expose a known-fix draft merely because a pass found it: apply the source-established correction and present the result only when it is ready or a true blocker remains.

Route remaining uncertainty by consequence:

| Condition | Action |
| --- | --- |
| Authoritative correction exists | Repair in authoring mode; `NEEDS REVISION` in review-only mode |
| Choice concerns implementation within the outcome, or can remain unknown without changing it | Delegate it or record the explicit unknown/gap; continue |
| Verification cannot run later | Preserve the criterion and report `UNPROVEN` during verification |
| Unresolved user-owned choice materially changes the outcome, risk, compatibility, or commitment | `BLOCKED`; ask the next independent question round |

If unresolved user-owned choices remain, keep any existing file under `drafts/`, ask the next independent question round, and do not request approval. Do not draft a complete speculative contract first when those choices can be identified from the source-derived view.

In review-only mode, do not revise the file. Finish the complete structural and semantic review and return `NEEDS REVISION` for source-resolved defects. Independent review may be used when the user explicitly requests it and the harness supports it, but it is never required by Intentwise.

## Presentation

Every new acceptance criterion must record precise authority locators in its
`Sources` field. A repository path or test that only describes current
behavior is not product authority unless an authoritative requirement protects
it.

If reporting coverage counts, derive them from the completed commitment-to-clause-to-assertion mapping. Reading every source or having a plan for every criterion does not establish completeness. A source-resolved omission is `NEEDS REVISION` even when structural validation passes; repair it during authoring or report the specific gap without requesting approval.

Keep the user-facing result compact: normally the verdict, structural/semantic checks and any material gap. Coverage counts are optional for a complex review or an explicitly requested audit; they are not evidence of completeness. When useful, report them from the actual commitment mapping:

```text
Draft preflight: READY

Coverage: sources <traced>/<material> · criteria <challenged>/<total> · verification <executable>/<total>
Structural validation: PASS
Semantic checks: PASS
```

Do not expose hidden reasoning, retain verbose critic logs, assign a confidence score, or describe the draft as approved.

In review-only mode, report source-resolved problems without rewriting:

```text
Draft review: NEEDS REVISION

Coverage: sources <traced>/<material> · criteria <challenged>/<total> · verification <executable>/<total>

1. <criterion or section>: <material defect and source-established correction>
```

When a consequential blocker remains, do not request approval. Ask the targeted question with a compact status:

```text
Draft preflight: BLOCKED

- Blocking gap: <decision the available evidence cannot resolve>
```

If a review contains both source-resolved findings and unresolved user-owned choices, use `BLOCKED`, include the established findings concisely, and ask the independent questions needed to continue. Defer dependent choices to later rounds.
