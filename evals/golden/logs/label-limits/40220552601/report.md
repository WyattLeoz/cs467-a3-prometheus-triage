✓ Downloaded artifacts for run 40220552601
✅ Safe-output limits test | success | 3.0m | https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40220552601
  run=40220552601 branch=main event=workflow_dispatch engine=copilot/gpt-4.1/v1.0.101
  fingerprint: directed/narrow/selective_write/lean/standalone
  metrics: errors=0 warnings=0 turns=1 tokens=13.5k aic=2.71 working-set-rebuild=1.00× action_min=3
  friction: occurrences=0 aic=0 ratio=0.0% range=0–0 AIC state=measured
  ledger: transactions_added=0
  session: wall=3.0m turns=1 tok/min=4486
  tokens: in=13.4k out=33 cache_read=0 reqs=1 steering=0
  agent_usage:
    agent | instances | outcome (completed/failed/incomplete) | requests | tokens (in/out) | credits | effort
    main main | 1 | 0/0/0 | 1 | 13.4k/33 | 0.000 | 
  github_api: calls=2 quota=1/5.00k
  jobs: 4/4 passed [activation:18.0s agent:2.1m safe_outputs:12.0s conclusion:14.0s]
  prompt: 9.63k chars file=aw-prompts/prompt.txt
  findings:
    [LOW] Potential Deterministic Alternative: This Triage run looks stable enough that deterministic automation may be a simpler fit.
  assessments:
    [LOW] This Triage run looks stable enough that deterministic automation may be a simpler fit. | turns=1 tool_types=2 actuation=selective_write
  recommendations:
    [MEDIUM] Consider whether a scripted rule or deterministic workflow step could replace this agentic path. — This Triage run looks stable enough that deterministic automation may be a simpler fit.
  insights:
    [LOW] 1 anomalous event pattern(s) detected | stage=tool_call score=0.65: new log template discovered; rare cluster (few observations)
  mcp_health:
    safeoutputs: ✅ healthy
  safe_outputs: 1 items — 1 label operation(s)
  created:
    add_labels
  tools:
    safeoutputs-add_labels ×1
    safeoutputs.add_labels ×1
  mcp_tools:
    safeoutputs/add_labels ×1
  firewall: 4 requests
  graders: pass=9 fail=1 error=0 unavailable=0
    pass artifact-production=1count direction=higher_is_better
    pass context-growth=1factor direction=lower_is_better
    pass execution-duration=8657ms direction=lower_is_better
    pass execution-step-count=1count direction=lower_is_better
    pass loops=0count threshold=3 direction=lower_is_better
    pass retries=0count threshold=10 direction=lower_is_better
    pass tool-failure-count=1count threshold=5 direction=lower_is_better
    fail tool-success-rate=0.5ratio threshold=0.8 direction=higher_is_better
    pass trajectory-efficiency=1ratio direction=higher_is_better
    pass working-set-rebuild-factor=1factor direction=lower_is_better
  logs: /tmp/audit/run-40220552601

i MCP Gateway Metrics

Total Requests: 1
Total Tool Calls: 1
Total Errors: 0
Servers: 1
Time Range: 43s

Server Usage
╭───────────┬────────┬──────────┬────────┬──────╮
│Server     │Requests│Tool Calls│Avg Time│Errors│
├───────────┼────────┼──────────┼────────┼──────┤
│safeoutputs│1       │1         │0ms     │0     │
╰───────────┴────────┴──────────┴────────┴──────╯

i Unified MCP + Firewall + Agent Event Timeline

Total Events  : 6
  Gateway     : 2  (tool_calls=2, difc_filtered=0, guard_blocked=0)
  Agent       : 4  (turns=1, tool_start=1, tool_done=1, messages=1, reasoning=0)

Event Timeline
╭────────────┬───┬───────────────────┬──────────────────────────────────┬─────────╮
│Time        │Src│Kind               │Detail                            │Status   │
├────────────┼───┼───────────────────┼──────────────────────────────────┼─────────┤
│18:19:10.635│GW │⚙ tool_call        │safeoutputs/tools/list            │initiated│
│18:19:43.493│AG │○ agent_turn       │turn 1                            │         │
│18:19:52.192│AG │● assistant_message│                                  │         │
│18:19:52.193│AG │▶ tool_start       │safeoutputs/safeoutputs-add_labels│         │
│18:19:53.941│GW │⚙ tool_call        │safeoutputs/add_labels            │initiated│
│18:19:53.948│AG │■ tool_done        │                                  │success  │
╰────────────┴───┴───────────────────┴──────────────────────────────────┴─────────╯
✓ Parsed log for run 40220552601 → /tmp/audit/run-40220552601/log.md
✓ Audit complete. Logs saved to /tmp/audit/run-40220552601
i Tip: use --artifacts to select specific artifact sets (agent, firewall, mcp, activation, detection, etc.)
