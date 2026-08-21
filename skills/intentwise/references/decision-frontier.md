# Consequential Decision Frontier

A decision belongs on the human-visible side of the frontier when its consequences materially affect the intended outcome.

## Surface

Surface choices involving high impact, expensive reversal, externally visible behavior, architecture boundaries, security/privacy, failure semantics, data loss/corruption risk, compatibility, or meaningful product trade-offs.

## Delegate

Delegate variable/function names, routine module placement, conventional API usage, mechanical refactoring, local helper design, formatting, ordinary test organization, and other reversible implementation details unless the contract explicitly makes them consequential.

## Heuristic

For each unresolved issue consider:
- Impact: how different would the resulting system be?
- Reversibility: how expensive is changing it later?
- User relevance: does the user care about the consequence rather than the mechanism?
- Risk: can it create security, privacy, data, operational, or compatibility harm?

Do not turn this into literal bureaucracy. The rubric exists to reduce questions, not generate them.

## Autonomy boundary

The contract is the boundary, not a recipe. Anything not fixed by intent, consequential decisions, constraints, acceptance criteria, or required evidence remains delegated. New implementation information crosses the boundary only when it creates a materially different outcome, risk, commitment, or cost of reversal.
