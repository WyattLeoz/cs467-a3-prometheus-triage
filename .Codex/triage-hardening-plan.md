# Triage submission hardening plan

Status: approved by the owner on 2026-10-28; Claude is paused. The evaluator will also bind each result tag to one configuration commit so resumed runs cannot mix versions.
Base inspected: `087bc648b72a2501a2acebc456b39fda2ae5000d`.

## Problem and scope

The agent sometimes publishes outputs inconsistent with its declared decision: A02 declared
ROUTE and posted a comment. The scorer catches this only after publication. The full evaluation
on the latest configuration is unfinished, and the documentation describes the previous skill.
The owner authorizes repository edits and GitHub updates, but will handle public visibility and
marker access personally. An A+ is a target, not an outcome to claim without supporting evidence.

## Smallest implementation

1. Preserve the existing run6 results and audit evidence. Use a separate result tag for any changed
   configuration; do not mix configuration commits or overwrite earlier attempts.
2. Add a deterministic check before the built-in safe-output publishers. Validate the actual
   proposed comments and labels against the final declared decision. Missing or ambiguous decision
   evidence fails closed. Keep GitHub's existing sanitization, allowed labels, target limits,
   detection, read-only agent permissions, network restrictions and budgets.
3. Clarify the skill's generic decision procedure and final output check. Skip label validation
   when emitting no labels. Do not include golden-case examples or change expected outcomes.
4. Add regression tests for invalid decision/output combinations, missing evidence, allowed
   combinations, and archive failure handling. Verify the compiled guard runs before publication.
5. Freeze the agent configuration, replay all 20 cases, save every result and its logs, and score
   honestly. Preserve and distinguish quota failures from model or policy failures. Respect the
   provider's retry interval; do not bypass limits or purchase a plan.
6. Update DESIGN.md (at most 150 normal Markdown lines), README.md, evaluation instructions,
   FAILURES.md, test counts and AI-use disclosure to match the tested configuration and results.
7. Review the diff, publish the verified changes through a pull request, and provide the exact
   submission commit plus a fresh rubric-based assessment. Finish any authorized integration only
   after checks pass; do not change repository visibility or invite collaborators.

## Data flow and ownership

Issue -> existing deterministic context -> skill/model -> proposed safe outputs and session
evidence -> deterministic consistency check -> existing safe-output publishers -> audit archive
-> evaluation scorer. The owner maintains the policy; the new check cannot infer whether the
model chose the right project, component or duplicate. The golden evaluation measures that.

## Validation and failure modes

- Build: recompile both workflows with gh-aw v0.93.1 and inspect changes to generated locks.
- Lint: strict compiler validation, Python syntax checks and whitespace/diff checks.
- Test: existing skill/scorer/input tests plus regression tests for the new check and archive logic.
- Run: exercise valid and rejected proposals locally, then verify actual sandbox runs and archives.
- Check both successful and rejected outputs; a green workflow is not evidence of correct triage.
- Use trusted repository code in the publishing job. Never execute text from agent output or an issue.
- Preserve logs for rejected outputs. An unavailable decision transcript must withhold publication.
- Final run may require several quota windows. Report the actual progress and remaining limitation
  instead of claiming a completed evaluation or inventing a grade improvement.

## Rollback

Revert the workflow/skill hardening commit and recompile its lock if necessary. Disable the workflow
and cancel pending executions first if a publishing regression is discovered. Keep all evaluation
and audit history; do not delete issues or rewrite Git history. No new paid dependency is planned.
