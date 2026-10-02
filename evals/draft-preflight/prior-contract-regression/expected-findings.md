# Expected Approval-Readiness Findings

The preflight should report `NEEDS REVISION`, not `BLOCKED`, because authoritative sources establish every correction:

1. Preserve visible transformation identity or grouped count on collapsed relationships instead of requiring selection to discover that a transformation exists.
2. Preserve explicit unresolved unknown origins before Bronze; current code or tests cannot silently supersede the verified requirement.
3. Add an acceptance criterion that exercises **Show transformations** in both directions and proves collapsed/expanded semantic equivalence.
4. Keep the right-side relationship panel improvement because it is the current regression task's additive requirement.

In authoring mode, the same findings must be repaired automatically before the draft is presented. The agent must not ask the user to re-decide behavior already established by the verified contract.
