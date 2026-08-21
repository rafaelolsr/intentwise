# Example — Trivial typo (no interview)

## Request

“Fix the misspelling ‘occured’ in the existing empty-state message.”

## Repository-first finding

The message appears once, its expected spelling is covered by a snapshot, and no identifier, API value, or localization key changes.

## Intentwise response

No consequential decision exists. Fix the text, update the snapshot if needed, run the focused test, and report the evidence. Do not create an `.intentwise/active/` contract and do not ask a question.

## Verification

- `PASS` at L2 if the focused snapshot test passes and the old spelling is absent.
- `UNPROVEN` if the test cannot be run; a code-edit claim alone is L0.
