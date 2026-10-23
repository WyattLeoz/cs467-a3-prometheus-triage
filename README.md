# CS467 A3 — Governed issue-triage agent for Prometheus

A GitHub Agentic Workflow (gh-aw, Copilot engine) that gives every newly opened
issue in a **sandbox mirror of `prometheus/prometheus`** a first-response triage:
route it to a component, ask for missing information, point usage questions and
other-project reports to the right place, or flag a likely duplicate. It can post
at most one comment and two allow-listed labels; it cannot close, edit or delete
anything.

**Start with [`DESIGN.md`](DESIGN.md)** — justification, governance controls,
agent bill of materials, test findings and the five assignment questions.

| Deliverable | Where |
|-------------|-------|
| Workflow (source + compiled) | [`.github/workflows/issue-triage.md`](.github/workflows/issue-triage.md), [`issue-triage.lock.yml`](.github/workflows/issue-triage.lock.yml) |
| Repository instructions | [`AGENTS.md`](AGENTS.md) |
| Skill + scripts + tests | [`.claude/skills/prometheus-issue-triage/`](.claude/skills/prometheus-issue-triage/SKILL.md) |
| AI-contribution policy | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Human approval on config | [`.github/CODEOWNERS`](.github/CODEOWNERS) |
| Golden set, expected vs actual, logs | [`evals/golden/`](evals/golden/README.md) |
| Upstream subset used as context | [`upstream/`](upstream/), [`data/upstream-issues.jsonl`](data/upstream-issues.jsonl) |

Upstream files in `upstream/` and issue text in `data/` and `evals/golden/cases/`
come from prometheus/prometheus (Apache-2.0, see `upstream/LICENSE` and
`upstream/NOTICE`); they are reproduced unchanged for evaluation.
