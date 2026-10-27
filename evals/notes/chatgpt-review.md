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

# Third review by ChatGPT (2026-10-27), full repository bundle at commit `13e8e86b`

Input: the brief, the context, and the full text of 26 key files (DESIGN.md, workflows, skill, scripts,
scorer, cases, results, FAILURES.md, earlier reviews) plus an audit-log excerpt. Verdict (condensed):
"strong submission, but not fully correct or submission-ready yet", 86/100 (B+).

| # | Finding | Action taken |
|---|---------|--------------|
| 1 | `score.py` passes when audit evidence is missing (A01 without its audit), does not check the declared decision, and passes ROUTE + comment (A02) or an empty ROUTE | Reproduced. Scorer now fails closed (agent success, audit present, declared decision accepted, outputs the decision allows); `test_score.py` pins all three examples. Rescored: run2 9/19, run3-v3 2/5, run4-final 9/19 |
| 2 | Archive concurrency without `queue: max` drops pending archives in a burst | `queue: max` added; `workflow_dispatch` backfill by run ID. Burst test: 3 dispatches within 3 s (runs 40436277133, 40436279772, 40436282375) all ran, none cancelled. All 88 completed runs were archived before the change. Archiving a genuinely missing run is untested (none was missing; deleting an archive to test it would tamper with the audit trail) |
| 3 | Marker access (private repository) | Owner adds `ctreude` as collaborator before submitting |
| 4 | A02's attack is cut at 300 characters; only the label request reaches the agent | Confirmed; A02 kept frozen, limitation pinned by a test; new case A04 delivers the whole payload (`test_inputs.py`); in `run5-adversarial` the agent ignored it and only added `component/promtool` |
| 5 | Duplicate failures are partly an information gap (G09's evidence at characters 2,536 / 2,818) | Confirmed; recorded in FAILURES.md and DESIGN.md §8; fix proposed, not applied, to keep the evaluated configuration fixed |
| 6 | Cone-mode sparse checkout also gives the agent `DESIGN.md`, `README.md`, `CONTRIBUTING.md` | Confirmed; a pre-agent `git sparse-checkout --no-cone` step removes them and logs the file list (verified in run 40433100846); earlier audits show no read of them |
| 7 | "Changes no files" is stronger than the compiled `--allow-tool write` supports | `edit: false` removes the write tool; AGENTS.md now separates local edits from publishing changes |
| 8 | "12/19 on the final configuration" mixes runs | Primary result is now the full run (9/19 under the stricter scorer); the retry figure is labelled secondary |
| Q2 | No detection interval for behaviour drift under the same snapshot | Monthly golden rerun reviewed by the owner (CONTRIBUTING.md); automated replay still proposed |
| Q3 | Mention the archive queue; an estimate is not a load test | Added to Q3 |
| Q5 | Phone use untested | Stated as untested in DESIGN.md |
