✓ Downloaded artifacts for run 40219450580
❌ Safe-output limits test | failure | 3.7m | https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40219450580
  run=40219450580 branch=main event=workflow_dispatch engine=copilot/gpt-4.1/v1.0.101
  fingerprint: adaptive/moderate/read_only/moderate/standalone
  metrics: errors=1 warnings=0 turns=1 tokens=27.2k aic=3.56 working-set-rebuild=1.03× action_min=4
  friction: occurrences=4 aic=7.12 ratio=200.0% range=0–15.08 AIC tokens=54396 tool-calls=4 state=statistical ±57%
  ledger: transactions_added=0
  session: wall=3.7m turns=1 tok/min=7418
  tokens: in=13.7k out=199 cache_read=13.3k reqs=2 steering=0
  agent_usage:
    agent | instances | outcome (completed/failed/incomplete) | requests | tokens (in/out) | credits | effort
    main main | 1 | 0/0/0 | 2 | 27.0k/199 | 0.000 | 
  github_api: calls=2 quota=1/5.00k
  jobs:
    ✓ activation (51.0s) success
    ✓ agent (1.9m) success
    ✗ safe_outputs (14.0s) failure
    ✓ conclusion (24.0s) success
  prompt: 9.56k chars file=aw-prompts/prompt.txt
  findings:
    [CRITICAL] Workflow Failed: Workflow 'Safe-output limits test' failed with 2 error(s): ##[error]✗ Message 1 (add_labels) failed: E003: Cannot add more than 2 labels (received 3)
##[error]1 safe output(s) failed:
      Playbook: https://github.com/github/gh-aw/blob/main/.github/aw/debug-playbook.md#audit-findings
  recommendations:
    [HIGH] Review error logs to identify root cause of failure — Understanding failure causes helps prevent recurrence
  insights:
    [MEDIUM] 2 anomalous event pattern(s) detected | stage=tool_call score=0.65: new log template discovered; rare cluster (few observations); stage=tool_result score=0.65: new log template discovered; rare cluster (few observations)
  errors:
    ##[error]✗ Message 1 (add_labels) failed: E003: Cannot add more than 2 labels (received 3)
##[error]1 safe output(s) failed:
    ##[error]✗ Message 1 (add_labels) failed: E003: Cannot add more than 2 labels (received 3)
##[error]1 safe output(s) failed:
  mcp_health:
    safeoutputs: ✅ healthy
  tools:
    safeoutputs-add_labels ×5
    safeoutputs.add_labels ×5
    safeoutputs-noop ×1
    safeoutputs.noop ×1
  mcp_tools:
    safeoutputs/add_labels ×5
    safeoutputs/noop ×1
  friction_drivers:
    source=agent_session driver=session_tool_failure occurrences=4 counted=4 state=statistical aic=7.12 tokens=54396 tool-calls=4
  friction_events:
    source=agent_session driver=session_tool_failure: agent session tool executions x4 counted=4 state=statistical aic=7.12 tokens=54396 tool-calls=4
  firewall: 4 requests
  graders: pass=8 fail=2 error=0 unavailable=0
    pass artifact-production=0count direction=higher_is_better
    pass context-growth=1.0297factor direction=lower_is_better
    pass execution-duration=23640ms direction=lower_is_better
    pass execution-step-count=2count direction=lower_is_better
    pass loops=3count threshold=3 direction=lower_is_better
    pass retries=0count threshold=10 direction=lower_is_better
    fail tool-failure-count=10count threshold=5 direction=lower_is_better
    fail tool-success-rate=0.1667ratio threshold=0.8 direction=higher_is_better
    pass trajectory-efficiency=0.3333ratio direction=higher_is_better
    pass working-set-rebuild-factor=1.0275factor direction=lower_is_better
  logs: /tmp/audit/run-40219450580

i MCP Gateway Metrics

Total Requests: 6
Total Tool Calls: 6
Total Errors: 0
Servers: 1
Time Range: 45s

Server Usage
╭───────────┬────────┬──────────┬────────┬──────╮
│Server     │Requests│Tool Calls│Avg Time│Errors│
├───────────┼────────┼──────────┼────────┼──────┤
│safeoutputs│6       │6         │0ms     │0     │
╰───────────┴────────┴──────────┴────────┴──────╯

i Unified MCP + Firewall + Agent Event Timeline

Total Events  : 22
  Gateway     : 7  (tool_calls=7, difc_filtered=0, guard_blocked=0)
  Agent       : 15  (turns=1, tool_start=6, tool_done=6, messages=2, reasoning=0)

Event Timeline
╭────────────┬───┬───────────────────┬────────────────────────────────────────────────┬─────────╮
│Time        │Src│Kind               │Detail                                          │Status   │
├────────────┼───┼───────────────────┼────────────────────────────────────────────────┼─────────┤
│18:05:39.317│GW │⚙ tool_call        │safeoutputs/tools/list                          │initiated│
│18:06:04.096│AG │○ agent_turn       │turn 1                                          │         │
│18:06:23.483│AG │● assistant_message│                                                │         │
│18:06:23.485│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:06:23.486│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:06:23.487│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:06:23.487│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:06:23.488│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:06:23.489│AG │▶ tool_start       │safeoutputs/safeoutputs-noop                    │         │
│18:06:24.704│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:06:24.704│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:06:24.704│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:06:24.705│GW │⚙ tool_call        │safeoutputs/noop                                │initiated│
│18:06:24.706│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:06:24.707│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:06:24.714│AG │■ tool_done        │                                                │success  │
│18:06:24.718│AG │■ tool_done        │                                                │error    │
│18:06:24.740│AG │■ tool_done        │                                                │error    │
│18:06:24.746│AG │■ tool_done        │                                                │success  │
│18:06:24.753│AG │■ tool_done        │                                                │error    │
│18:06:24.760│AG │■ tool_done        │                                                │error    │
│18:06:29.072│AG │● assistant_message│The label limit was enforced: only the first ...│         │
╰────────────┴───┴───────────────────┴────────────────────────────────────────────────┴─────────╯
✓ Parsed log for run 40219450580 → /tmp/audit/run-40219450580/log.md
✓ Audit complete. Logs saved to /tmp/audit/run-40219450580
i Tip: use --artifacts to select specific artifact sets (agent, firewall, mcp, activation, detection, etc.)
