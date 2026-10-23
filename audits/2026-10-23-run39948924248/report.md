✓ Downloaded artifacts for run 39948924248
✅ Prometheus Issue Triage | success | 4.1m | https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/39948924248
  run=39948924248 branch=main event=issues engine=copilot/gpt-4.1/v1.0.101
  fingerprint: directed/moderate/read_only/lean/standalone
  metrics: errors=0 warnings=0 turns=1 tokens=65.3k aic=5.17 working-set-rebuild=1.04× action_min=5
  friction: occurrences=2 aic=2.58 ratio=50.0% range=0.9464–4.22 AIC tokens=32648 tool-calls=2 state=statistical ±32%
  ledger: transactions_added=0
  session: wall=4.1m turns=1 tok/min=15926
  tokens: in=11.7k out=188 cache_read=53.4k reqs=4 steering=0
  agent_usage:
    agent | instances | outcome (completed/failed/incomplete) | requests | tokens (in/out) | credits | effort
    main main | 1 | 0/0/0 | 4 | 65.1k/188 | 0.000 | 
  detection_model_usage: model=gpt-4.1-2025-04-14 requests=5
  github_api: calls=12 quota=35/5.00k
  jobs: 6/6 passed [pre_activation:12.0s activation:26.0s agent:1.4m detection:1.2m safe_outputs:16.0s conclusion:16.0s]
  prompt: 10.7k chars file=aw-prompts/prompt.txt
  findings:
    [MEDIUM] High Token Usage: Used 65.3k tokens
      Playbook: https://github.com/github/gh-aw/blob/main/.github/aw/debug-playbook.md#audit-findings
  insights:
    [MEDIUM] 2 anomalous event pattern(s) detected | stage=tool_call score=0.65: new log template discovered; rare cluster (few observations); stage=tool_result score=0.65: new log template discovered; rare cluster (few observations)
  mcp_health:
    safeoutputs: ✅ healthy
  tools:
    bash ×2
    safeoutputs-noop ×1
    safeoutputs.noop ×1
  mcp_tools:
    safeoutputs/noop ×1
  friction_drivers:
    source=agent_session driver=session_tool_failure occurrences=2 counted=2 state=statistical aic=2.58 tokens=32648 tool-calls=2
  friction_events:
    source=agent_session driver=session_tool_failure: agent session tool executions x2 counted=2 state=statistical aic=2.58 tokens=32648 tool-calls=2
  firewall: 6 requests
  graders: pass=9 fail=1 error=0 unavailable=0
    pass artifact-production=0count direction=higher_is_better
    pass context-growth=1.0516factor direction=lower_is_better
    pass execution-duration=8422ms direction=lower_is_better
    pass execution-step-count=4count direction=lower_is_better
    pass loops=1count threshold=3 direction=lower_is_better
    pass retries=0count threshold=10 direction=lower_is_better
    pass tool-failure-count=3count threshold=5 direction=lower_is_better
    fail tool-success-rate=0.25ratio threshold=0.8 direction=higher_is_better
    pass trajectory-efficiency=0.75ratio direction=higher_is_better
    pass working-set-rebuild-factor=1.0402factor direction=lower_is_better
  logs: /tmp/audit/run-39948924248

i MCP Gateway Metrics

Total Requests: 1
Total Tool Calls: 1
Total Errors: 0
Servers: 1
Time Range: 34s

Server Usage
╭───────────┬────────┬──────────┬────────┬──────╮
│Server     │Requests│Tool Calls│Avg Time│Errors│
├───────────┼────────┼──────────┼────────┼──────┤
│safeoutputs│1       │1         │0ms     │0     │
╰───────────┴────────┴──────────┴────────┴──────╯

i Unified MCP + Firewall + Agent Event Timeline

Total Events  : 13
  Gateway     : 2  (tool_calls=2, difc_filtered=0, guard_blocked=0)
  Agent       : 11  (turns=1, tool_start=3, tool_done=3, messages=4, reasoning=0)

Event Timeline
╭────────────┬───┬───────────────────┬────────────────────────────────────────────────┬─────────╮
│Time        │Src│Kind               │Detail                                          │Status   │
├────────────┼───┼───────────────────┼────────────────────────────────────────────────┼─────────┤
│11:51:58.913│GW │⚙ tool_call        │safeoutputs/tools/list                          │initiated│
│11:52:24.732│AG │○ agent_turn       │turn 1                                          │         │
│11:52:26.741│AG │● assistant_message│                                                │         │
│11:52:26.742│AG │▶ tool_start       │bash                                            │         │
│11:52:26.781│AG │■ tool_done        │                                                │error    │
│11:52:28.692│AG │● assistant_message│                                                │         │
│11:52:28.694│AG │▶ tool_start       │bash                                            │         │
│11:52:28.716│AG │■ tool_done        │                                                │error    │
│11:52:32.477│AG │● assistant_message│                                                │         │
│11:52:32.480│AG │▶ tool_start       │safeoutputs/safeoutputs-noop                    │         │
│11:52:32.895│GW │⚙ tool_call        │safeoutputs/noop                                │initiated│
│11:52:32.904│AG │■ tool_done        │                                                │success  │
│11:52:33.880│AG │● assistant_message│Triage could not be completed because the req...│         │
╰────────────┴───┴───────────────────┴────────────────────────────────────────────────┴─────────╯
✓ Parsed log for run 39948924248 → /tmp/audit/run-39948924248/log.md
✓ Audit complete. Logs saved to /tmp/audit/run-39948924248
i Tip: use --artifacts to select specific artifact sets (agent, firewall, mcp, activation, detection, etc.)
