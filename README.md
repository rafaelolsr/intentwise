# Intentwise

**Decide what matters. Delegate the rest.**

Intentwise is a small, harness-agnostic Agent Skill that helps a developer surface consequential software decisions, delegate everything else to the coding agent, and verify delivery against explicit evidence.

`Intent -> Implications -> Consequential Decisions -> Autonomy -> Evidence`

Intentwise is not a planner, orchestrator, workflow engine, model router, worktree manager, or replacement coding harness. A non-trivial task starts with one project-local Markdown contract. Verified work may also curate durable knowledge and explanatory assets, all contained under `.intentwise/`. One standard-library validator checks contract structure.

## How it behaves

- Inspects the repository before asking questions.
- Uses repository evidence first, then authorized connected context such as MCP-accessible documentation and other repositories, then current primary external sources when they can materially improve a consequential decision.
- Asks only about consequential outcomes and recommends a default.
- Asks no questions for clear, low-consequence work.
- Stores each non-trivial contract as a draft at `.intentwise/active/<contract-id>.md`, then stops for explicit user approval before implementation.
- Supports concurrent sessions by keeping contracts separate and session-owned.
- Leaves all choices outside the contract to the coding harness.
- Escalates only when implementation reveals a new consequential decision.
- Expresses advisory delivery-strategy expectations without prescribing implementation order.
- Supports `COMPLETION`, `CHECKPOINTS`, and `OFF` learning modes; checkpoints teach without becoming approval gates.
- Maps concrete, repository-derived maintainability expectations to acceptance evidence.
- Shows an advisory anticipated file tree and records the actual change surface without making either an execution plan.
- Records required and actually observed evidence levels, and verifies each acceptance criterion as `PASS`, `FAIL`, or `UNPROVEN` without allowing lower evidence to satisfy a higher requirement.
- Remediates demonstrated failures inside the approved boundary, verifies again, and persists a compact delivery retrospective that teaches what changed, how it works, why meaningful choices were made, and which drawbacks remain.
- Uses an [OKF-compatible](https://okf.md/spec/) Markdown envelope and promotes durable current knowledge under `.intentwise/knowledge/`; rich media remains separate under `.intentwise/assets/`.

See [the principles](docs/principles.md), [contract template](skills/intentwise/references/contract-template.md), and [examples](examples/).

## Install

The installable unit is the `skills/intentwise` directory. Copy or symlink that entire directory so its `SKILL.md`, `references/`, and `scripts/` stay together.

### Codex

For one repository:

```sh
mkdir -p .agents/skills
cp -R /path/to/intentwise/skills/intentwise .agents/skills/intentwise
```

For personal use across repositories, copy it to `~/.agents/skills/intentwise`. Codex discovers repository skills under `.agents/skills` from the current directory through the repository root and personal skills under `~/.agents/skills`. Invoke it explicitly with `$intentwise`, or let Codex select it from the description. Restart Codex if a new skill does not appear.

Official reference: [OpenAI — Build skills](https://developers.openai.com/codex/skills).

### Claude Code

For one repository:

```sh
mkdir -p .claude/skills
cp -R /path/to/intentwise/skills/intentwise .claude/skills/intentwise
```

For personal use, copy it to `~/.claude/skills/intentwise`. Claude Code automatically discovers custom skill directories containing `SKILL.md` in those locations.

Official reference: [Anthropic — Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

### GitHub Copilot

For a project skill, copy the directory to `.github/skills/intentwise` (Copilot also documents `.agents/skills` and `.claude/skills` as project locations). For a personal Copilot CLI skill, use `~/.copilot/skills/intentwise` or `~/.agents/skills/intentwise`.

```sh
mkdir -p .github/skills
cp -R /path/to/intentwise/skills/intentwise .github/skills/intentwise
```

Copilot CLI can reload newly added skills with `/skills reload`, inspect them with `/skills info intentwise`, and invoke this one as `/intentwise`.

Official references: [GitHub — Adding agent skills for Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) and [Copilot CLI skill reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#skills-reference).

These locations and behaviors were checked against the linked official documentation on August 20, 2026. Product support can change; consult the links when packaging for another surface.

## Use

For a non-trivial request, ask the harness to use Intentwise while describing the desired outcome:

```text
Use Intentwise to add reliable webhook retries, then implement and verify the approved contract.
```

Intentwise first uses repository evidence. For consequential decisions whose answer depends on current or organizational knowledge, it then consults authorized connected sources such as MCP-accessible documentation and other repositories, followed by authoritative primary external sources when available. It records the evidence basis, sources, and applicability instead of presenting model memory as research. If consequential ambiguity remains, it asks one consequence-focused question at a time with a best-fit recommendation. It writes a `DRAFT` contract and stops; only explicit user acceptance makes that contract `APPROVED`. After approval, the coding harness implements autonomously and records the actual change surface and evidence in its selected `.intentwise/active/<contract-id>.md`. Delivery-strategy expectations and the forecasted file tree may influence evidence but never prescribe implementation order. Learning checkpoints, when enabled, teach through non-blocking conceptual updates rather than approval gates. Demonstrated failures return to implementation and verification; unavailable evidence remains `UNPROVEN`. Before `VERIFIED`, the contract gains a durable delivery retrospective and records any current knowledge or explanatory assets promoted under `.intentwise/`. A fully passing, structurally valid contract then moves to `.intentwise/completed/` with the same filename as immutable provenance; it is not closed while still active.

### Concurrent tasks

Each task gets a separate file:

```text
.intentwise/
├── index.md
├── active/
│   ├── IW-142-webhook-retries.md
│   └── 20260820-194530-telemetry-privacy-a3f91c.md
├── completed/
├── knowledge/
│   ├── index.md
│   ├── architecture/
│   ├── decisions/
│   ├── external/
│   └── operations/
└── assets/
    ├── diagrams/
    ├── images/
    └── visualizations/
```

Prefer an issue or task ID plus a short slug. Without one, use a UTC timestamp, short slug, and six-character random suffix. A session updates only the contract it created or was explicitly asked to resume; it must never overwrite or close another active contract. Active contracts are isolated; shared knowledge remains convention-based concurrency rather than a locking system. Shared indexes must not become active-task registries. Before updating canonical knowledge, re-read and reconcile the target, stopping on an unsafe conflict rather than overwriting it.

See the [complete golden delivery](examples/golden-delivery/.intentwise/completed/IW-204-evidence-integrity.md) for a verified contract linked to durable knowledge and a separate explanatory asset.

Run the structural validator from this repository or an installed skill:

```sh
python3 skills/intentwise/scripts/validate_contract.py .intentwise/active/IW-142-webhook-retries.md
```

Exit code `0` means the OKF envelope and Intentwise Markdown structure are valid, `1` means the contract is structurally invalid, and `2` means the file could not be read. Structural validity never proves implementation, maintainability, or runtime behavior.

## Develop

There are no runtime dependencies beyond Python 3.10+ for the optional validator. Run the tests with:

```sh
python3 -m unittest discover -s tests -v
```

Validate the included contracts directly:

```sh
python3 skills/intentwise/scripts/validate_contract.py tests/fixtures/valid.md
python3 skills/intentwise/scripts/validate_contract.py tests/fixtures/invalid.md
python3 skills/intentwise/scripts/validate_contract.py examples/webhook-retries.md
python3 skills/intentwise/scripts/validate_contract.py examples/foundry-telemetry.md
```

The invalid fixture is expected to exit with code `1`.

## Repository layout

```text
skills/intentwise/
  SKILL.md
  references/
  scripts/validate_contract.py
docs/principles.md
examples/
tests/
LICENSE
```

Intentwise is available under the [MIT License](LICENSE).
