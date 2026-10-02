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
EXECUTION_DISPOSITIONS = {"CONTINUE", "DEFERRED"}
CONTRACT_TYPE = "Intentwise Delivery Contract"
CURRENT_SCHEMA = "intentwise/v0.4"
SUPPORTED_SCHEMAS = {"intentwise/v0.2", "intentwise/v0.3", CURRENT_SCHEMA}
EXPERIENCE_SCHEMAS = {"intentwise/v0.3", CURRENT_SCHEMA}
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
EXPERIENCE_SECTIONS = (
    "Target Experience",
    "Interaction States",
    "Experience Rules",
    "Success Scenario",
)
PREFLIGHT_CONTENT_SECTIONS = (
    "Intent",
    "Outcome",
    "Target Experience",
    "Interaction States",
    "Experience Rules",
    "Success Scenario",
    "Constraints",
    "Delivery Strategy Expectations",
    "Maintainability Expectations",
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
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", re.MULTILINE)
STATUS_RE = re.compile(r"^Status:\s*(\S+)\s*$", re.MULTILINE)
DECISION_RE = re.compile(r"^###\s+D(\d{3})\s+[—-]\s+(.+?)\s*$", re.MULTILINE)
CRITERION_RE = re.compile(r"^###\s+AC(\d{2,3})\s+[—-]\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")
FENCE_LINE_RE = re.compile(r"^[ \t]*(?P<fence>`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(?P<ticks>`+)[^`\n]*(?P=ticks)")
HTML_LINE_BREAK_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
PLACEHOLDER_LINE_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:tbd|todo|to be determined|not yet defined)\.?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
VAGUE_SOURCE_RE = re.compile(
    r"^(?:the\s+)?(?:(?:repository|repo|codebase)(?:\s+(?:documentation|docs))?"
    r"|documentation|docs|task|issue|user request)\.?$",
    re.IGNORECASE,
)
VERIFICATION_RESOURCE_PATTERN = (
    r"(?:fixture(?:\s+data)?|test\s+data|data|artifact|"
    r"environment|service|access|credentials?)"
)
# These catch explicit proof contingencies, not arbitrary test actions or input
# descriptions. Full evidence readiness still requires the semantic preflight.
CONDITIONAL_PLAN_RE = re.compile(
    rf"\b(?:if|when)\s+(?:the\s+)?{VERIFICATION_RESOURCE_PATTERN}"
    r"\s+(?:is|are|becomes?)\s+available\b|"
    r"\bif\s+(?:(?:a|an|the)\s+[\w-]+|one)\s+(?:exists?|can be found)\b|"
    r"\b(?:if|when|where)\s+(?:available|possible|practical|feasible)\b|"
    r"\b(?:if|when|where)\s+supported(?=\s*(?:[.,;:]|$)|\s+(?:by|on|in)\b)|"
    r"\bas\s+(?:available|possible|practical)\b|"
    r"\bsubject to availability\b|"
    rf"\bunless\s+(?:the\s+)?{VERIFICATION_RESOURCE_PATTERN}"
    r"\s+(?:(?:is|are|becomes?)\s+)?(?:unavailable|inaccessible|missing|absent)\b|"
    rf"\b(?:depending|dependent)\s+on\s+(?:the\s+)?{VERIFICATION_RESOURCE_PATTERN}"
    r"\s+availability\b|"
    r"\b(?:depending|dependent)\s+on\s+(?:the\s+)?availability\s+(?:of|for)\s+"
    rf"(?:the\s+)?{VERIFICATION_RESOURCE_PATTERN}\b",
    re.IGNORECASE,
)
FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---(?:\s*\r?\n|\Z)", re.DOTALL)


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def _mask_fenced_code(text: str) -> str:
    """Replace fenced-code characters with spaces while preserving offsets."""

    result: list[str] = []
    active_character: str | None = None
    active_length = 0
    for line in text.splitlines(keepends=True):
        match = FENCE_LINE_RE.match(line)
        if active_character is None:
            if match is None:
                result.append(line)
                continue
            fence = match.group("fence")
            active_character = fence[0]
            active_length = len(fence)
        else:
            stripped = line.strip()
            if (
                stripped
                and set(stripped) == {active_character}
                and len(stripped) >= active_length
            ):
                active_character = None
                active_length = 0
        result.append(
            "".join(character if character in "\r\n" else " " for character in line)
        )
    return "".join(result)


def _sections(text: str) -> dict[str, str]:
    matches = list(HEADING_RE.finditer(_mask_fenced_code(text)))
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
    match = re.search(
        rf"^{re.escape(name)}:[ \t]*(.*?)[ \t]*$",
        _mask_fenced_code(block),
        re.MULTILINE,
    )
    return match.group(1).strip() if match else None


def _frontmatter_field(frontmatter: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:[ \t]*(.*?)[ \t]*$", frontmatter, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def _subsections(section: str) -> dict[str, str]:
    matches = [
        match
        for match in HEADING_RE.finditer(_mask_fenced_code(section))
        if len(match.group(1)) == 3
    ]
    return {
        match.group(2).strip(): section[
            match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(section)
        ].strip()
        for index, match in enumerate(matches)
    }


def _has_placeholder(value: str) -> bool:
    searchable = INLINE_CODE_RE.sub("", value)
    # Mermaid labels use literal HTML line breaks. Keep scanning fenced diagrams
    # for genuine template markers rather than ignoring their entire contents.
    searchable = HTML_LINE_BREAK_RE.sub("", searchable)
    lowered = searchable.lower()
    return bool(
        PLACEHOLDER_RE.search(searchable) or PLACEHOLDER_LINE_RE.search(searchable)
    ) or any(
        phrase in lowered
        for phrase in ("complete after implementation", "not populated until implementation")
    )


def _blocks(section: str, pattern: re.Pattern[str]) -> list[tuple[re.Match[str], str]]:
    matches = list(pattern.finditer(_mask_fenced_code(section)))
    return [
        (match, section[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(section)].strip())
        for index, match in enumerate(matches)
    ]


def _lifecycle_directory(contract_path: str | Path) -> str | None:
    parts = Path(contract_path).parts
    for index in range(len(parts) - 1):
        if parts[index] == ".intentwise":
            candidate = parts[index + 1]
            if candidate in {"drafts", "ready", "active", "completed"}:
                return candidate
    return None


def validate(text: str, contract_path: str | Path | None = None) -> ValidationResult:
    errors: list[str] = []
    structural_text = _mask_fenced_code(text)
    schema: str | None = None
    frontmatter_match = FRONTMATTER_RE.match(text)
    if not frontmatter_match:
        errors.append("contract must begin with OKF-compatible YAML frontmatter")
    else:
        contract_type = _frontmatter_field(frontmatter_match.group(1), "type")
        if contract_type != CONTRACT_TYPE:
            errors.append(f"frontmatter type must be '{CONTRACT_TYPE}'")
        schema = _frontmatter_field(frontmatter_match.group(1), "schema")
        if schema is not None and schema not in SUPPORTED_SCHEMAS:
            errors.append(
                "frontmatter schema must be one of " + ", ".join(sorted(SUPPORTED_SCHEMAS))
            )

    status_matches = STATUS_RE.findall(structural_text)
    status = status_matches[0] if len(status_matches) == 1 else None
    if len(status_matches) != 1:
        errors.append("contract must contain exactly one 'Status: <value>' line")
    elif status not in STATUSES:
        errors.append(f"invalid status '{status}'; expected one of {', '.join(sorted(STATUSES))}")

    sections = _sections(text)
    required_sections = REQUIRED_SECTIONS
    if schema in EXPERIENCE_SCHEMAS:
        required_sections += EXPERIENCE_SECTIONS
    if schema in SUPPORTED_SCHEMAS:
        required_sections += ("Execution",)
    section_names = [
        match.group(2).strip()
        for match in HEADING_RE.finditer(structural_text)
        if len(match.group(1)) == 2
    ]
    duplicate_required = [
        name for name in required_sections if section_names.count(name) > 1
    ]
    if duplicate_required:
        errors.append("duplicate required section(s): " + ", ".join(duplicate_required))
    missing = [name for name in required_sections if name not in sections]
    if missing:
        errors.append("missing required section(s): " + ", ".join(missing))
    for name in required_sections:
        if name in sections and not sections[name]:
            errors.append(f"section '{name}' must not be empty")
        elif (
            schema == CURRENT_SCHEMA
            and name in PREFLIGHT_CONTENT_SECTIONS
            and name in sections
            and _has_placeholder(sections[name])
        ):
            errors.append(f"section '{name}' must not contain placeholder text")

    learning_mode = _field(sections.get("Learning Mode", ""), "Mode")
    if learning_mode not in LEARNING_MODES:
        errors.append(
            "Learning Mode must contain 'Mode: COMPLETION', 'Mode: CHECKPOINTS', or 'Mode: OFF'"
        )

    disposition: str | None = None
    if "Execution" in sections:
        disposition = _field(sections["Execution"], "Disposition")
        if disposition not in EXECUTION_DISPOSITIONS:
            errors.append("Execution must contain 'Disposition: CONTINUE' or 'Disposition: DEFERRED'")

    if contract_path is not None:
        lifecycle = _lifecycle_directory(contract_path)
        allowed_statuses = {
            "drafts": {"DRAFT"},
            "ready": {"APPROVED"},
            "active": {"APPROVED", "IMPLEMENTED"},
            "completed": {"VERIFIED"},
        }
        required_dispositions = {
            "ready": "DEFERRED",
            "active": "CONTINUE",
            "completed": "CONTINUE",
        }
        if lifecycle is not None:
            if status not in allowed_statuses[lifecycle]:
                errors.append(
                    f"lifecycle directory '{lifecycle}' is incompatible with status '{status}'"
                )
            required_disposition = required_dispositions.get(lifecycle)
            # Schema-less legacy records may omit Execution altogether. Enforce
            # its disposition only when required by the schema or supplied.
            if (
                required_disposition is not None
                and (schema in SUPPORTED_SCHEMAS or "Execution" in sections)
                and disposition != required_disposition
            ):
                errors.append(
                    f"lifecycle directory '{lifecycle}' requires Disposition: "
                    f"{required_disposition}"
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
            elif schema == CURRENT_SCHEMA and field == "Sources" and VAGUE_SOURCE_RE.fullmatch(value):
                errors.append(f"{identifier} Sources must contain a precise evidence locator")

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
        planned_verification = _field(block, "Planned verification")
        normalized_plan = planned_verification.lower().rstrip(".") if planned_verification else ""
        observed_level = _field(block, "Observed evidence")
        result = _field(block, "Result")
        evidence = _field(block, "Evidence")
        if not expected:
            errors.append(f"{identifier} must contain a non-empty Expected field")
        elif schema == CURRENT_SCHEMA and _has_placeholder(expected):
            errors.append(f"{identifier} Expected must not contain placeholder text")
        if required_level not in LEVELS:
            errors.append(f"{identifier} Required evidence must be L1, L2, or L3")
        if schema == CURRENT_SCHEMA:
            if not planned_verification:
                errors.append(f"{identifier} must contain a non-empty Planned verification field")
            elif _has_placeholder(planned_verification) or normalized_plan in {
                "none",
                "n/a",
                "tbd",
                "to be determined",
                "not yet planned",
                "not yet collected",
            }:
                errors.append(f"{identifier} Planned verification must not contain placeholder text")
            elif CONDITIONAL_PLAN_RE.search(planned_verification):
                errors.append(
                    f"{identifier} Planned verification must not make evidence conditional "
                    "on availability or feasibility"
                )
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

    result = validate(text, args.contract)
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
