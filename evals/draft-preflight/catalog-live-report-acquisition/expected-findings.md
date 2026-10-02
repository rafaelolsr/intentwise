# Expected Approval-Readiness Findings

The preflight should report `NEEDS REVISION`, not `READY`, for these four blocking defects:

1. **AC08 has a target-specificity loophole.** It permits any accessible report even though the authoritative behavioral target is OOS Compute in workspace `fcda3e25-80c0-451a-bec3-4022efe2b125`, report `c4cdbb71-7abf-4a89-8f54-13731277db3a`, selected page `b4769d06e38e08ab91d4`. Both `Expected` and `Planned verification` must bind the L3 scenario to that target.
2. **AC05 leaves total-failure semantics ambiguous.** “Cannot appear successful” does not require the live-acquisition stage to fail and may permit an empty degraded result. It must require a categorized, redacted aggregate error and prohibit an empty result or a successful live-acquisition outcome.
3. **AC01 omits the combined-input state.** Local `--pbip-root` and live inputs must be explicitly mutually exclusive, with deterministic L2 coverage proving that configuring both returns a configuration error. Silent precedence and merging are out of scope.
4. **AC04 leaks downstream scope.** “Extracted page and visual identity” can pull interpretation into Task 3973868. The criterion must say that normalized definition material preserves intrinsic identifiers for downstream extraction, while Task 3973868 neither interprets them nor creates visual usage records.

The reviewer may phrase these findings differently, but it must preserve their behavioral consequence and avoid introducing unrelated implementation requirements.
