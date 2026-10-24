<details>
<summary>MCP Gateway</summary>

- ✓ **startup** MCPG Gateway version: v0.4.37
- ✓ **startup** Starting MCPG with config: stdin, listen: 0.0.0.0:8080, log-dir: /tmp/gh-aw/mcp-logs/
- ✓ **startup** WASM compilation cache directory: /tmp/gh-aw/wazero-cache
- ✓ **startup** Environment validation passed
- ✓ **startup** Loaded 1 MCP server(s): [safeoutputs]
- ✓ **startup** Guards sink server ID logging enrichment disabled (no sink server IDs configured)
- ✓ **startup** OpenTelemetry tracing disabled (no OTLP endpoint configured)
- ✓ **backend**
  ```
  Successfully connected to MCP backend server, command=docker
  ```
- 🔍 rpc **safeoutputs**→`tools/list`
- 🔍 rpc **safeoutputs**←`resp` `{"jsonrpc":"2.0","id":1,"result":{"ttlMs":0,"cacheScope":"","tools":[{"description":"WRITE-ONCE: do NOT probe this tool with empty or placeholder arguments. If not ready to post a real comment, call noop. Adds a comment to an existing GitHub issue, pull request, or discussion; use create_issue, create_discussion, or create_pull_request for new items. Input is limited to 524288 characters, 10 mentions, and configured max-links URL occurrences (default: 50). Oversized agent content is automatically replaced b...`
- ✓ **startup** Starting MCPG in ROUTED mode on 0.0.0.0:8080
- ✓ **startup** Routes: /mcp/<server> where <server> is one of: [safeoutputs]
- ✓ **startup** TLS not configured — listening on http://0.0.0.0:8080 (set --tls-cert/--tls-key to enable)
- ✓ **backend**
  ```
  Successfully connected to MCP backend server, command=docker
  ```
- 🔍 rpc **safeoutputs**→`tools/call` `add_comment`
  
  ```json
  {"params":{"arguments":{"body":"This appears to be the same problem as prometheus/prometheus#17512 (similar /-/healthy endpoint hang and API symptoms). Please add any new details to that issue to help maintainers track the problem in one place."},"name":"add_comment"}}
  ```
- 🔍 rpc **safeoutputs**→`tools/call` `add_labels`
  
  ```json
  {"params":{"arguments":{"labels":[{"confidence":"HIGH","name":"component/web","rationale":"The issue describes a hang in the /-/healthy endpoint, which is part of the web API."}]},"name":"add_labels"}}
  ```
- 🔍 rpc **safeoutputs**←`resp`
  
  ```json
  {"id":1,"result":{"content":[{"text":"{\"result\":\"success\",\"temporary_id\":\"aw_Ozo20MR8\",\"comment\":\"#aw_Ozo20MR8\"}","type":"text"}]}}
  ```
- 🔍 rpc **safeoutputs**←`resp`
  
  ```json
  {"id":1,"result":{"content":[{"text":"{\"result\":\"success\"}","type":"text"}]}}
  ```
- ✓ **shutdown** Shutting down gateway...

</details>
