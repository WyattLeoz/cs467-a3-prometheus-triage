# Independent review by ChatGPT (2026-10-25)

Input: the workflow source, a summary of SKILL.md, DESIGN.md (commit `90d56876`) and the run2 /
run3-v3 result summaries, with the instruction to act as a strict marker and list (1) ranked gaps
with fixes, (2) controls claimed but not enforced, (3) inaccurate or low-value DESIGN.md lines.
The reply is recorded below in condensed form, followed by what was changed.

## Findings (condensed)

| # | Finding | Action taken |
|---|---------|--------------|
| 1 (critical) | `add-labels.max: 2` limits **calls**, not labels; gh-aw allows 10 labels per call | Verified in gh-aw docs; fixed to `max: 1` + `max-labels: 2` (commit `a8ab68bc`), checked in the compiled lock file and a unit test |
| 2 | G16's expected outcome might contradict the skill (SECURITY row precedes POSSIBLE_DUPLICATE) | Checked: G16 lists publicly published GHSA advisories from an image scan, so it is not an *undisclosed* vulnerability and row 3 does not apply; expectation unchanged, explanation added to DESIGN.md §5 |
| 3 | `triage.py labels` is a procedural check, not an enforced gate | DESIGN.md §2 now says so; enforcement is `allowed`/`blocked` plus gh-aw's rejection of non-existent labels |
| 4 | v3 fixes were re-tested on 5 cases only | Stated in DESIGN.md §8; full rerun of the final configuration attempted as `run4` |
| 5 | Drift detection claimed more strongly than implemented ("one week") | Q2 and §3 rewritten: golden rerun is manual, scheduled replay proposed (needs a PAT) |
| 6 | Q3 did not say what happens to rate-limited issues | Q3 now: not retried, gh-aw opens/updates an `[aw] … hit engine rate limit` issue, bug scrub handles it |
| 7 | Evidence references missing | DESIGN.md cites run IDs, sandbox issue numbers and the expected-outcomes commit `ef169d4a` |
| — | "Deterministic checks cannot be skipped" overstated | Reworded: they always run; the model may still ignore them |
| — | CODEOWNERS is not approval without branch protection | §3 Human approval reworded |
| — | Distinguish 10/19 from 9/18 model-run cases and the 3/5 targeted re-test | §5 updated |
| — | Copilot CLI pinning should be precise | BOM: installed at run time, minimum 1.0.35, not pinned |
