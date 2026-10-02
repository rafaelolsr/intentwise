from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "intentwise" / "scripts" / "validate_contract.py"
SKILL_GUIDANCE = ROOT / "skills" / "intentwise" / "SKILL.md"
PREFLIGHT_GUIDANCE = ROOT / "skills" / "intentwise" / "references" / "draft-preflight.md"
FIXTURES = Path(__file__).parent / "fixtures"
GOLDEN_CONTRACT = (
    ROOT
    / "examples"
    / "golden-delivery"
    / ".intentwise"
    / "completed"
    / "IW-204-evidence-integrity.md"
)
PREFLIGHT_EVAL_DRAFT = (
    ROOT
    / "evals"
    / "draft-preflight"
    / "catalog-live-report-acquisition"
    / "draft-before.md"
)
VISUAL_EXTRACTION_EVAL_DRAFT = (
    ROOT
    / "evals"
    / "draft-preflight"
    / "catalog-visual-extraction"
    / "draft-before.md"
)
PRIOR_CONTRACT_EVAL_DRAFT = (
    ROOT
    / "evals"
    / "draft-preflight"
    / "prior-contract-regression"
    / "draft-before.md"
)
sys.path.insert(0, str(SCRIPT.parent))

from validate_contract import validate  # noqa: E402


class ContractValidationTests(unittest.TestCase):
    def fixture(self, name: str) -> str:
        return (FIXTURES / name).read_text(encoding="utf-8")

    def test_valid_contract(self) -> None:
        self.assertTrue(validate(self.fixture("valid.md")).valid)

    def test_golden_completed_contract_is_valid(self) -> None:
        self.assertTrue(
            validate(GOLDEN_CONTRACT.read_text(encoding="utf-8"), GOLDEN_CONTRACT).valid
        )

    def test_cli_accepts_golden_completed_legacy_contract(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(GOLDEN_CONTRACT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, "")

    def test_review_mode_defines_the_complete_verdict_contract(self) -> None:
        skill = SKILL_GUIDANCE.read_text(encoding="utf-8")
        preflight = PREFLIGHT_GUIDANCE.read_text(encoding="utf-8")
        self.assertIn("review-only mode", skill)
        self.assertIn("continue the semantic audit", skill)
        for verdict in ("READY", "NEEDS REVISION", "BLOCKED"):
            self.assertIn(f"`{verdict}`", skill)
            self.assertIn(f"`{verdict}`", preflight)

    def test_preflight_semantic_gap_fixture_is_structurally_valid(self) -> None:
        self.assertTrue(validate(PREFLIGHT_EVAL_DRAFT.read_text(encoding="utf-8")).valid)

    def test_visual_extraction_fixture_catches_conditional_evidence_plan(self) -> None:
        errors = validate(VISUAL_EXTRACTION_EVAL_DRAFT.read_text(encoding="utf-8")).errors
        self.assertIn(
            "AC01 Planned verification must not make evidence conditional on availability or feasibility",
            errors,
        )

    def test_prior_contract_regression_fixture_is_structurally_valid(self) -> None:
        self.assertTrue(validate(PRIOR_CONTRACT_EVAL_DRAFT.read_text(encoding="utf-8")).valid)

    def test_preflight_preserves_source_authority_and_progress(self) -> None:
        skill = SKILL_GUIDANCE.read_text(encoding="utf-8")
        preflight = PREFLIGHT_GUIDANCE.read_text(encoding="utf-8")
        self.assertIn("approved and verified contracts remain product authority", skill)
        self.assertIn("Return `NEEDS REVISION`, not `BLOCKED`", skill)
        self.assertIn("do not authorize a product change by themselves", preflight)
        self.assertIn("Do not use `BLOCKED` for a defect with a known correction", preflight)
        self.assertIn("Verification cannot run later", preflight)

    def test_invalid_fixture_reports_multiple_structural_errors(self) -> None:
        errors = validate(self.fixture("invalid.md")).errors
        self.assertTrue(any("invalid status" in error for error in errors))
        self.assertTrue(any("missing required section" in error for error in errors))
        self.assertTrue(any("Required evidence" in error for error in errors))

    def test_verified_requires_all_criteria_to_pass(self) -> None:
        text = self.fixture("valid.md").replace("Status: APPROVED", "Status: VERIFIED")
        result = validate(text)
        self.assertIn("VERIFIED requires every acceptance criterion to be PASS", result.errors)

    def test_verified_requires_learning_record(self) -> None:
        text = (
            self.fixture("valid.md")
            .replace("Status: APPROVED", "Status: VERIFIED")
            .replace("Result: UNPROVEN", "Result: PASS")
            .replace("Observed evidence: NONE", "Observed evidence: L3")
            .replace("Evidence: Not yet collected.", "Evidence: deterministic test output.")
        )
        result = validate(text)
        self.assertIn(
            "VERIFIED missing required section(s): Actual Change Surface, Delivery Retrospective, Knowledge Promotion",
            result.errors,
        )

    def test_verified_accepts_complete_learning_record(self) -> None:
        text = (
            self.fixture("valid.md")
            .replace("Status: APPROVED", "Status: VERIFIED")
            .replace("Result: UNPROVEN", "Result: PASS")
            .replace("Observed evidence: NONE", "Observed evidence: L3")
            .replace("Evidence: Not yet collected.", "Evidence: deterministic test output.")
            + """

## Actual Change Surface

src/events.py [modified]

## Delivery Retrospective

### Implementation Summary

Recent diagnostic events are retained and queryable.

### How It Works

The event store applies the approved retention boundary during persistence.

### Autonomous Decisions

None. Repository conventions determined the implementation.

### Drawbacks and Residual Risks

None known.

### Verification Summary

AC01, AC02, and AC03 pass with deterministic test evidence.

## Knowledge Promotion

- Task-local knowledge retained only in this contract: retention implementation details.
- Knowledge concepts created or updated: none.
- Assets created or updated: none.
"""
        )
        self.assertTrue(validate(text).valid)

    def test_verified_rejects_placeholder_learning_record(self) -> None:
        text = (
            self.fixture("valid.md")
            .replace("Status: APPROVED", "Status: VERIFIED")
            .replace("Result: UNPROVEN", "Result: PASS")
            .replace("Observed evidence: NONE", "Observed evidence: L3")
            .replace("Evidence: Not yet collected.", "Evidence: deterministic test output.")
            + """

## Actual Change Surface

<actual project-relative tree>

## Delivery Retrospective

### Implementation Summary

<what changed>

### How It Works

<how it works>

### Autonomous Decisions

None.

### Drawbacks and Residual Risks

None known.

### Verification Summary

All criteria pass.

## Knowledge Promotion

- Task-local knowledge retained only in this contract: none.
- Knowledge concepts created or updated: <paths or none>
- Assets created or updated: none.
"""
        )
        result = validate(text)
        self.assertIn(
            "VERIFIED section 'Actual Change Surface' must not contain placeholder text",
            result.errors,
        )
        self.assertIn(
            "Delivery Retrospective subsection 'Implementation Summary' must not contain placeholder text",
            result.errors,
        )
        self.assertIn(
            "VERIFIED section 'Knowledge Promotion' must not contain placeholder text",
            result.errors,
        )

    def test_okf_frontmatter_is_required(self) -> None:
        text = self.fixture("valid.md").split("---", 2)[2].lstrip()
        self.assertIn(
            "contract must begin with OKF-compatible YAML frontmatter",
            validate(text).errors,
        )

    def test_okf_frontmatter_requires_contract_type(self) -> None:
        text = self.fixture("valid.md").replace(
            "type: Intentwise Delivery Contract", "type: Architecture"
        )
        self.assertIn(
            "frontmatter type must be 'Intentwise Delivery Contract'",
            validate(text).errors,
        )

    def test_unknown_schema_is_rejected(self) -> None:
        text = self.fixture("valid.md").replace(
            "schema: intentwise/v0.4", "schema: intentwise/v9.9"
        )
        self.assertIn(
            "frontmatter schema must be one of intentwise/v0.2, intentwise/v0.3, intentwise/v0.4",
            validate(text).errors,
        )

    def test_learning_mode_must_be_known(self) -> None:
        text = self.fixture("valid.md").replace("Mode: COMPLETION", "Mode: SOMETIMES")
        self.assertIn(
            "Learning Mode must contain 'Mode: COMPLETION', 'Mode: CHECKPOINTS', or 'Mode: OFF'",
            validate(text).errors,
        )

    def test_learning_mode_inside_fenced_code_is_ignored(self) -> None:
        text = self.fixture("valid.md").replace(
            "Mode: COMPLETION",
            "```text\nMode: COMPLETION\n```",
        )
        self.assertIn(
            "Learning Mode must contain 'Mode: COMPLETION', 'Mode: CHECKPOINTS', or 'Mode: OFF'",
            validate(text).errors,
        )

    def test_current_schema_requires_execution_disposition(self) -> None:
        text = self.fixture("valid.md").replace(
            "\n## Execution\n\nDisposition: CONTINUE\n",
            "",
        )
        self.assertIn("missing required section(s): Execution", validate(text).errors)

    def test_current_schema_requires_target_experience_sections(self) -> None:
        text = re.sub(
            r"\n## Target Experience\n.*?(?=\n## Consequential Decisions\n)",
            "\n",
            self.fixture("valid.md"),
            flags=re.DOTALL,
        )
        self.assertIn(
            "missing required section(s): Target Experience, Interaction States, Experience Rules, Success Scenario",
            validate(text).errors,
        )

    def test_current_schema_rejects_placeholder_outcome(self) -> None:
        text = self.fixture("valid.md").replace(
            "Operators can inspect recent diagnostic events.",
            "TBD.",
        )
        self.assertIn("section 'Outcome' must not contain placeholder text", validate(text).errors)

    def test_inline_code_angle_literal_is_not_a_placeholder(self) -> None:
        text = self.fixture("valid.md").replace(
            "Operators can inspect recent diagnostic events.",
            "Operators can inspect the literal `<missing>` diagnostic value.",
        )
        self.assertTrue(validate(text).valid)

    def test_current_schema_rejects_placeholder_expected(self) -> None:
        text = re.sub(
            r"Expected:.*",
            "Expected: TBD.",
            self.fixture("valid.md"),
            count=1,
        )
        self.assertIn(
            "AC01 Expected must not contain placeholder text",
            validate(text).errors,
        )

    def test_current_schema_rejects_placeholder_target_experience(self) -> None:
        text = self.fixture("valid.md").replace(
            "Diagnostic event -> privacy filter -> 30-day event store -> operator query",
            "TODO",
        )
        self.assertIn(
            "section 'Target Experience' must not contain placeholder text",
            validate(text).errors,
        )

    def test_mermaid_line_breaks_are_literals_not_placeholders(self) -> None:
        for tag in ("<br>", "<br/>", "<br />", "<BR/>"):
            with self.subTest(tag=tag):
                text = re.sub(
                    r"\n## Target Experience\n.*?(?=\n## Interaction States)",
                    '\n## Target Experience\n\n```mermaid\nflowchart LR\n'
                    f'  A["Diagnostic{tag}event"] --> B["Privacy filter"]\n```\n',
                    self.fixture("valid.md"),
                    flags=re.DOTALL,
                )
                self.assertTrue(validate(text).valid, validate(text).errors)

    def test_mermaid_line_break_does_not_hide_real_placeholder(self) -> None:
        text = re.sub(
            r"\n## Target Experience\n.*?(?=\n## Interaction States)",
            '\n## Target Experience\n\n```mermaid\nflowchart LR\n'
            '  A["<starting state><br/>event"] --> B["Privacy filter"]\n```\n',
            self.fixture("valid.md"),
            flags=re.DOTALL,
        )
        self.assertIn(
            "section 'Target Experience' must not contain placeholder text",
            validate(text).errors,
        )

    def test_v02_contract_remains_valid_without_target_experience_sections(self) -> None:
        text = re.sub(
            r"\n## Target Experience\n.*?(?=\n## Consequential Decisions\n)",
            "\n",
            self.fixture("valid.md").replace("schema: intentwise/v0.4", "schema: intentwise/v0.2"),
            flags=re.DOTALL,
        )
        text = re.sub(r"\nPlanned verification:.*", "", text)
        self.assertTrue(validate(text).valid)

    def test_v03_contract_remains_valid_without_planned_verification(self) -> None:
        text = self.fixture("valid.md").replace(
            "schema: intentwise/v0.4", "schema: intentwise/v0.3"
        )
        text = re.sub(r"\nPlanned verification:.*", "", text)
        self.assertTrue(validate(text).valid)

    def test_current_schema_requires_planned_verification(self) -> None:
        text = re.sub(r"\nPlanned verification:.*", "", self.fixture("valid.md"), count=1)
        self.assertIn(
            "AC01 must contain a non-empty Planned verification field",
            validate(text).errors,
        )

    def test_current_schema_rejects_placeholder_planned_verification(self) -> None:
        text = re.sub(
            r"Planned verification:.*",
            "Planned verification: TBD.",
            self.fixture("valid.md"),
            count=1,
        )
        self.assertIn(
            "AC01 Planned verification must not contain placeholder text",
            validate(text).errors,
        )

    def test_current_schema_rejects_conditional_planned_verification(self) -> None:
        text = re.sub(
            r"Planned verification:.*",
            "Planned verification: Map the report when fixture data is available.",
            self.fixture("valid.md"),
            count=1,
        )
        self.assertIn(
            "AC01 Planned verification must not make evidence conditional on availability or feasibility",
            validate(text).errors,
        )

    def test_current_schema_rejects_indirect_conditional_planned_verification(self) -> None:
        for plan in (
            "Planned verification: Use a fixture if one can be found.",
            "Planned verification: Run the mapping check where supported.",
            "Planned verification: Run the mapping check where supported by the environment.",
            "Planned verification: Exercise the operator query unless credentials are unavailable.",
            "Planned verification: Depending on fixture availability, run event queries and assert the retained IDs.",
            "Planned verification: Run event queries depending on the availability of fixture data.",
        ):
            with self.subTest(plan=plan):
                text = re.sub(
                    r"Planned verification:.*",
                    plan,
                    self.fixture("valid.md"),
                    count=1,
                )
                self.assertIn(
                    "AC01 Planned verification must not make evidence conditional on availability or feasibility",
                    validate(text).errors,
                )

    def test_concrete_negative_test_is_not_conditional_verification(self) -> None:
        text = self.fixture("valid.md").replace(
            "Planned verification: Run the event-persistence tests with a payload-bearing fixture "
            "and assert that the stored record contains metadata but no payload body.",
            "Planned verification: Run deterministic persistence tests that attempt to store "
            "an event with a payload body; assert that the stored metadata contains no payload bytes.",
        )
        self.assertTrue(validate(text).valid, validate(text).errors)

    def test_supported_input_cases_are_not_conditional_verification(self) -> None:
        text = re.sub(
            r"^Planned verification:.*$",
            "Planned verification: Run the actual operator query where supported input cases "
            "include empty, recent, and expired event collections; assert exact returned IDs "
            "and no payload bytes.",
            self.fixture("valid.md"),
            count=1,
            flags=re.MULTILINE,
        )
        self.assertTrue(validate(text).valid, validate(text).errors)

    def test_execution_disposition_must_be_known(self) -> None:
        text = self.fixture("valid.md").replace(
            "Disposition: CONTINUE",
            "Disposition: SOMEDAY",
        )
        self.assertIn(
            "Execution must contain 'Disposition: CONTINUE' or 'Disposition: DEFERRED'",
            validate(text).errors,
        )

    def test_lifecycle_directory_rejects_status_and_disposition_mismatches(self) -> None:
        text = self.fixture("valid.md")
        cases = (
            ("drafts", "lifecycle directory 'drafts' is incompatible with status 'APPROVED'"),
            ("ready", "lifecycle directory 'ready' requires Disposition: DEFERRED"),
            ("completed", "lifecycle directory 'completed' is incompatible with status 'APPROVED'"),
        )
        for directory, expected_error in cases:
            with self.subTest(directory=directory):
                path = Path("repo") / ".intentwise" / directory / "contract.md"
                self.assertIn(expected_error, validate(text, path).errors)
        self.assertTrue(
            validate(
                text, Path("repo/.intentwise/active/contract.md")
            ).valid
        )

    def test_legacy_contract_without_schema_or_execution_remains_valid(self) -> None:
        text = (
            self.fixture("valid.md")
            .replace("schema: intentwise/v0.4\n", "")
            .replace("\n## Execution\n\nDisposition: CONTINUE\n", "")
        )
        text = re.sub(r"\nPlanned verification:.*", "", text)
        self.assertTrue(validate(text).valid)

    def test_legacy_execution_when_present_still_respects_lifecycle(self) -> None:
        text = self.fixture("valid.md").replace("schema: intentwise/v0.4\n", "")
        self.assertIn(
            "lifecycle directory 'ready' requires Disposition: DEFERRED",
            validate(text, Path("repo/.intentwise/ready/legacy.md")).errors,
        )
        self.assertTrue(
            validate(text, Path("repo/.intentwise/active/legacy.md")).valid
        )

    def test_pass_requires_concrete_evidence(self) -> None:
        text = (
            self.fixture("valid.md")
            .replace("Result: UNPROVEN", "Result: PASS")
            .replace("Observed evidence: NONE", "Observed evidence: L3")
        )
        result = validate(text)
        self.assertTrue(any("cannot be PASS" in error for error in result.errors))

    def test_pass_rejects_observed_evidence_below_required_level(self) -> None:
        text = (
            self.fixture("valid.md")
            .replace("Result: UNPROVEN", "Result: PASS", 1)
            .replace("Observed evidence: NONE", "Observed evidence: L2", 1)
            .replace("Evidence: Not yet collected.", "Evidence: deterministic test output.", 1)
        )
        self.assertIn(
            "AC01 cannot be PASS because observed L2 is below required L3",
            validate(text).errors,
        )

    def test_fail_requires_observed_evidence(self) -> None:
        text = self.fixture("valid.md").replace("Result: UNPROVEN", "Result: FAIL", 1)
        result = validate(text)
        self.assertIn("AC01 cannot be FAIL with Observed evidence NONE", result.errors)

    def test_duplicate_criterion_ids_are_rejected(self) -> None:
        text = self.fixture("valid.md").replace("AC02", "AC01")
        self.assertIn("acceptance criterion IDs must be unique", validate(text).errors)

    def test_duplicate_required_h2_sections_are_rejected(self) -> None:
        text = self.fixture("valid.md").replace(
            "\n## Outcome\n",
            "\n## Outcome\n\nFirst outcome.\n\n## Outcome\n",
            1,
        )
        self.assertIn("duplicate required section(s): Outcome", validate(text).errors)

    def test_decision_requires_auditable_evidence_basis(self) -> None:
        text = self.fixture("valid.md").replace(
            "Evidence basis: Repository retention conventions and the stated privacy constraint.",
            "Evidence basis:",
        )
        self.assertIn(
            "D001 must contain a non-empty Evidence basis field",
            validate(text).errors,
        )

    def test_decision_requires_sources_and_applicability(self) -> None:
        text = (
            self.fixture("valid.md")
            .replace(
                "Sources: `src/events/`; repository privacy documentation.",
                "Sources:",
            )
            .replace(
                "Applicability: The existing event-store boundary already owns retention and payload filtering.",
                "Applicability:",
            )
        )
        result = validate(text)
        self.assertIn("D001 must contain a non-empty Sources field", result.errors)
        self.assertIn("D001 must contain a non-empty Applicability field", result.errors)

    def test_current_schema_rejects_vague_decision_source(self) -> None:
        text = self.fixture("valid.md").replace(
            "Sources: `src/events/`; repository privacy documentation.",
            "Sources: Repository.",
        )
        self.assertIn(
            "D001 Sources must contain a precise evidence locator",
            validate(text).errors,
        )

    def test_current_schema_rejects_vague_repository_documentation_source(self) -> None:
        text = self.fixture("valid.md").replace(
            "Sources: `src/events/`; repository privacy documentation.",
            "Sources: Repository documentation.",
        )
        self.assertIn(
            "D001 Sources must contain a precise evidence locator",
            validate(text).errors,
        )

    def test_contract_without_decisions_is_valid(self) -> None:
        text = self.fixture("valid.md").replace(
            """### D001 — Retention

Choice: Keep 30 days.

Rationale: This balances diagnosis and privacy.

Evidence basis: Repository retention conventions and the stated privacy constraint.

Sources: `src/events/`; repository privacy documentation.

Applicability: The existing event-store boundary already owns retention and payload filtering.""",
            "None. The repository establishes all relevant behavior.",
        )
        self.assertTrue(validate(text).valid)

    def test_cli_returns_zero_and_disclaims_behavioral_proof(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / "valid.md")],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode)
        self.assertIn("does not prove implementation or runtime behavior", completed.stdout)

    def test_cli_returns_one_for_invalid_contract(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / "invalid.md")],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, completed.returncode)
        self.assertIn("INVALID", completed.stderr)

    def test_cli_returns_two_for_unreadable_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.md"
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(missing)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(2, completed.returncode)


if __name__ == "__main__":
    unittest.main()
