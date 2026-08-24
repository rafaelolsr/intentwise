# Intentwise Principles

Intentwise protects product intent without taking over execution. Its unit of control is a compact delivery contract, not a plan, graph, queue, or agent topology.

## Consequential decision frontier

The frontier separates choices a developer should see from choices a coding agent should make. A choice belongs on the human-visible side when alternatives materially change external behavior, risk, architectural commitment, compatibility, data semantics, or cost of reversal. Local, conventional, reversible choices stay delegated. The frontier should reduce questions: task complexity follows the density of consequential decisions, not lines of code.

## Evidence-backed discovery

Consequential recommendations should not rely on model memory when available repository, organizational, or current primary evidence could materially change them. Intentwise starts with repository truth, then uses authorized connected context such as MCP-accessible documentation and other repositories, then current official documentation, standards, specifications, or primary research. Model knowledge is a disclosed fallback, never evidence of current market practice.

External guidance does not automatically override a system's existing architecture. Every recorded decision states its evidence basis, sources, and why that evidence applies to the repository and constraints. Research stops when further information is unlikely to change the consequential recommendation; ordinary delegated implementation choices do not receive a mandatory research ceremony.

## Autonomy boundary

The approved contract is the boundary. The human controls intent, consequential decisions, constraints, acceptance criteria, and evidence requirements. The skill must present a draft and stop; only explicit user acceptance can approve it. Everything else belongs to the coding harness. Advisory strategy expectations may favor early end-to-end evidence, but execution order remains delegated. During implementation, discovery warrants escalation only when it introduces a consequential choice outside that boundary—not merely when the work becomes difficult, the implementation strategy changes, or an anticipated file tree evolves.

Approval and execution are distinct. A deferred approved contract is build-ready under `.intentwise/ready/` but grants no current implementation action. Only an explicit start moves it to `active/`. This lifecycle distinction records readiness without scheduling, prioritizing, or managing a backlog.

## Maintainability without ceremony

Maintainability expectations must name concrete repository boundaries, compatibility properties, duplication risks, tests, or documentation obligations and map them to acceptance evidence. Intentwise does not pretend that long-term ease of change has an immediate deterministic oracle. Unverifiable concerns remain explicit residual risks rather than vague claims of quality.

## Contract-first verification

Verification begins with each acceptance criterion, not with a tour of the implementation. For each criterion, identify what must be observable, obtain evidence at or above the required level, and record one result. Implementation claims may point toward evidence but cannot replace it.

## PASS, FAIL, and UNPROVEN

- `PASS`: sufficient evidence at the required level demonstrates the criterion.
- `FAIL`: evidence demonstrates the criterion is not satisfied.
- `UNPROVEN`: the criterion may be satisfied, but adequate evidence was not obtained.

`UNPROVEN` is deliberately different from failure. It prevents confidence from being manufactured when an environment cannot run a required scenario.

A demonstrated `FAIL` returns to implementation and verification within the approved boundary. It does not permit the harness to weaken the criterion. An unavailable required check is `UNPROVEN`, not a reason to rewrite working code indefinitely.

## Learn from delivery

A verified contract is also a compact teaching record for developers who did not watch the work. It explains what changed, how the delivered behavior fits the existing system, meaningful autonomous implementation decisions and their drawbacks, residual risks, the actual file surface, and verification evidence. It is not an activity log, exhaustive diff, implementation plan, or disclosure of hidden reasoning.

Learning mode controls timing, not authority. `COMPLETION` teaches at delivery, `CHECKPOINTS` adds non-blocking explanations at consequential conceptual boundaries, and `OFF` suppresses educational commentary while retaining the factual retrospective. A checkpoint never approves or redirects delegated implementation by itself.

## Durable knowledge, contained

Everything Intentwise creates stays under `.intentwise/`. Completed contracts are immutable provenance; `.intentwise/knowledge/` holds mutable current architecture, decisions, external integrations, and operational behavior. Persistent Markdown uses an OKF-compatible typed frontmatter envelope, while Intentwise retains its stricter body schema. Rich SVG, image, and HTML teaching assets live under `.intentwise/assets/` and must be referenced from knowledge or delivery records.

## Evidence levels

- `L0 — Claim`: someone or an agent says the behavior works. Never sufficient for PASS.
- `L1 — Static`: code, configuration, or documentation inspection supports the criterion.
- `L2 — Deterministic`: a reproducible test, type check, schema check, linter, or assertion supports it.
- `L3 — Behavioral`: the actual scenario is executed and its observable outcome is verified.

The contract specifies a minimum level. Higher evidence can satisfy a lower requirement when it addresses the same criterion; lower evidence cannot satisfy a higher requirement. Structural contract validation proves only contract structure, never product behavior.

Each criterion records both its required level and the strongest observed level. `PASS` is structurally invalid when observed evidence is absent or below the requirement; this check guards the record's internal consistency without claiming that the evidence itself is truthful or sufficient.
