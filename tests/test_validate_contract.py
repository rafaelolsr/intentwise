from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "intentwise" / "scripts" / "validate_contract.py"
FIXTURES = Path(__file__).parent / "fixtures"
GOLDEN_CONTRACT = (
    ROOT
    / "examples"
    / "golden-delivery"
    / ".intentwise"
    / "completed"
    / "IW-204-evidence-integrity.md"
)
sys.path.insert(0, str(SCRIPT.parent))

from validate_contract import validate  # noqa: E402


class ContractValidationTests(unittest.TestCase):
    def fixture(self, name: str) -> str:
        return (FIXTURES / name).read_text(encoding="utf-8")

    def test_valid_contract(self) -> None:
        self.assertTrue(validate(self.fixture("valid.md")).valid)

    def test_golden_completed_contract_is_valid(self) -> None:
        self.assertTrue(validate(GOLDEN_CONTRACT.read_text(encoding="utf-8")).valid)

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

    def test_learning_mode_must_be_known(self) -> None:
        text = self.fixture("valid.md").replace("Mode: COMPLETION", "Mode: SOMETIMES")
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

    def test_execution_disposition_must_be_known(self) -> None:
        text = self.fixture("valid.md").replace(
            "Disposition: CONTINUE",
            "Disposition: SOMEDAY",
        )
        self.assertIn(
            "Execution must contain 'Disposition: CONTINUE' or 'Disposition: DEFERRED'",
            validate(text).errors,
        )

    def test_legacy_contract_without_schema_or_execution_remains_valid(self) -> None:
        text = (
            self.fixture("valid.md")
            .replace("schema: intentwise/v0.2\n", "")
            .replace("\n## Execution\n\nDisposition: CONTINUE\n", "")
        )
        self.assertTrue(validate(text).valid)

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
