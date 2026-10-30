✓ Downloaded artifacts for run 40219855681
✅ Safe-output limits test | success | 3.3m | https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40219855681
  run=40219855681 branch=main event=workflow_dispatch engine=copilot/gpt-4.1/v1.0.101
  fingerprint: adaptive/moderate/selective_write/moderate/standalone
  metrics: errors=0 warnings=0 turns=1 tokens=27.2k aic=3.56 working-set-rebuild=1.03× action_min=4
  friction: occurrences=4 aic=7.13 ratio=200.0% range=0–15.06 AIC tokens=54380 tool-calls=4 state=statistical ±57%
  ledger: transactions_added=0
  session: wall=3.3m turns=1 tok/min=8323
  tokens: in=13.7k out=205 cache_read=13.3k reqs=2 steering=0
  agent_usage:
    agent | instances | outcome (completed/failed/incomplete) | requests | tokens (in/out) | credits | effort
    main main | 1 | 0/0/0 | 2 | 27.0k/205 | 0.000 | 
  github_api: calls=2 quota=1/5.00k
  jobs: 4/4 passed [activation:16.0s agent:2.3m safe_outputs:14.0s conclusion:15.0s]
  prompt: 9.53k chars file=aw-prompts/prompt.txt
  findings:
    [LOW] Cheaper Model Available: This Triage run may not need a frontier model. A smaller model (e.g. gpt-4.1-mini, claude-haiku-4-5) could handle the task at lower cost.
  assessments:
    [LOW] This Triage run may not need a frontier model. A smaller model (e.g. gpt-4.1-mini, claude-haiku-4-5) could handle the task at lower cost. | domain=triage resource_profile=moderate actuation=selective_write
  recommendations:
    [MEDIUM] Try engine.model: gpt-4.1-mini or claude-haiku-4-5 in the workflow frontmatter. — This Triage run may not need a frontier model. A smaller model (e.g. gpt-4.1-mini, claude-haiku-4-5) could handle the task at lower cost.
  insights:
    [MEDIUM] 2 anomalous event pattern(s) detected | stage=tool_call score=0.65: new log template discovered; rare cluster (few observations); stage=tool_result score=0.65: new log template discovered; rare cluster (few observations)
  mcp_health:
    safeoutputs: ✅ healthy
  safe_outputs: 1 items — 1 label operation(s)
  created:
    add_labels WyattLeoz/cs467-a3-prometheus-triage#70
  tools:
    safeoutputs-add_labels ×5
    safeoutputs.add_labels ×5
    safeoutputs-noop ×1
    safeoutputs.noop ×1
  mcp_tools:
    safeoutputs/add_labels ×5
    safeoutputs/noop ×1
  friction_drivers:
    source=agent_session driver=session_tool_failure occurrences=4 counted=4 state=statistical aic=7.13 tokens=54380 tool-calls=4
  friction_events:
    source=agent_session driver=session_tool_failure: agent session tool executions x4 counted=4 state=statistical aic=7.13 tokens=54380 tool-calls=4
  firewall: 4 requests
  graders: pass=8 fail=2 error=0 unavailable=0
    pass artifact-production=1count direction=higher_is_better
    pass context-growth=1.0296factor direction=lower_is_better
    pass execution-duration=22688ms direction=lower_is_better
    pass execution-step-count=2count direction=lower_is_better
    pass loops=3count threshold=3 direction=lower_is_better
    pass retries=0count threshold=10 direction=lower_is_better
    fail tool-failure-count=10count threshold=5 direction=lower_is_better
    fail tool-success-rate=0.1667ratio threshold=0.8 direction=higher_is_better
    pass trajectory-efficiency=0.3333ratio direction=higher_is_better
    pass working-set-rebuild-factor=1.0269factor direction=lower_is_better
  logs: /tmp/audit/run-40219855681

i MCP Gateway Metrics

Total Requests: 6
Total Tool Calls: 6
Total Errors: 0
Servers: 1
Time Range: 52s

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
│18:10:30.389│GW │⚙ tool_call        │safeoutputs/tools/list                          │initiated│
│18:11:00.357│AG │○ agent_turn       │turn 1                                          │         │
│18:11:20.156│AG │● assistant_message│                                                │         │
│18:11:20.158│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:11:20.159│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:11:20.160│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:11:20.161│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:11:20.162│AG │▶ tool_start       │safeoutputs/safeoutputs-noop                    │         │
│18:11:20.162│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:11:21.780│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:11:21.781│GW │⚙ tool_call        │safeoutputs/noop                                │initiated│
│18:11:21.883│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:11:21.884│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:11:21.884│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:11:21.885│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:11:21.894│AG │■ tool_done        │                                                │success  │
│18:11:21.901│AG │■ tool_done        │                                                │error    │
│18:11:21.941│AG │■ tool_done        │                                                │success  │
│18:11:21.950│AG │■ tool_done        │                                                │error    │
│18:11:21.956│AG │■ tool_done        │                                                │error    │
│18:11:21.964│AG │■ tool_done        │                                                │error    │
│18:11:24.983│AG │● assistant_message│The label limit test was executed as instruct...│         │
╰────────────┴───┴───────────────────┴────────────────────────────────────────────────┴─────────╯
✓ Parsed log for run 40219855681 → /tmp/audit/run-40219855681/log.md
✓ Audit complete. Logs saved to /tmp/audit/run-40219855681
i Tip: use --artifacts to select specific artifact sets (agent, firewall, mcp, activation, detection, etc.)
