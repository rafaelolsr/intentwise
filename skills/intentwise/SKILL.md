---
name: intentwise
description: Preserve developer control over consequential software decisions while delegating implementation. Use for ambiguous features, architectural changes, migrations, or other engineering work that benefits from a compact intent contract and evidence-based verification; skip the interview for clear, low-consequence tasks.
---

# Intentwise

Preserve this sequence: **Intent -> Implications -> Consequential Decisions -> Autonomy -> Evidence**. This is intent and verification control, not planning or orchestration.

Whenever presenting an Intentwise-created file to the user, resolve and show its absolute filesystem path. When the interface supports Markdown file links, make the path clickable. Keep paths stored inside contracts and knowledge documents relative for portability.

## Shape the contract

1. Inspect the repository's code, tests, configuration, documentation, and instructions before asking anything. Infer what those sources already establish. When an unresolved consequential decision depends on current platform behavior, domain practice, organizational precedent, or an unfamiliar integration, use available connected sources and authoritative primary sources following [evidence-backed discovery](references/questioning.md#evidence-backed-discovery); do not present model memory as researched fact or turn ordinary implementation choices into a market survey.
2. Restate the intended observable outcome and derive its important implications.
3. Identify only choices whose consequences cross the [decision frontier](references/decision-frontier.md). Do not surface uncertainty merely because implementation is difficult.
4. For each unresolved consequential choice, ask one outcome-focused question at a time. Recommend the best fit for the repository and user intent—not an abstract universal best practice—and state its evidence basis, applicability, and consequences. Follow [questioning guidance](references/questioning.md).
5. Stop questioning when remaining choices are local, reversible, conventional, or mechanical. A clear low-consequence task normally needs no questions. Use a tiny contract only when an acceptance condition, constraint, or decision is worth preserving; otherwise proceed directly.
6. For non-trivial work, read [delivery guidance](references/delivery-guidance.md) and write the compact, OKF-compatible [delivery contract](references/contract-template.md) as `DRAFT` to its own `.intentwise/drafts/<contract-id>.md`. Prefer an existing issue or task ID plus a short slug; otherwise use a UTC timestamp, short slug, and six-character random suffix. Never overwrite an existing contract. Record outcomes, maintainability expectations, and constraints, never an implementation task list unless the user explicitly asks for one. An anticipated change surface and delivery-strategy expectations are advisory; they may influence evidence without prescribing the harness's implementation order.
7. Present the draft contract and stop for review. Only explicit user acceptance authorizes approval; never self-approve or infer approval from having written the contract. On acceptance, record `APPROVED`. If `Execution` is `DEFERRED`, move the contract to `.intentwise/ready/<contract-id>.md` and stop. If it is `CONTINUE`, move it to `.intentwise/active/<contract-id>.md` and proceed. Do not begin implementation before acceptance or while a contract remains under `drafts/` or `ready/`.

The human owns intended outcomes, external behavior, consequential trade-offs, architectural commitments, privacy/security choices, constraints, and acceptance criteria. The coding agent owns every implementation choice not constrained by the contract, including decomposition, ordinary APIs, file organization, refactoring mechanics, tools, tests, iteration, and debugging.

## Implement

Treat a user-approved contract as authoritative while independently inspecting the repository and choosing the implementation path. When the user explicitly starts a contract under `ready/`, change its execution disposition to `CONTINUE`, move it to `active/`, and proceed; this does not reopen the approved product decisions. Do not ask approval for delegated choices. Apply its [learning mode and delivery guidance](references/delivery-guidance.md) without turning learning checkpoints into approval gates. The anticipated change surface and implementation strategy may evolve without approval as local choices become clearer. Stop only if new information creates a consequential decision outside the approved contract; difficulty or ordinary implementation divergence alone is not a reason to stop.

Track the selected contract as it moves between lifecycle directories. Update only the contract this session created or was explicitly asked to resume; other files in `drafts/`, `ready/`, and `active/` belong to other work. If present, validate the selected file with `python3 <skill-directory>/scripts/validate_contract.py <contract-path>`. A successful structural check does not prove runtime behavior.

## Verify and close

Read [verification guidance](references/verification.md), then independently assess every acceptance criterion against its required evidence. Report exactly `PASS`, `FAIL`, or `UNPROVEN`; never accept an implementation claim as proof or silently lower the required evidence level. When evidence demonstrates `FAIL`, remediate the implementation and verify again unless doing so requires a new consequential decision or progress is genuinely blocked. Do not turn missing evidence into implementation churn: if required evidence cannot be obtained, report `UNPROVEN`.

Update the selected contract's status, actual change surface, observed evidence levels, and verification result. Before marking it `VERIFIED`, persist the compact [delivery retrospective](references/verification.md#delivery-retrospective) and follow [knowledge and asset guidance](references/knowledge-and-assets.md): promote durable current knowledge inside `.intentwise/knowledge/`, keep rich media in `.intentwise/assets/`, and record what was promoted. When all criteria pass, validate the completed record, set it to `VERIFIED`, and move that same file to `.intentwise/completed/<contract-id>.md`; the delivery is not closed while its verified contract remains active. Otherwise leave it active. Use the retrospective for the final report; do not narrate routine steps or hidden reasoning.
