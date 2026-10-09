# Consequential Decision Frontier

A decision belongs on the human-visible side of the frontier when its consequences materially affect the intended outcome.

## Surface

Surface choices involving high impact, expensive reversal, externally visible behavior, architecture boundaries, security/privacy, failure semantics, data loss/corruption risk, compatibility, or meaningful product trade-offs.

Reversibility affects how much discussion a choice needs, not who owns it. Two easily implemented options may serve different audiences or define different success conditions; ask when the request and existing authority do not choose between them. Facts established by code are for the agent to resolve, while desired behavior remains the user's decision.

## Delegate

Delegate variable/function names, routine module placement, conventional API usage, mechanical refactoring, local helper design, formatting, ordinary test organization, and other reversible implementation details unless the contract explicitly makes them consequential.

## Heuristic

For each unresolved issue consider:
- Impact: how different would the resulting system be?
- Reversibility: how expensive is changing it later?
- User relevance: does the user care about the consequence rather than the mechanism?
- Risk: can it create security, privacy, data, operational, or compatibility harm?

Use the rubric to distinguish material outcome choices from implementation details, not as a checklist requiring a question for every uncertainty. Ask independent unresolved choices together in a round.

## Autonomy boundary

The contract is the boundary, not a recipe. Anything not fixed by intent, consequential decisions, constraints, acceptance criteria, or required evidence remains delegated. New implementation information crosses the boundary only when it creates a materially different outcome, risk, commitment, or cost of reversal.
