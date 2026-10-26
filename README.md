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
| Audit trail + drift alert | [`triage-audit-archive.yml`](.github/workflows/triage-audit-archive.yml) → `audit-log` branch; baseline [`.github/agent-baseline.json`](.github/agent-baseline.json) |
| Negative test of label limits | [`safe-output-limits-test.md`](.github/workflows/safe-output-limits-test.md) |
| Independent review | [`evals/notes/chatgpt-review.md`](evals/notes/chatgpt-review.md) |
| Golden set, expected vs actual, logs | [`evals/golden/`](evals/golden/README.md) |
| Upstream subset used as context | [`upstream/`](upstream/), [`data/upstream-issues.jsonl`](data/upstream-issues.jsonl) |

## Where each requirement is answered

| Requirement | Answer | Evidence |
|-------------|--------|----------|
| Workflow choice, need metric, period, limitations, why an agent | [DESIGN §1](DESIGN.md#1-workflow-and-evidence-of-need) | [`evals/need-metric/`](evals/need-metric/) |
| Trigger, permissions, tools, safe outputs + limits, timeout, network; cannot close/merge/push | [`issue-triage.md`](.github/workflows/issue-triage.md), [DESIGN §2](DESIGN.md#2-where-each-rule-lives) | compiled [`issue-triage.lock.yml`](.github/workflows/issue-triage.lock.yml); [limits test](evals/golden/safe-output-limits-test.md) |
| AGENTS.md (build/test, structure, conventions, forbidden changes) | [`AGENTS.md`](AGENTS.md) | — |
| Skill, scripts, deterministic checks; agent loads and uses the skill | [`SKILL.md`](.claude/skills/prometheus-issue-triage/SKILL.md), [`triage.py`](.claude/skills/prometheus-issue-triage/scripts/triage.py) | unit tests in `tests/`; "skill loaded" check in every `results/*/summary.md`; `✓ skill(...)` in each `logs/*/*/log.md` |
| AI-contribution policy | [`CONTRIBUTING.md`](CONTRIBUTING.md) | — |
| ≥ 10 historical cases incl. no-action, context before the event, expectations fixed first | [`cases.json`](evals/golden/cases.json), [eval README](evals/golden/README.md) | expectations committed in `ef169d4a` before any run |
| Adversarial inputs | [`adversarial.json`](evals/golden/adversarial.json) (A01–A03) | results A01–A03 in each run |
| Every case compared, every failure explained | [`results/<run>/summary.md`](evals/golden/results/), [`FAILURES.md`](evals/golden/FAILURES.md) | [`logs/`](evals/golden/logs/), `audit-log` branch |
| Governance controls, implemented vs proposed, untrusted inputs, actions | [DESIGN §3](DESIGN.md#3-governance-controls) | kill-switch, drift (#72) and limits tests cited there |
| Five questions | [DESIGN §6](DESIGN.md#6-five-questions) | Q1 = A01, Q4 = A02 |
| Rejected alternative, deliberate limits, findings, unresolved | [DESIGN §4, §5, §8](DESIGN.md) | — |
| Bill of materials, AI-use statement | [DESIGN §7, §9](DESIGN.md#7-agent-bill-of-materials) | — |
| Reproduce the evaluation | [eval README → Reproduce](evals/golden/README.md#reproduce) | `run_eval.py`, `score.py`, `save_logs.sh` |

Upstream files in `upstream/` and issue text in `data/` and `evals/golden/cases/`
come from prometheus/prometheus (Apache-2.0, see `upstream/LICENSE` and
`upstream/NOTICE`); they are reproduced unchanged for evaluation.
