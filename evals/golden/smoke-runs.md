# Smoke runs before the golden evaluation (2026-10-23)

Sandbox issues #1, #3, #6–#15 are smoke tests (a promtool feature request that is *not* a
golden case). Issues #2, #4, #5 were opened automatically by gh-aw's failure reporting.
Each run's full audit is on the `audit-log` branch (`audits/<date>-run<id>/`).

| Run | Config change under test | What happened | Consequence |
|-----|--------------------------|---------------|-------------|
| 39908966795 | First run, `COPILOT_GITHUB_TOKEN` not yet set | Activation stopped at *Validate COPILOT_GITHUB_TOKEN secret*; nothing posted; gh-aw opened failure issue #2 | Fail-closed, alerting works |
| 39931152982 | `copilot-requests: write` (keyless, Actions token) with `claude-sonnet-4.5` | `model_not_supported` | — |
| 39931953463 | keyless with `gpt-5-mini` | `model_not_supported` | Keyless org-billed inference unavailable for a personal-account repo; reverted to the PAT (`copilot-requests: none`) |
| 39943214109 | PAT, `claude-sonnet-4.5` | Token accepted; `400 The requested model is not supported` | — |
| 39944046261 / 39944759869 / 39946181522 | `claude-sonnet-5.5`, `auto`, engine default | Same 400 (auto/default resolved to `claude-sonnet-5.5`) | — |
| 39945330955 | `gpt-5.6-luna` + fallback chain | All rejected | — |
| 39946827890 | `claude-haiku-4.5` | Same 400 | Diagnosed with a temporary workflow (`evals/notes/copilot-access-diagnostic.md`): token owner is on **Copilot Free** (`free_limited_copilot`, 0 premium interactions, no org); only `gpt-4.1` is callable through the `agentic-workflows` integration |
| 39948066734 | `gpt-4.1` pinned | Run **succeeded**, but the agent never loaded the skill or ran a script: it labelled `kind/feature` and posted an off-policy comment without the footer ("marked as a feature request…") | A green run is not a correct run. Prompt changed to invoke `/prometheus-issue-triage` explicitly and to require the three checks first |
| 39948924248 | explicit skill invocation | Agent tried `python3 …/triage.py precheck`; Copilot CLI **denied** it (`denied-no-approval-rule`) because the shell allow rule matches on the command name; agent fell back to `noop` ("could not run required scripts") | Fail-safe. Script made executable and allow-listed by path only (no general `python3`) |
| 39949542341 | direct script allowlist | Correct: `skill` tool call → precheck → duplicates → label validation → `component/promtool` + `kind/feature`, no comment, `noop` audit note | Configuration used for golden attempt 0 |
| 39950320056 … 39952273151 | Golden attempt 0 (`results/run0-aborted/`) | A01 correct `noop`; **A02** agent typed `python3 …/triage.py`, denied, looped 12 tool calls, then `noop` — detection then hit HTTP 429; **A03** HTTP 429 before any output; **G01** gate worked but showed the run as *failed* | Stopped after 4 cases. Fixes: skill checks moved into deterministic pre-steps (cannot be skipped or mistyped), gate returns an output instead of failing, eval runner paces cases and resumes after 429 |
| 39952339286 | Kill-switch test on G02's run | Cancelled via the API while the agent job was in `Set up job`; run ended `cancelled` 2 min 40 s later; `safe_outputs` cancelled; issue #21 received no comment or label | Running executions can be stopped before anything is published |
| 39952913259 | Smoke 13 with pre-steps | Pre-steps worked (precheck + duplicates logged), agent got **HTTP 429**: `x-ratelimit-exceeded: global-chat:tbb-utility-models-aiu…`, `retry-after` until 16:00 UTC | Copilot Free caps "utility model" usage per ~4-hour window, so the golden set is replayed in windows (`run_eval.py` stops on 429 and resumes) |
