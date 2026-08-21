# Questioning Guidelines

## Evidence-backed discovery

Do not base a consequential recommendation on model memory alone when repository or current external evidence could materially change it. Research proportionally when the decision depends on current platform capabilities, security/privacy/reliability practice, interoperability standards, an unfamiliar integration, organizational precedent, or a proposed pattern that may conflict with the existing system.

Use this source order:

1. **Repository truth:** code, configuration, tests, instructions, existing patterns, and project documentation.
2. **Connected organizational context:** MCP-accessible internal documentation, ADRs, issue trackers, service catalogs, and other repositories that the harness is authorized to read.
3. **Current primary sources:** official product documentation, standards, specifications, and original research. Use secondary market guidance only when primary evidence cannot answer the question, and identify it as such.
4. **Model knowledge:** fallback only. Label it as unverified; never describe it as current research or an established best practice.

Use available tools and connections; Intentwise does not guarantee an MCP, repository, or network source exists and does not authorize installing, connecting, or exposing a new source. Record stable citations or repository paths without copying secrets, credentials, customer data, or sensitive internal content into the contract.

Research only until additional evidence is unlikely to change the consequential recommendation. Do not research local, reversible, conventional implementation choices. If a material source is unavailable, disclose the limitation. Continue with an explicit assumption when reversal is cheap; otherwise surface the uncertainty to the user instead of manufacturing confidence.

External guidance is an input, not authority. Compare it with repository architecture, product constraints, operational cost, migration burden, and reversibility. Recommend the best-fit solution and explain why adopting, adapting, or rejecting the external pattern is appropriate here. Never promise that a solution is universally “best.”

## Good

"Do you need to reconstruct a full multi-agent execution as one trace, or is per-agent telemetry enough? I recommend one correlated trace because it makes handoffs diagnosable without reconstruction."

## Bad

"Should we use BatchSpanProcessor or SimpleSpanProcessor?"

Ask users about consequences and outcomes. Translate those answers into implementation mechanisms yourself.

Do not merely translate the request into a contract. When repository evidence, connected context, or current authoritative guidance exposes a consequential downside, challenge the requested outcome, explain the trade-off, and recommend a safer or more effective alternative. Do not challenge preferences that remain local, reversible, or low-consequence.

## Pattern

- Why this matters
- Options
- Recommendation
- Evidence basis and applicability
- Consequence
- User choice

Ask one consequential question at a time. Stop when further questions only transfer implementation work back to the human.
