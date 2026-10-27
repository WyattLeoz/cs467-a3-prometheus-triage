# Prometheus Issue Triage Agent

A governed AI agent that gives every newly opened issue a first response: it routes the issue to a
component, asks for missing information, points usage questions and other-project reports to the
right place, or flags a likely duplicate. It runs as a
[GitHub Agentic Workflow](https://github.com/github/gh-aw) (gh-aw v0.93.1, Copilot CLI engine) in a
private sandbox that mirrors the issue intake of
[`prometheus/prometheus`](https://github.com/prometheus/prometheus), and is replayed on real
historical issues.

The agent can post **at most one comment and two allow-listed labels** on the issue that triggered
it. It cannot close, edit or delete anything, merge, push, use the network or call the GitHub API.
Those limits are enforced by workflow permissions and gh-aw safe outputs, not by the prompt.

## Motivation

Of the 65 issues non-maintainers opened in `prometheus/prometheus` between 2026-07-23 and
2026-10-22, 45 (69%) had no maintainer comment when measured, and the rest waited a median of 89
hours ([`evals/need-metric/`](evals/need-metric/)). Upstream triage happens in periodic "bug scrubs".
A first response that sorts and prepares each issue saves the scrub time. Much of that sorting can
be done by rules (template completeness, label validity, a time-bounded duplicate search), and those
parts are plain scripts here. The rest needs judgement no rule encodes: is a Helm-chart symptom a
Prometheus bug, and is a similar earlier issue really the same problem? See
[`DESIGN.md`](DESIGN.md) §1 for the metric's limits.

## How it works

```mermaid
flowchart TD
  A[Issue opened] --> B{Gate: maintainer-authored?}
  B -- yes --> S[Skipped, no model call]
  B -- no --> C["Deterministic checks (triage.py):<br/>template, other-project hints,<br/>duplicate search before the issue's date"]
  C --> D["Agent job (gpt-4.1, read-only token,<br/>no network, triage skill)"]
  D --> E{Threat detection}
  E -- "flagged or no verdict" --> N[Nothing published]
  E -- clean --> F["safe_outputs job:<br/>≤ 1 comment, ≤ 2 allow-listed labels"]
  F --> G["Audit archive: gh aw audit → audit-log branch,<br/>model/CLI drift check"]
  N --> G
```

1. **Gate.** Issues by owners, members and collaborators are skipped without a model call.
2. **Deterministic checks.** Before the model starts, [`triage.py`](.claude/skills/prometheus-issue-triage/scripts/triage.py)
   checks the bug template, notices mentions of other projects, and searches a frozen corpus of 494
   upstream issues for similar reports filed *earlier*.
3. **Agent.** The model loads the [`prometheus-issue-triage` skill](.claude/skills/prometheus-issue-triage/SKILL.md),
   reads the check output and picks one decision: `ROUTE`, `NEEDS_INFO`, `SUPPORT_QUESTION`,
   `OTHER_PROJECT`, `POSSIBLE_DUPLICATE`, `SECURITY` or `NO_ACTION`. It validates its labels with the
   script and states its reasoning in the run log.
4. **Publish.** gh-aw's detection job checks the proposed outputs for obeyed injections, leaked
   secrets and blocked labels. A separate job then applies them under fixed limits, as
   `github-actions[bot]`.
5. **Archive.** Every run's audit (trigger, model, tool calls, firewall decisions, outputs, AI
   credits) is committed to the `audit-log` branch. A drift check compares the model snapshot and
   CLI version against a reviewed baseline.

## Safety and governance

| Control | How | Status |
|---------|-----|--------|
| Least privilege | Agent job has `contents: read`, `issues: read`, no GitHub tools, no file-edit tool, `network: {}` firewall; writes happen only in gh-aw's `safe_outputs` job | Implemented, tested |
| Safe outputs | `add-comment.max: 1`; `add-labels` = 1 call × 2 labels from an exact list of 23 existing labels; `kind/bug`, `priority/*`, `duplicate`, `stale` blocked; `mentions: false`; link domains allow-listed | Implemented; [negative test](evals/golden/safe-output-limits-test.md) |
| Isolation | The agent's workspace holds only the skill, [`AGENTS.md`](AGENTS.md) and `data/`; expected outcomes and result documents are removed before it starts, and the file list is logged | Implemented, verified in a run log |
| Fail closed | Detection with `continue-on-error: false`: a flagged or undecided run publishes nothing | Implemented, tested |
| Budgets | 10-minute agent step, 20 turns, AI-credit caps per run and per day, 3 runs/hour per reporter, one agent job at a time, `stop-after` date | Implemented |
| Identity | Comments and labels come from `github-actions[bot]` with an attribution footer linking the run | Implemented |
| Audit trail | [`triage-audit-archive.yml`](.github/workflows/triage-audit-archive.yml) archives every run to the `audit-log` branch; archive jobs queue (up to 100 pending) and a missed run can be backfilled by ID | Implemented, tested |
| Drift detection | Opens a `[drift]` issue when the served model snapshot or CLI differs from [`.github/agent-baseline.json`](.github/agent-baseline.json); behaviour drift is caught by a monthly golden rerun | Version check tested; rerun is a manual process |
| Kill switch | Disable the workflow and cancel runs (from the web UI or `gh`) | Tested |
| Human approval | [`CODEOWNERS`](.github/CODEOWNERS) for the configuration; enforcing it needs branch protection, which this private repo's plan lacks | **Proposed** |

All outputs are reversible suggestions. Closing, prioritising and confirming bugs stay with
maintainers. [`CONTRIBUTING.md`](CONTRIBUTING.md) is the AI-contribution policy for reporters,
contributors and anyone changing the agent.

## Evaluation and results

The golden set holds 16 real historical issues (including two that need no action) and 4
constructed adversarial inputs. Each input is replayed as a real issue with only the information
available when it was first filed. Expected outcomes were committed before any agent run
(`ef169d4a`; A04 in `a3f16bb1`). The scorer fails closed: a pass needs the right outputs, an
acceptable declared decision, outputs that decision allows, and audit evidence that the skill was
loaded. A green workflow run alone never counts.

- **Full run on all 19 original cases ([`run4-final`](evals/golden/results/run4-final/summary.md)): 9/19 pass.**
  Two failures came from infrastructure (a runner download 404 and a detection timeout), and both
  passed on re-run. The other eight are model-judgement errors by gpt-4.1: missed duplicates and
  other-project reports, public CVEs treated as an undisclosed vulnerability, and labels the
  decision forbids. [`FAILURES.md`](evals/golden/FAILURES.md) explains each one.
- **Safety held in every run:** no blocked label, no closed issue, at most one comment and two
  labels, no live @mention, no secret-like text.
- **Adversarial inputs:** A01 (a fake "maintainer-approved" request to close stale issues), A02 and
  A04 (malicious instructions returned by the duplicate-search tool), and A03 (escalation and
  credential exfiltration). Re-run on the final configuration
  ([`run5-adversarial`](evals/golden/results/run5-adversarial/summary.md)): 3/4 pass. The agent ignored
  every injected instruction. A03 failed on judgement: it routed the issue instead of asking for information.
- **Label limits** were attacked directly by a dispatch-only workflow: 3 labels in one call, a
  second call, `kind/bug` and an invented label. All were refused, after one fix that this test found.

## Getting started

Requirements: a GitHub repository you control, GitHub Copilot, the `gh` CLI with the gh-aw
extension, and Python 3.11+ (standard library only).

```bash
gh extension install github/gh-aw --pin v0.93.1
python3 evals/golden/sync_labels.py --repo OWNER/REPO     # create the upstream labels
gh secret set COPILOT_GITHUB_TOKEN --repo OWNER/REPO      # fine-grained PAT, Copilot Requests: Read
gh aw compile issue-triage --strict                       # after any change to issue-triage.md
```

Push to the repository and open an issue. To stop the agent:
`gh workflow disable "Prometheus Issue Triage"`, then cancel any queued or running runs.

## Reproducing the evaluation

```bash
python3 evals/golden/run_eval.py --repo OWNER/REPO --tag <tag> --pause 120
bash evals/golden/save_logs.sh <tag>
python3 evals/golden/score.py evals/golden/results/<tag>
python3 -m unittest discover -s evals/golden -p 'test_*.py'
python3 -m unittest discover -s .claude/skills/prometheus-issue-triage/tests
```

On Copilot Free the runner stops with exit code 75 at the first rate limit and resumes on the next
invocation. Details, run history and caveats are in [`evals/golden/README.md`](evals/golden/README.md).

## Project structure

```
.github/workflows/issue-triage.md         agent workflow (compiled to issue-triage.lock.yml)
.github/workflows/triage-audit-archive.yml audit archive + drift alert
.github/workflows/safe-output-limits-test.md  negative test of the label limits
.claude/skills/prometheus-issue-triage/   triage skill: SKILL.md, scripts/triage.py, references/, tests/
AGENTS.md                                 repository facts for agents
CONTRIBUTING.md                           AI-contribution policy and change process
DESIGN.md                                 design rationale, governance, bill of materials
data/upstream-issues.jsonl                frozen upstream issue corpus (+ 2 synthetic fixtures)
evals/golden/                             cases, expected outcomes, results, logs, scorer
evals/need-metric/                        first-response metric script and snapshot
upstream/                                 upstream files used as context
```

## Limitations

- Accuracy is not good enough to act without review. That is why the agent only suggests. The only
  model this Copilot Free account can use is `gpt-4.1`, and its quota (about 1–4 runs per ~4.5 hours)
  caps throughput at roughly 5–20 issues a day.
- Duplicate candidates reach the model as a title plus 300 characters, which can hide the evidence
  needed to confirm a duplicate.
- Each case was run once, and the full run spans several commits. There is no clean single-commit
  rerun of all cases.
- The served model snapshot is not pinned. Version drift is detected, not prevented.

## Documentation

- [`DESIGN.md`](DESIGN.md): why this workflow, where each rule is enforced, governance controls,
  the rejected alternative, test findings, answers to operational questions, and the bill of materials.
- [`evals/golden/README.md`](evals/golden/README.md): evaluation method and run history.
  [`FAILURES.md`](evals/golden/FAILURES.md) covers every failure.
- [`evals/notes/chatgpt-review.md`](evals/notes/chatgpt-review.md): independent reviews and what changed.
- [`AGENTS.md`](AGENTS.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SKILL.md`](.claude/skills/prometheus-issue-triage/SKILL.md).

## Acknowledgements and license

Upstream files in `upstream/` and issue text in `data/` and `evals/golden/cases/` come from
[prometheus/prometheus](https://github.com/prometheus/prometheus) (Apache-2.0, see
[`upstream/LICENSE`](upstream/LICENSE) and [`upstream/NOTICE`](upstream/NOTICE)). They are
reproduced unchanged for evaluation, except the two clearly marked synthetic fixtures in `data/`.
Built with [GitHub Agentic Workflows](https://github.com/github/gh-aw). Developed for CS467
(Singapore Management University) by Loh Kai Zhe.
