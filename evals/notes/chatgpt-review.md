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

# Second review by ChatGPT (2026-10-26), against the full assignment brief

Input: the brief, the workflow, SKILL.md, AGENTS.md, CONTRIBUTING.md, DESIGN.md and all results.
Verdict (condensed): "strong governance and safety design"; requirements met except "partly" for
the unfinished final rerun, the explanation of failures, Q3 and some wording.

| Finding | Action taken |
|---------|--------------|
| run4 unfinished and spans several config commits | Each result now records `config_sha` (shown in every `summary.md`); remaining cases run; the infrastructure (A01) and detection (G02) failures are re-run on the final commit as `run4-retry` |
| Failures should be grouped and counted | `evals/golden/FAILURES.md`: every failure with cause and category (judgement / configuration / availability) |
| Add worked examples to SKILL.md for G04, G08, G09/G10 | Not done on purpose: examples drawn from the golden cases would tune the agent on its own test set; listed as unresolved instead |
| Q3 ignores the 100-pending-run cap of `queue: max` | Checked against the GitHub changelog (2026-05-07); Q3 updated |
| "gpt-4.1 pinned", "no token", "every run archived" too strong | BOM: name fixed, snapshot not pinned; Q4: no write token in the sandbox; audit row cites A01's archived startup failure |
| Budget should mention cost | Budgets row: no money spent (Copilot Free, Actions minutes of a private repo) |
