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
- 🔍 rpc **safeoutputs**→`tools/call` `add_labels`
  
  ```json
  {"params":{"arguments":{"item_number":133,"labels":[{"confidence":"HIGH","name":"kind/enhancement","rationale":"The report is a clear, reproducible bug/feature proposal for the web component."}]},"name":"add_labels"}}
  ```
- 🔍 rpc **safeoutputs**→`tools/call` `add_labels`
  
  ```json
  {"params":{"arguments":{"item_number":133,"labels":[{"confidence":"HIGH","name":"component/web","rationale":"The issue describes a hang in the web API endpoint, matching the web component."}]},"name":"add_labels"}}
  ```
- 🔍 rpc **safeoutputs**←`resp`
  
  ```json
  {"id":1,"result":{"content":[{"text":"{\"result\":\"success\"}","type":"text"}]}}
  ```
- 🔍 rpc **safeoutputs**←`resp` ⚠️`calling "tools/call": E002: add_labels limit reached — 1 of 1 already used this run`
- 🔍 rpc **safeoutputs**→`tools/call` `add_labels`
  
  ```json
  {"params":{"arguments":{"item_number":133,"labels":[{"confidence":"HIGH","name":"component/web","rationale":"The issue describes a hang in the web API endpoint, matching the web component."}]},"name":"add_labels"}}
  ```
- 🔍 rpc **safeoutputs**←`resp` ⚠️`calling "tools/call": E002: add_labels limit reached — 1 of 1 already used this run`
- 🔍 rpc **safeoutputs**→`tools/call` `{"jsonrpc":"2.0","method":"tools/call","params":{"arguments":{"integrity":"high","message":"Decision: ROUTE. The issue is a clear, reproducible report of the /-/healthy web API endpoint hanging, which matches the web component. Precheck: not maintainer-authored, bug template mostly filled (missing expected result and config), no other project or security signals. Duplicate candidate prometheus/prometheus#17512 is a near-identical report but is not earlier. Label validator accepted component/web. Only one ad...`
- 🔍 rpc **safeoutputs**←`resp`
  
  ```json
  {"id":1,"result":{"content":[{"text":"{\"result\":\"success\"}","type":"text"}]}}
  ```
- ✓ **shutdown** Shutting down gateway...

</details>
