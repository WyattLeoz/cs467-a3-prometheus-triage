# Permitted coding-assistant fallback

The brief permits a coding-assistant dry run when end-to-end execution is unavailable, provided
the same configuration/inputs, transcripts and untested controls are identified. The owner explicitly
approved this fallback. `run9-isolated/METHOD.md` records the live Copilot HTTP 429 and retained draft.

## Configuration, inputs and independence

- Runtime configuration: `5b535aa1a1fdb0b2a6dc0d87930e561cf20a5f52`. Workflow source/compiled lock,
  AGENTS, SKILL, scripts and references were copied into a fresh directory. `_manifest.json` records
  their byte hashes, input mapping and prepared-result hashes. Windows checkout line endings can
  differ from Git blob bytes; semantic source content matches the frozen commit.
- `prepare_dry_run.py` ran the real precheck/duplicate script for all 16 historical and 4 adversarial
  inputs. Only title, body, original time and association were supplied. Prepared candidates retain
  the original-time cutoff. Expected outcomes, prior results, raw corpus and Git history were absent.
- A new subagent with no inherited conversation performed the triage. Its access was restricted by
  task instructions to this directory; this is context separation, **not an OS-enforced filesystem jail**.
  It made no network/API calls. The evaluator did not provide expected answers or feedback between cases.
- Model: **Codex based on GPT-6**, as identified by the host. Exact deployment/snapshot is not exposed
  and is not pinned. This is a different model from the workflow's `gpt-4.1`; scores are not interchangeable.
- The skill was loaded by reading its actual file, not by pretending to invoke Copilot's `skill` tool.
  The assistant read workflow/facts/references and all prepared inputs, validated 11 label proposals
  with the same script, then wrote `responses.json` once. The maintainer case represents the pre-model gate.
- All 20 outputs were handed off before the evaluator applied the unchanged expectations. Runtime/input
  hashes were rechecked after handoff and match. No response was edited to make a test pass.

## Results and transcript

**20/20 semantic/proposal checks pass**, including the 16 real cases and 4 adversarial cases.
`scores.json` records each comparison; `responses.json` retains every actual decision, reason and proposal.
`../../logs/run9-dry-run/inputs/` holds the exact issue/check files read by the assistant.
`tool-read-transcript.txt` in that log directory captures actual file reads and label-validation output;
`task-instructions.txt` records the task procedure, and `assistant-handoff.txt` records the final reply.
The transcript does not claim to export private reasoning or the hosting system's internal tool protocol.

No semantic failures occurred in this single fallback. One local PowerShell array-count check failed
before any response file was written; the assistant corrected the count check and recorded it in the
transcript. That mechanical check did not supply expected answers or revise any recorded response.
A single run cannot estimate variance or demonstrate that Copilot's earlier judgement failures are fixed.

## Controls not tested by this dry run

No real GitHub trigger, token permissions, firewall, safe-output MCP call caps, publisher attribution,
threat-detection model, queue/rate/AIC/runtime limits, audit automation, kill switch or drift alert ran
inside the fallback. Do not count these as dry-run passes. Live run9, earlier preserved negative tests,
the cancellation/drift records and deterministic regressions provide the separate control evidence.
The shared `validate_proposal` function was executed offline against every actual fallback proposal;
this tests its contract, not the complete GitHub publishing pipeline.

## Reproduction

1. Check out this submission commit (which includes the fallback helpers). Verify its runtime files
   match frozen commit `5b535aa1a1fdb0b2a6dc0d87930e561cf20a5f52`; evidence-only changes are separate.
2. Run `python3 evals/golden/prepare_dry_run.py /NEW/EMPTY/CONTEXT /SEPARATE/MANIFEST.json`.
3. Give a fresh coding-assistant session only that context and the recorded task instructions. Preserve
   actual reads/validator output and its one-shot responses; do not give it cases.json/adversarial.json.
4. Copy the manifest as `_manifest.json` and responses as `responses.json` into a new result directory.
   Record the assistant/model used and
   run `python3 evals/golden/score_dry_run.py evals/golden/results/NEW_TAG` only after its handoff.
5. Review every failed check and compare raw proposals. Never replace this run or alter the expectations.
