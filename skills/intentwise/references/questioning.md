# Questioning Guidelines

## Evidence-backed discovery

Do not base a consequential recommendation on model memory alone when repository or current external evidence could materially change it. Research proportionally when the decision depends on current platform capabilities, security/privacy/reliability practice, interoperability standards, an unfamiliar integration, organizational precedent, or a proposed pattern that may conflict with the existing system.

Use this discovery order while keeping authority distinct from implementation evidence:

1. **Product authority:** the explicit current user request; current issue or task acceptance text and discussion; applicable approved or verified Intentwise contracts; and explicit organizational decisions such as ADRs. Search overlapping `.intentwise/ready/`, `.intentwise/active/`, and `.intentwise/completed/` records by task ID and affected behavior. Draft contracts are assertions, not authority.
2. **Repository implementation evidence:** code, configuration, tests, instructions, existing patterns, and project documentation. These establish current behavior, feasibility, constraints, and regressions. They do not by themselves authorize a different product outcome or prove that an existing behavior is invalid.
3. **Connected organizational context:** MCP-accessible internal documentation, issue trackers, service catalogs, and other repositories that the harness is authorized to read.
4. **Current primary sources:** official product documentation, standards, specifications, and original research. Use secondary market guidance only when primary evidence cannot answer the question, and identify it as such.
5. **Model knowledge:** fallback only. Label it as unverified; never describe it as current research or an established best practice.

An explicit current authoritative statement that intentionally addresses the same behavior may supersede an older decision. Recency, a new draft, or changed code alone does not. When implementation evidence conflicts with an applicable approved or verified decision and no authoritative supersession exists, preserve the decision and treat the implementation as a regression or the draft as needing correction.

Use available tools and connections; Intentwise does not guarantee an MCP, repository, or network source exists and does not authorize installing, connecting, or exposing a new source. Record stable citations or repository paths without copying secrets, credentials, customer data, or sensitive internal content into the contract.

Research only until additional evidence is unlikely to change the consequential recommendation. Use the codebase as the source of truth for facts about current behavior, interfaces, constraints, and feasible paths. Investigate factual uncertainty yourself rather than interviewing the user about what the repository can establish. If a material source is unavailable, disclose the limitation; a low-impact implementation assumption may remain explicit. Ask whenever an unresolved user-owned choice materially changes the intended outcome, even if reversal is cheap. A source-established correction is not a question.

External guidance is an input, not authority. Compare it with repository architecture, product constraints, operational cost, migration burden, and reversibility. Recommend the best-fit solution and explain why adopting, adapting, or rejecting the external pattern is appropriate here. Never promise that a solution is universally “best.”

## Good

"Do you need to reconstruct a full multi-agent execution as one trace, or is per-agent telemetry enough? I recommend one correlated trace because it makes handoffs diagnosable without reconstruction."

## Bad

"Should we use BatchSpanProcessor or SimpleSpanProcessor?"

Do not ask whether existing behavior should be preserved, or whether to add something the request did not mention (a total row, extra columns, new options), unless evidence shows a conflict or the request implies it; preserve by default and leave additions out. Ask users about consequences and outcomes. Translate those answers into implementation mechanisms yourself.

Do not merely translate the request into a contract. When repository evidence, connected context, or current authoritative guidance exposes a consequential downside, challenge the requested outcome, explain the trade-off, and recommend a safer or more effective alternative. Do not challenge low-impact preferences or delegated implementation details.

## Question rounds

Model unresolved decisions by their dependencies. In each round, ask the independent decisions whose prerequisites are settled. Group them as a short numbered list; keep each question understandable without another answer from the same round. Defer dependent questions until their parent choice is answered. Investigate missing facts while independent questions can proceed; use available tools without requiring subagents or a particular harness.

For each question, name the outcome choice, recommend the best fit, and explain the material trade-off using the evidence already found. Keep the wording concise enough that the user can answer by number or accept a recommendation. For example:

1. Should the report show the current backlog or work completed in a date range? I recommend the current backlog because the existing store has current states but no transition history. A completion trend would require collecting that history.
2. Should leads see team totals or individual breakdowns? I recommend team totals for this overview; individual breakdowns introduce a different audience and privacy decision.

Wait for answers before advancing dependent decisions or drafting their commitments. If the user answers only part of a round, preserve unanswered choices and ask for those still needed. Never treat silence, a preselected option, your recommendation, or general enthusiasm as an answer. An explicit instruction to choose on the user's behalf delegates that choice within the stated scope.

Recompute the remaining decisions after every answer rather than following a fixed questionnaire. Challenge consequential downsides and conflicting answers with a focused follow-up. Stop when material user-owned choices are resolved by answers or existing authority and only implementation details remain. Summarize the resulting outcome in the draft for the existing approval step; do not add another confirmation gate.
