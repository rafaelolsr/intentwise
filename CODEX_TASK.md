# Codex Implementation Task — Intentwise v0.1

You are implementing the first usable release of **Intentwise**, a harness-agnostic Agent Skill.

Read the entire repository before editing anything.

## Product thesis

Intentwise should help a developer preserve control over intent and consequential decisions without micromanaging an autonomous coding harness.

It follows:

**Intent → Implications → Consequential Decisions → Autonomy → Evidence**

The skill must not become a planner, orchestrator, workflow engine, or verbose requirements questionnaire.

## Deliverable

Turn this design scaffold into a polished, installable open-source Agent Skill repository suitable for use with Codex, Claude Code, and GitHub Copilot where their Agent Skills conventions permit it.

## Required work

1. Review and refine `skills/intentwise/SKILL.md` for clarity, minimalism, and strong agent behavior.
2. Validate the YAML front matter and directory conventions against current Agent Skills conventions available in your environment/docs.
3. Keep the primary skill concise. Move detailed guidance into `references/` rather than bloating `SKILL.md`.
4. Add at least three realistic examples:
   - trivial task that requires no interview
   - medium feature with 2–4 consequential decisions
   - architectural task with meaningful trade-offs
5. Add a contract lifecycle convention. Prefer a tiny project-local `.intentwise/` state directory with an `active.md` contract and optional completed history, but change this if a more portable convention is clearly better.
6. Add a deterministic validation script that can validate an Intentwise contract structurally. It must not pretend to prove runtime behavior.
7. Add automated tests for the validator.
8. Add installation/use instructions for the major harnesses that currently support compatible Agent Skills, but only state behaviors you can verify from current documentation or local conventions.
9. Add a short design/principles document explaining:
   - consequential decision frontier
   - autonomy boundary
   - contract-first verification
   - PASS / FAIL / UNPROVEN
   - evidence levels L0–L3
10. Add LICENSE recommendation or an appropriate permissive license if repository conventions make that safe to do.
11. Add a clean `.gitignore` and any minimal development configuration needed by the validator/tests.

## Critical behavioral requirements

### Repository-first
The skill must inspect available code/config/docs before questioning the user.

### Consequence-first questioning
Ask about consequences and outcomes, not implementation mechanisms.

### Recommendations
When surfacing a decision, provide a recommended option and briefly explain why.

### Adaptive depth
Trivial tasks should normally produce zero questions. Complexity is driven by consequential-decision density, not task size.

### No planning bureaucracy
Do not generate implementation task lists unless explicitly requested.

### Autonomy
Everything outside explicit intent, decisions, constraints, and acceptance criteria belongs to the coding harness.

### Escalation
During implementation, stop only when new information creates a consequential decision outside the approved contract.

### Verification
Verify acceptance criteria independently against evidence. Never treat implementation claims as proof.

Use PASS / FAIL / UNPROVEN.

### Evidence
Support the conceptual levels:
- L0 claim
- L1 static evidence
- L2 deterministic evidence
- L3 behavioral evidence

Do not mark PASS if the contract requires a higher evidence level than can be obtained.

## Design constraints

- No custom orchestrator.
- No LangGraph.
- No MCP server.
- No model router.
- No task database.
- No worktree manager.
- No unnecessary runtime dependencies.
- Prefer Markdown + a very small validation utility.
- Keep the repository easy to understand in under five minutes.

## Quality bar

Before declaring completion:

1. Run all tests.
2. Run the contract validator against valid and invalid fixtures/examples.
3. Inspect the final diff for unrelated changes.
4. Verify the skill remains substantially smaller than the systems it is intended to replace.
5. Produce a short final report mapping each required work item to concrete evidence.
6. Call out anything that remains UNPROVEN rather than claiming success.

## Do not

Do not redesign Intentwise into a multi-agent delivery framework. If a proposed feature adds execution control rather than intent/decision/evidence control, leave it out unless strictly necessary.
