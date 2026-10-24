✓ Downloaded artifacts for run 40027444395
✅ Prometheus Issue Triage | success | 5.4m | https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40027444395
  run=40027444395 branch=main event=issues engine=copilot/gpt-4.1/v1.0.101
  fingerprint: adaptive/moderate/read_only/moderate/standalone
  metrics: errors=0 warnings=0 turns=1 tokens=89.2k aic=7.47 working-set-rebuild=1.16× action_min=6
  friction: occurrences=1 aic=1.49 ratio=20.0% range=0.6242–2.36 AIC tokens=17843 tool-calls=1 state=statistical ±30%
  ledger: transactions_added=0
  session: wall=5.4m turns=1 tok/min=16624
  tokens: in=18.8k out=253 cache_read=70.1k reqs=5 steering=0
  agent_usage:
    agent | instances | outcome (completed/failed/incomplete) | requests | tokens (in/out) | credits | effort
    main main | 1 | 0/0/0 | 5 | 89.0k/253 | 0.000 | 
  detection_model_usage: model=gpt-4.1-2025-04-14 requests=16
  github_api: calls=17 quota=42/5.00k
  jobs: 6/6 passed [pre_activation:14.0s activation:29.0s agent:1.9m detection:1.8m safe_outputs:15.0s conclusion:20.0s]
  prompt: 11.1k chars file=aw-prompts/prompt.txt
  findings:
    [MEDIUM] High Token Usage: Used 89.2k tokens
      Playbook: https://github.com/github/gh-aw/blob/main/.github/aw/debug-playbook.md#audit-findings
    [LOW] Cheaper Model Available: This Triage run may not need a frontier model. A smaller model (e.g. gpt-4.1-mini, claude-haiku-4-5) could handle the task at lower cost.
  assessments:
    [LOW] This Triage run may not need a frontier model. A smaller model (e.g. gpt-4.1-mini, claude-haiku-4-5) could handle the task at lower cost. | domain=triage resource_profile=moderate actuation=read_only
  recommendations:
    [MEDIUM] Try engine.model: gpt-4.1-mini or claude-haiku-4-5 in the workflow frontmatter. — This Triage run may not need a frontier model. A smaller model (e.g. gpt-4.1-mini, claude-haiku-4-5) could handle the task at lower cost.
  insights:
    [MEDIUM] 2 anomalous event pattern(s) detected | stage=tool_call score=0.65: new log template discovered; rare cluster (few observations); stage=tool_result score=0.65: new log template discovered; rare cluster (few observations)
  skill_activations:
    prometheus-issue-triage: invoked (source: log_parse)
  mcp_health:
    safeoutputs: ✅ healthy
  tools:
    bash ×2
    safeoutputs-noop ×1
    safeoutputs.noop ×1
    skill ×1
    skill:prometheus-issue-triage ×1
  mcp_tools:
    safeoutputs/noop ×1
  friction_drivers:
    source=agent_session driver=session_tool_failure occurrences=1 counted=1 state=statistical aic=1.49 tokens=17843 tool-calls=1
  friction_events:
    source=agent_session driver=session_tool_failure: agent session tool executions x1 counted=1 state=statistical aic=1.49 tokens=17843 tool-calls=1
  firewall: 7 requests
  graders: pass=10 fail=0 error=0 unavailable=0
    pass artifact-production=0count direction=higher_is_better
    pass context-growth=1.1723factor direction=lower_is_better
    pass execution-duration=31451ms direction=lower_is_better
    pass execution-step-count=5count direction=lower_is_better
    pass loops=0count threshold=3 direction=lower_is_better
    pass retries=0count threshold=10 direction=lower_is_better
    pass tool-failure-count=1count threshold=5 direction=lower_is_better
    pass tool-success-rate=0.8ratio threshold=0.8 direction=higher_is_better
    pass trajectory-efficiency=0.8ratio direction=higher_is_better
    pass working-set-rebuild-factor=1.1581factor direction=lower_is_better
  logs: /tmp/audit/run-40027444395

i MCP Gateway Metrics

Total Requests: 1
Total Tool Calls: 1
Total Errors: 0
Servers: 1
Time Range: 44s

Server Usage
╭───────────┬────────┬──────────┬────────┬──────╮
│Server     │Requests│Tool Calls│Avg Time│Errors│
├───────────┼────────┼──────────┼────────┼──────┤
│safeoutputs│1       │1         │0ms     │0     │
╰───────────┴────────┴──────────┴────────┴──────╯

i Unified MCP + Firewall + Agent Event Timeline

Total Events  : 16
  Gateway     : 2  (tool_calls=2, difc_filtered=0, guard_blocked=0)
  Agent       : 14  (turns=1, tool_start=4, tool_done=4, messages=5, reasoning=0)

Event Timeline
╭────────────┬───┬───────────────────┬────────────────────────────────────────────────┬─────────╮
│Time        │Src│Kind               │Detail                                          │Status   │
├────────────┼───┼───────────────────┼────────────────────────────────────────────────┼─────────┤
│21:33:29.246│GW │⚙ tool_call        │safeoutputs/tools/list                          │initiated│
│21:33:54.183│AG │○ agent_turn       │turn 1                                          │         │
│21:33:58.987│AG │● assistant_message│                                                │         │
│21:33:58.990│AG │▶ tool_start       │skill                                           │         │
│21:33:58.998│AG │■ tool_done        │                                                │success  │
│21:34:03.243│AG │● assistant_message│                                                │         │
│21:34:03.244│AG │▶ tool_start       │bash                                            │         │
│21:34:03.278│AG │■ tool_done        │                                                │success  │
│21:34:07.364│AG │● assistant_message│                                                │         │
│21:34:07.365│AG │▶ tool_start       │bash                                            │         │
│21:34:07.427│AG │■ tool_done        │                                                │success  │
│21:34:12.547│AG │● assistant_message│                                                │         │
│21:34:12.549│AG │▶ tool_start       │safeoutputs/safeoutputs-noop                    │         │
│21:34:12.898│GW │⚙ tool_call        │safeoutputs/noop                                │initiated│
│21:34:12.906│AG │■ tool_done        │                                                │success  │
│21:34:26.358│AG │● assistant_message│Decision: NO_ACTION. The issue is promotional...│         │
╰────────────┴───┴───────────────────┴────────────────────────────────────────────────┴─────────╯
✓ Parsed log for run 40027444395 → /tmp/audit/run-40027444395/log.md
✓ Audit complete. Logs saved to /tmp/audit/run-40027444395
i Tip: use --artifacts to select specific artifact sets (agent, firewall, mcp, activation, detection, etc.)
