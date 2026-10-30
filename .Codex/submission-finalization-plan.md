# Final submission plan — 2026-10-30

Approved by the repository owner in the submission-preparation chat before implementation.

The problem is evidence/configuration consistency, not a requirement to make every model
decision correct. Keep the historical cases and expectations unchanged. Preserve all
recorded failures and distinguish a historical live result from final-config validation.

## Data flow and smallest complete change

- Run deterministic issue checks in a trusted workflow step. Give the model only the
  issue, prepared check results, skill and repository facts; exclude raw future corpus
  entries and evaluation-bearing git objects from its workspace.
- Keep model proposals separate from the write-token job. Reject mixed noop/action
  proposals and multiple kind labels. Clarify ROUTE's ambiguity fallback without
  widening the label allowlist or changing expected outcomes.
- Require successful reads of both prepared outputs in evaluation evidence, rather
  than matching filenames mentioned in prose. Add regressions for each defect.
- Bring the four negative-label-test records into this branch with immutable provenance.
- Correct documentation claims and keep DESIGN.md at most 150 normal Markdown lines.

## Dependencies, failures and validation

Use Python standard library and gh-aw v0.93.1. Compile both workflows strictly, require
no generated-lock diff, run all unit/regression checks and execute representative
deterministic checks. Freeze the candidate before a live golden replay. If the free
Copilot provider quota blocks completion, retain the attempts and run the assignment's
permitted coding-assistant fallback in a fresh isolated context. Preserve its transcript,
identify the different assistant/model, and state which live controls it cannot test.
Do not claim a dry run demonstrates Copilot accuracy, firewall or GitHub publication.

The owner approved the isolated fallback and final GitHub publication. Changes go through
a PR and local/CI review. A provisional default-branch deployment is sandbox-only.
Rollback: revert this candidate's configuration commit and recompile; historical evidence
is retained. No upstream deployment, new secret, or expanded GitHub permission is needed.

## Delivery

Verify the final exact commit, all evidence links, clean tests/CI, and eLearn requirements.
The eLearn page requires one commit-specific GitHub URL, no PDF. Fill the text field and
leave Submit untouched for the owner. Deadline shown: 2026-11-01 23:59 Singapore time.
