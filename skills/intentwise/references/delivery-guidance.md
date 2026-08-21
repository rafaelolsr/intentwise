# Delivery Guidance

## Delivery strategy expectations

The implementation harness owns execution order, decomposition, and whether vertical slices are the best path. A contract may express outcome-level strategy expectations when they reduce consequential delivery risk:

- Reach independently testable end-to-end behavior early when practical.
- Preserve deployability and compatibility through migrations or staged rollouts.
- Avoid accumulating multiple unverified layers when early behavioral evidence is feasible.
- Record why another strategy was more suitable when that choice has a meaningful drawback.

Keep these expectations advisory unless the user explicitly makes a rollout, compatibility, or intermediate-state property part of the approved outcome. Never turn them into file-by-file steps, ordered implementation tasks, or mandatory checkpoints.

## Learning mode

Record exactly one mode in the contract:

- `COMPLETION` (default): no educational interruption during implementation. Teach through the verified delivery retrospective and include a diagram only when it materially clarifies the system.
- `CHECKPOINTS`: provide concise, non-blocking learning updates at safe conceptual boundaries while implementation continues. Use when the user asks to stay actively familiar with the changing system.
- `OFF`: omit educational commentary and optional diagrams. The factual delivery retrospective remains required for durable auditability.

In `CHECKPOINTS`, emit a learning update only when implementation changes an important conceptual model, such as a public API, persistence semantics, security boundary, runtime topology, cross-service flow, or operational failure mode. Include:

1. What changed.
2. Why it matters.
3. A small diagram when relationships or flow would otherwise be hard to understand.
4. One to three optional comprehension questions.

Continue by default; a learning checkpoint is not approval. If the user asks to slow down, answers in a way that reveals a material misunderstanding, or requests another explanation, pause at the next safe boundary and teach before continuing. Never expose hidden chain-of-thought.

## Maintainability expectations

Derive maintainability expectations from repository conventions and the risks of the requested change. Use concrete, reviewable properties such as:

- Reuse an established architectural boundary instead of creating a parallel path.
- Keep provider-specific behavior behind an existing adapter.
- Avoid duplicating consequential domain logic.
- Preserve public schema or API compatibility.
- Cover important failure behavior with deterministic tests.
- Document a new architectural or operational dependency.

Do not use vague requirements such as “clean code” or “best practices.” Map every meaningful maintainability expectation to an acceptance criterion with suitable evidence, or identify it as a residual risk when no immediate oracle exists. State that no special expectation exists when repository conventions are sufficient.
