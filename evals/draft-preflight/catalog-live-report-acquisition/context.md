# Catalog Live-Report Acquisition Evaluation Context

Use the Intentwise draft-readiness preflight to review `draft-before.md`. Treat the following as authoritative source commitments for the evaluation:

- Task 3973868 adds live catalog report acquisition while preserving existing local PBIP behavior.
- Behavioral proof must use workspace `fcda3e25-80c0-451a-bec3-4022efe2b125`, report `c4cdbb71-7abf-4a89-8f54-13731277db3a` (OOS Compute), and selected page `b4769d06e38e08ab91d4` from the supplied Power BI URL.
- A successful live acquisition reports source format PBIP, produces non-empty normalized in-memory PBIP files, and creates no temporary PBIP directory.
- When every explicitly configured live report fails, the acquisition stage fails with a categorized, redacted aggregate error. It cannot return an empty successful result or let the catalog report successful live acquisition.
- Local `--pbip-root` and live report inputs are mutually exclusive for Task 3973868. Configuring both is an explicit configuration error; merging them is out of scope.
- Task 3973868 preserves intrinsic page and visual identifiers in normalized definition material. Task 3973869 interprets those identifiers and creates visual usage records.
- No feature flag, persistence, dedicated projection, graph, API, or UI work belongs to Task 3973868.
