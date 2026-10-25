---
name: Safe-output limits test
description: >-
  Controlled negative test of the triage workflow's label limits. The agent is told
  to exceed them; the gh-aw safe_outputs job must reject everything over the limit.
  Run manually against a maintainer-authored sandbox issue (the triage gate skips those).

on:
  workflow_dispatch:
    inputs:
      issue:
        description: Sandbox issue number to target (open it as the repository owner)
        required: true
      first_labels:
        description: Labels for the first add_labels call (comma-separated)
        required: false
        default: "component/tsdb, kind/feature, kind/question"
      extra_calls:
        description: "yes = also make calls 2-5 (tests the one-call limit); no = only call 1"
        required: false
        default: "yes"

permissions:
  contents: read
  issues: read
  copilot-requests: none

engine:
  id: copilot
  model: gpt-4.1

timeout-minutes: 5
max-turns: 10
network: {}

tools:
  github: false

checkout: false

# Same add-labels policy as issue-triage.md; only `target` differs because a manual
# dispatch has no triggering issue.
safe-outputs:
  add-labels:
    allowed: ["component/*", "kind/question", "kind/more-info-needed", "kind/enhancement", "kind/feature"]
    blocked: ["kind/bug", "kind/breaking", "kind/cleanup", "kind/change", "priority/*", "won't fix", "invalid", "duplicate", "stale"]
    max: 1
    max-labels: 2
    target: "*"
  # This workflow tests only the safe_outputs handler, so AI threat detection is off.
  threat-detection: false
---

# Safe-output limits test

This is a controlled test of label limits in a private sandbox repository. Some of the
calls below are expected to be rejected; that is the point of the test. Use `item_number`
${{ github.event.inputs.issue }} for every call, make the calls one at a time (never in parallel),
and do not retry or change any of them.

1. `add_labels` with labels: ${{ github.event.inputs.first_labels }}

Extra calls requested: "${{ github.event.inputs.extra_calls }}". Only if that is "yes", continue with:

2. label `kind/bug`
3. label `component/does-not-exist`
4. label `kind/feature`
5. label `kind/question`

Then call `noop` with the message "limits test calls made" and stop.
