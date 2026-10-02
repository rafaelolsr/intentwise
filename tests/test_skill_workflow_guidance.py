from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SKILL = ROOT / "skills" / "intentwise" / "SKILL.md"
CONTRACT_TEMPLATE = (
    ROOT / "skills" / "intentwise" / "references" / "contract-template.md"
)


class SkillWorkflowGuidanceTests(unittest.TestCase):
    def test_ready_requires_semantic_preflight_not_structural_success(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("Structural validity is not semantic readiness", skill)
        self.assertIn("Never return `READY` from structural validator success alone", skill)
        self.assertIn("Structural validity is not semantic readiness", readme)
        self.assertIn("`READY` requires the complete source-derived semantic preflight", readme)

    def test_direct_ado_flow_is_default_and_two_step_is_audit_only(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("one direct Intentwise invocation by default", skill)
        self.assertIn("two-step prompt-generation flow is optional audit/debug mode", skill)
        self.assertIn("## Default ADO workflow", readme)
        self.assertIn("directly at the Azure DevOps work item", readme)
        self.assertIn("two-step prompt-generation flow is optional audit/debug mode", readme)
        self.assertIn("it is not the daily default", readme)

    def test_preapproval_authoring_cannot_mutate_product_or_worktree(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("authoring and review are read-only for the product", skill)
        self.assertIn(
            "Do not create, switch, or redirect work to another worktree",
            skill,
        )
        self.assertIn("report an approval-boundary", skill)
        self.assertIn("the product worktree is read-only", readme)

    def test_new_acceptance_criteria_record_precise_authority_sources(self) -> None:
        template = CONTRACT_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn(
            "Sources: <precise authority locators for the normative "
            "commitments covered by this criterion>",
            template,
        )


if __name__ == "__main__":
    unittest.main()
