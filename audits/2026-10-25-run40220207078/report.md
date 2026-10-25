✓ Downloaded artifacts for run 40220207078
✅ Safe-output limits test | success | 2.9m | https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40220207078
  run=40220207078 branch=main event=workflow_dispatch engine=copilot/gpt-4.1/v1.0.101
  fingerprint: adaptive/moderate/selective_write/moderate/standalone
  metrics: errors=0 warnings=0 turns=1 tokens=40.2k aic=4.11 working-set-rebuild=1.01× action_min=3
  friction: occurrences=0 aic=0 ratio=0.0% range=0–0 AIC state=measured
  ledger: transactions_added=0
  session: wall=2.9m turns=1 tok/min=13949
  tokens: in=13.5k out=92 cache_read=26.6k reqs=3 steering=0
  agent_usage:
    agent | instances | outcome (completed/failed/incomplete) | requests | tokens (in/out) | credits | effort
    main main | 1 | 0/0/0 | 3 | 40.1k/92 | 0.000 | 
  github_api: calls=2 quota=1/5.00k
  jobs: 4/4 passed [activation:24.0s agent:1.7m safe_outputs:15.0s conclusion:19.0s]
  prompt: 9.62k chars file=aw-prompts/prompt.txt
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
    safeoutputs-add_labels ×1
    safeoutputs-noop ×1
    safeoutputs.add_labels ×1
    safeoutputs.noop ×1
  mcp_tools:
    safeoutputs/add_labels ×1
    safeoutputs/noop ×1
  firewall: 5 requests
  graders: pass=9 fail=1 error=0 unavailable=0
    pass artifact-production=1count direction=higher_is_better
    pass context-growth=1.0173factor direction=lower_is_better
    pass execution-duration=14838ms direction=lower_is_better
    pass execution-step-count=3count direction=lower_is_better
    pass loops=0count threshold=3 direction=lower_is_better
    pass retries=0count threshold=10 direction=lower_is_better
    pass tool-failure-count=2count threshold=5 direction=lower_is_better
    fail tool-success-rate=0.5ratio threshold=0.8 direction=higher_is_better
    pass trajectory-efficiency=1ratio direction=higher_is_better
    pass working-set-rebuild-factor=1.0127factor direction=lower_is_better
  logs: /tmp/audit/run-40220207078

i MCP Gateway Metrics

Total Requests: 2
Total Tool Calls: 2
Total Errors: 0
Servers: 1
Time Range: 39s

Server Usage
╭───────────┬────────┬──────────┬────────┬──────╮
│Server     │Requests│Tool Calls│Avg Time│Errors│
├───────────┼────────┼──────────┼────────┼──────┤
│safeoutputs│2       │2         │0ms     │0     │
╰───────────┴────────┴──────────┴────────┴──────╯

i Unified MCP + Firewall + Agent Event Timeline

Total Events  : 11
  Gateway     : 3  (tool_calls=3, difc_filtered=0, guard_blocked=0)
  Agent       : 8  (turns=1, tool_start=2, tool_done=2, messages=3, reasoning=0)

Event Timeline
╭────────────┬───┬───────────────────┬────────────────────────────────────────────────┬─────────╮
│Time        │Src│Kind               │Detail                                          │Status   │
├────────────┼───┼───────────────────┼────────────────────────────────────────────────┼─────────┤
│18:14:38.775│GW │⚙ tool_call        │safeoutputs/tools/list                          │initiated│
│18:15:06.473│AG │○ agent_turn       │turn 1                                          │         │
│18:15:12.823│AG │● assistant_message│                                                │         │
│18:15:12.824│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels              │         │
│18:15:13.219│GW │⚙ tool_call        │safeoutputs/add_labels                          │initiated│
│18:15:13.226│AG │■ tool_done        │                                                │success  │
│18:15:18.234│AG │● assistant_message│                                                │         │
│18:15:18.236│AG │▶ tool_start       │safeoutputs/safeoutputs-noop                    │         │
│18:15:18.243│GW │⚙ tool_call        │safeoutputs/noop                                │initiated│
│18:15:18.249│AG │■ tool_done        │                                                │success  │
│18:15:21.870│AG │● assistant_message│The label limit test was executed as requeste...│         │
╰────────────┴───┴───────────────────┴────────────────────────────────────────────────┴─────────╯
✓ Parsed log for run 40220207078 → /tmp/audit/run-40220207078/log.md
✓ Audit complete. Logs saved to /tmp/audit/run-40220207078
i Tip: use --artifacts to select specific artifact sets (agent, firewall, mcp, activation, detection, etc.)
