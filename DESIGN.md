# DESIGN — Governed first-response triage for Prometheus

## 1. Workflow and evidence of need

**Workflow:** first-response triage of newly opened issues in `prometheus/prometheus`,
replayed in this private sandbox. The agent routes an issue to a component, asks for
missing information, redirects usage questions and other-project reports, or flags a
likely duplicate — so the maintainers' periodic bug scrub starts from prepared issues.

**Measured** (`evals/need-metric/compute.py`, GitHub REST API, issues opened
2026-07-23 → 2026-10-22, captured 2026-10-23):
- 65 issues opened by non-maintainers; **45 (69%) had no maintainer comment**; the 20
  that had one waited a median **89 h**.
- Of the 37 issues at least 30 days old, **21 (57%)** still had no maintainer comment.
- 59 of 65 carried no label, although upstream CONTRIBUTING says issues are "regularly tagged".

**Limitations:** "maintainer" = comment author association OWNER/MEMBER/COLLABORATOR
(org members who are not maintainers count; maintainers acting through labels, closing,
linked PRs or Slack do not); recent issues are right-censored; a single snapshot, not a
trend; comment counts include contributors claiming issues, so raw "no comment" figures
understate the gap.

## 2. Why an agent rather than conventional automation

Keyword labelers and template linters already cover the mechanical parts, and this design
keeps those parts deterministic (gate, template completeness, label validation,
time-bounded duplicate search in `triage.py`). What remains needs judgement that rules
cannot encode: whether "kube-prometheus-stack creates no StatefulSet" is a Prometheus bug or
a Helm-chart issue, whether a lexically similar earlier issue is the *same* symptom, and
whether a template with empty fields is still actionable because it names the exact code
path. The model only picks one of seven decisions and writes one short comment.

## 3. Where each rule is enforced

| Rule | Enforced by |
|------|-------------|
| Cannot close, edit, delete, lock, merge or push | Agent job `contents: read`, `issues: read`; no close/update/PR safe outputs (`issue-triage.md`) |
| ≤ 1 comment, ≤ 2 labels, only on the triggering issue | `add-comment.max: 1`, `add-labels.max: 2`, `target: triggering` |
| Never `kind/bug` (= *confirmed*), `priority/*`, `duplicate`, `won't fix` | `add-labels.allowed` / `blocked` globs; mirrored by `triage.py labels` + unit test |
| No pings, foreign links or upstream timeline noise | `mentions: false`, `allowed-domains`, `allowed-github-references: ["repo"]` |
| No exfiltration path | `network: {}` (AWF firewall), `tools.github: false`, bash allowlist |
| Maintainer-authored issues are not triaged | Deterministic `on.steps` gate — no model call |
| Agent cannot see expected outcomes | `checkout.sparse-checkout` excludes `evals/` |
| Unsafe output is never published | `threat-detection.continue-on-error: false` |
| Decision procedure, comment rules | `SKILL.md` (procedure only) |
| Build/test commands, structure, label meanings | `AGENTS.md` (facts only) |

## 4. Governance controls

RESULTS-PENDING

## 5. Untrusted inputs and possible actions

RESULTS-PENDING

## 6. Test results

RESULTS-PENDING

## 7. Five questions

RESULTS-PENDING

## 8. Agent bill of materials

RESULTS-PENDING

## 9. Unresolved

RESULTS-PENDING

## 10. AI-use statement

RESULTS-PENDING
