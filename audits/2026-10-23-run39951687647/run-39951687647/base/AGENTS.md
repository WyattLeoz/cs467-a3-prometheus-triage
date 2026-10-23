# AGENTS.md — Prometheus triage sandbox

Repository facts for any coding or triage agent working here. Procedures live in
the skill (`.claude/skills/prometheus-issue-triage/SKILL.md`); hard limits live
in `.github/workflows/issue-triage.md` (permissions and safe outputs).

## What this repository is

A sandbox that mirrors the issue intake of
[prometheus/prometheus](https://github.com/prometheus/prometheus) (Go, Apache-2.0)
so that a GitHub Agentic Workflow can triage replayed historical issues without
touching the real project. It holds the agent configuration, a frozen
representative subset of upstream files, and the evaluation set.

## Build and test commands

This repository (Python 3.11+, stdlib only; `gh` with the `gh-aw` extension v0.93.1):

| Task | Command |
|------|---------|
| Unit-test the skill scripts | `python3 -m unittest discover -s .claude/skills/prometheus-issue-triage/tests -v` |
| Recompile the workflow after editing `issue-triage.md` | `gh aw compile issue-triage` (commit the `.lock.yml` with it) |
| Validate workflow security | `gh aw compile issue-triage --strict` |
| Replay the golden set in a sandbox repo | `python3 evals/golden/run_eval.py --repo OWNER/REPO` |
| Score collected results | `python3 evals/golden/score.py` |
| Inspect a run (audit trail) | `gh aw audit <run-id>` / `gh aw logs issue-triage` |

Upstream Prometheus (useful when judging reports; not built here):

| Task | Command |
|------|---------|
| Go toolchain | Go 1.26 (`go 1.26.9` in upstream `go.mod`) |
| Build server + UI | `make build` (UI only: `make ui-install && make ui-build`) |
| All tests | `make test`; one package: `go test ./tsdb/...` |
| Lint | `make lint` (golangci-lint) |
| Regenerate PromQL parser | `make parser` |

## Project structure

```
.github/workflows/issue-triage.md   agent workflow (source)   -> issue-triage.lock.yml (compiled, do not edit)
.github/ISSUE_TEMPLATE/             upstream issue forms (bug_report.yml, feature_request.yml)
.claude/skills/prometheus-issue-triage/
    SKILL.md                        triage procedure
    scripts/triage.py               deterministic checks: precheck, duplicates, labels
    references/                     label snapshot + policy, component map, other-project list
    tests/                          unit tests for triage.py
data/upstream-issues.jsonl          frozen corpus of upstream issues (2025-07-01 .. 2026-10-22) for duplicate search
upstream/                           upstream files at commit 22c287a (README, MAINTAINERS, SECURITY, CONTRIBUTING, TREE.txt, wiki label page)
evals/golden/                       golden cases, expected outcomes, results and logs (not visible to the agent)
```

Upstream code layout → component label (full table in the skill's `references/component-map.md`):
`promql/` promql · `tsdb/` tsdb · `tsdb/agent` agent · `scrape/`, `model/textparse` scraping ·
`discovery/<provider>` service discovery · `storage/remote` remote storage (`otlptranslator` → otlp) ·
`rules/` rules · `notifier/` notify · `web/api` api · `web/ui` ui · `cmd/promtool` promtool ·
`config/` config · `documentation/prometheus-mixin` mixin · `docs/` documentation.

## Conventions

- Upstream label meanings (wiki "Label Names and Descriptions"): `kind/bug` = a **confirmed** bug;
  `kind/more-info-needed` = author must supply information; `kind/question` = usage question best
  asked in community channels; `priority/P0..P3, Pmaybe` = maintainer scheduling decisions.
- Upstream triage happens in maintainers' periodic "bug scrub"; this agent only prepares issues for it.
- Usage questions go to https://prometheus.io/community/ ; suspected vulnerabilities are reported
  privately per https://prometheus.io/docs/operating/security/ .
- Bug reports use the form in `.github/ISSUE_TEMPLATE/bug_report.yml` (what you did, expected,
  observed, system information, Prometheus version, configuration, logs).
- Refer to upstream issues as `prometheus/prometheus#NNNN`; this sandbox's own numbers differ.
- Upstream PR conventions (title `area: description`, DCO sign-off, `release-notes` block) are in
  `upstream/AGENTS.upstream.md`.

## Forbidden changes

- The triage agent changes **no files** and **no repository settings**. Its only outputs are one
  comment, up to two labels from the allowlist, or a no-op — enforced by the workflow, not by this file.
- Never close, reopen, lock, transfer, delete or edit issues; never merge or push. (The workflow has
  `issues: read`, `contents: read`, and no such safe outputs.)
- Never hand-edit `*.lock.yml`; change `issue-triage.md` and recompile.
- Never edit `evals/golden/cases.json` or `evals/golden/adversarial.json` after a run has been recorded;
  add a new case or a new dated result instead.
- Do not modify `data/upstream-issues.jsonl` except to refresh it with a dated snapshot in its own commit.
- Changes to `.github/`, `.claude/`, `AGENTS.md` and `CONTRIBUTING.md` require review by a CODEOWNER.
