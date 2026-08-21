#!/usr/bin/env python3
"""Validate the structure of an Intentwise Markdown contract."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


STATUSES = {"DRAFT", "APPROVED", "IMPLEMENTED", "VERIFIED"}
RESULTS = {"PASS", "FAIL", "UNPROVEN"}
LEVELS = {"L1", "L2", "L3"}
OBSERVED_LEVELS = {"NONE", *LEVELS}
LEVEL_RANK = {"L1": 1, "L2": 2, "L3": 3}
LEARNING_MODES = {"COMPLETION", "CHECKPOINTS", "OFF"}
CONTRACT_TYPE = "Intentwise Delivery Contract"
REQUIRED_SECTIONS = (
    "Intent",
    "Outcome",
    "Consequential Decisions",
    "Constraints",
    "Delivery Strategy Expectations",
    "Learning Mode",
    "Maintainability Expectations",
    "Acceptance Criteria",
    "Agent Autonomy",
)
VERIFIED_REQUIRED_SECTIONS = (
    "Actual Change Surface",
    "Delivery Retrospective",
    "Knowledge Promotion",
)
RETROSPECTIVE_SUBSECTIONS = (
    "Implementation Summary",
    "How It Works",
    "Autonomous Decisions",
    "Drawbacks and Residual Risks",
    "Verification Summary",
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^Status:\s*(\S+)\s*$", re.MULTILINE)
DECISION_RE = re.compile(r"^###\s+D(\d{3})\s+[—-]\s+(.+?)\s*$", re.MULTILINE)
CRITERION_RE = re.compile(r"^###\s+AC(\d{2,3})\s+[—-]\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")
FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---(?:\s*\r?\n|\Z)", re.DOTALL)


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def _sections(text: str) -> dict[str, str]:
    matches = list(HEADING_RE.finditer(text))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        if len(match.group(1)) != 2:
            continue
        start = match.end()
        end = len(text)
        for following in matches[index + 1 :]:
            if len(following.group(1)) <= 2:
                end = following.start()
                break
        result[match.group(2).strip()] = text[start:end].strip()
    return result


def _field(block: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:[ \t]*(.*?)[ \t]*$", block, re.MULTILINE)
    return match.group(1).strip() if match else None


def _frontmatter_field(frontmatter: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:[ \t]*(.*?)[ \t]*$", frontmatter, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def _subsections(section: str) -> dict[str, str]:
    matches = [match for match in HEADING_RE.finditer(section) if len(match.group(1)) == 3]
    return {
        match.group(2).strip(): section[
            match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(section)
        ].strip()
        for index, match in enumerate(matches)
    }


def _has_placeholder(value: str) -> bool:
    lowered = value.lower()
    return bool(PLACEHOLDER_RE.search(value)) or any(
        phrase in lowered
        for phrase in ("complete after implementation", "not populated until implementation")
    )


def _blocks(section: str, pattern: re.Pattern[str]) -> list[tuple[re.Match[str], str]]:
    matches = list(pattern.finditer(section))
    return [
        (match, section[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(section)].strip())
        for index, match in enumerate(matches)
    ]


def validate(text: str) -> ValidationResult:
    errors: list[str] = []
    frontmatter_match = FRONTMATTER_RE.match(text)
    if not frontmatter_match:
        errors.append("contract must begin with OKF-compatible YAML frontmatter")
    else:
        contract_type = _frontmatter_field(frontmatter_match.group(1), "type")
        if contract_type != CONTRACT_TYPE:
            errors.append(f"frontmatter type must be '{CONTRACT_TYPE}'")

    status_matches = STATUS_RE.findall(text)
    status = status_matches[0] if len(status_matches) == 1 else None
    if len(status_matches) != 1:
        errors.append("contract must contain exactly one 'Status: <value>' line")
    elif status not in STATUSES:
        errors.append(f"invalid status '{status}'; expected one of {', '.join(sorted(STATUSES))}")

    sections = _sections(text)
    missing = [name for name in REQUIRED_SECTIONS if name not in sections]
    if missing:
        errors.append("missing required section(s): " + ", ".join(missing))
    for name in REQUIRED_SECTIONS:
        if name in sections and not sections[name]:
            errors.append(f"section '{name}' must not be empty")

    learning_mode = _field(sections.get("Learning Mode", ""), "Mode")
    if learning_mode not in LEARNING_MODES:
        errors.append(
            "Learning Mode must contain 'Mode: COMPLETION', 'Mode: CHECKPOINTS', or 'Mode: OFF'"
        )

    decisions = _blocks(sections.get("Consequential Decisions", ""), DECISION_RE)
    decision_ids = [match.group(1) for match, _ in decisions]
    if len(decision_ids) != len(set(decision_ids)):
        errors.append("decision IDs must be unique")
    for match, block in decisions:
        identifier = f"D{match.group(1)}"
        if not _field(block, "Choice"):
            errors.append(f"{identifier} must contain a non-empty Choice field")
        if not _field(block, "Rationale"):
            errors.append(f"{identifier} must contain a non-empty Rationale field")
        for field in ("Evidence basis", "Sources", "Applicability"):
            value = _field(block, field)
            if not value:
                errors.append(f"{identifier} must contain a non-empty {field} field")
            elif _has_placeholder(value):
                errors.append(f"{identifier} {field} must not contain placeholder text")

    criteria = _blocks(sections.get("Acceptance Criteria", ""), CRITERION_RE)
    if not criteria:
        errors.append("Acceptance Criteria must contain at least one '### ACnn — title' entry")
    criterion_ids = [match.group(1) for match, _ in criteria]
    if len(criterion_ids) != len(set(criterion_ids)):
        errors.append("acceptance criterion IDs must be unique")

    criterion_results: list[str] = []
    for match, block in criteria:
        identifier = f"AC{match.group(1)}"
        expected = _field(block, "Expected")
        required_level = _field(block, "Required evidence")
        observed_level = _field(block, "Observed evidence")
        result = _field(block, "Result")
        evidence = _field(block, "Evidence")
        if not expected:
            errors.append(f"{identifier} must contain a non-empty Expected field")
        if required_level not in LEVELS:
            errors.append(f"{identifier} Required evidence must be L1, L2, or L3")
        if observed_level not in OBSERVED_LEVELS:
            errors.append(f"{identifier} Observed evidence must be NONE, L1, L2, or L3")
        if result not in RESULTS:
            errors.append(f"{identifier} Result must be PASS, FAIL, or UNPROVEN")
        else:
            criterion_results.append(result)
        placeholder_evidence = evidence.lower().rstrip(".") if evidence else ""
        if result == "PASS" and placeholder_evidence in {"", "none", "n/a", "not yet collected"}:
            errors.append(f"{identifier} cannot be PASS without concrete Evidence")
        if result == "PASS" and observed_level == "NONE":
            errors.append(f"{identifier} cannot be PASS with Observed evidence NONE")
        if (
            result == "PASS"
            and required_level in LEVELS
            and observed_level in LEVELS
            and LEVEL_RANK[observed_level] < LEVEL_RANK[required_level]
        ):
            errors.append(
                f"{identifier} cannot be PASS because observed {observed_level} "
                f"is below required {required_level}"
            )
        if result == "FAIL" and placeholder_evidence in {"", "none", "n/a", "not yet collected"}:
            errors.append(f"{identifier} cannot be FAIL without concrete Evidence")
        if result == "FAIL" and observed_level == "NONE":
            errors.append(f"{identifier} cannot be FAIL with Observed evidence NONE")

    if status == "VERIFIED":
        if criterion_results and any(result != "PASS" for result in criterion_results):
            errors.append("VERIFIED requires every acceptance criterion to be PASS")

        missing_verified = [name for name in VERIFIED_REQUIRED_SECTIONS if name not in sections]
        if missing_verified:
            errors.append("VERIFIED missing required section(s): " + ", ".join(missing_verified))

        for name in VERIFIED_REQUIRED_SECTIONS:
            if name in sections and not sections[name]:
                errors.append(f"VERIFIED section '{name}' must not be empty")
            elif name in sections and _has_placeholder(sections[name]):
                errors.append(f"VERIFIED section '{name}' must not contain placeholder text")

        retrospective = sections.get("Delivery Retrospective", "")
        retrospective_parts = _subsections(retrospective)
        missing_parts = [name for name in RETROSPECTIVE_SUBSECTIONS if name not in retrospective_parts]
        if retrospective and missing_parts:
            errors.append("Delivery Retrospective missing subsection(s): " + ", ".join(missing_parts))
        for name in RETROSPECTIVE_SUBSECTIONS:
            if name in retrospective_parts and not retrospective_parts[name]:
                errors.append(f"Delivery Retrospective subsection '{name}' must not be empty")
            elif name in retrospective_parts and _has_placeholder(retrospective_parts[name]):
                errors.append(
                    f"Delivery Retrospective subsection '{name}' must not contain placeholder text"
                )

    return ValidationResult(tuple(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate an Intentwise contract's Markdown structure (not implementation behavior)."
    )
    parser.add_argument("contract", type=Path, help="path to the contract Markdown file")
    args = parser.parse_args(argv)

    try:
        text = args.contract.read_text(encoding="utf-8")
    except OSError as error:
        print(f"ERROR: cannot read {args.contract}: {error}", file=sys.stderr)
        return 2

    result = validate(text)
    if result.valid:
        print(f"VALID: {args.contract} has a valid Intentwise contract structure.")
        print("NOTE: structural validity does not prove implementation or runtime behavior.")
        return 0

    print(f"INVALID: {args.contract}", file=sys.stderr)
    for error in result.errors:
        print(f"- {error}", file=sys.stderr)
    print("NOTE: this validator checks structure only.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
