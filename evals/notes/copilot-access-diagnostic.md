# Copilot access diagnostic (2026-10-23)

Why the workflow pins `gpt-4.1`. Produced by the temporary workflow `.github/workflows/copilot-access-diagnostic.yml` (removed after use; see git history), runs 39947946181 and 39948762273. The token itself was never printed.

Every other model failed inside the agent with `400 The requested model is not supported` (runs 39943214109, 39944046261, 39944759869, 39945330955, 39946181522, 39946827890), while authentication, token type (fine-grained PAT) and Copilot CLI (1.0.95, gh-aw compat window 1.0.35–1.0.101) were fine.

```text
gpt-5.6-luna-free-auto /responses -> HTTP 400 {"message":"The requested model is not supported.","code":"model_not_supported","param":"model","type":"invalid_request_error"}
claude-haiku-4.5 /v1/messages -> HTTP 400 {"message":"The requested model is not supported.","code":"model_not_supported","param":"model","type":"invalid_request_error"}
gpt-4.1 /chat/completions -> HTTP 200 
claude-haiku-5.5                  disabled  false  /v1/messages+/chat/completions  null  null
claude-opus-4.8                   disabled  false  /v1/messages+/chat/completions  null  null
claude-opus-4.8-fast              disabled  false  /v1/messages+/chat/completions  null  null
claude-opus-5                     disabled  false  /v1/messages+/chat/completions  null  null
claude-opus-5.5                   disabled  false  /v1/messages+/chat/completions  null  null
claude-sonnet-5                   disabled  false  /v1/messages+/chat/completions  null  null
claude-sonnet-5.5                 disabled  false  /v1/messages+/chat/completions  null  null
copilot-search-a                  -         false  /chat/completions               null  null
copilot-search-b                  -         false  /chat/completions               null  null
gpt-3.5-turbo                     -         false  null                            null  
gpt-3.5-turbo-0613                -         false  null                            null  
gpt-4                             -         false  null                            null  
gpt-4-0613                        -         false  null                            null  
gpt-4-o-preview                   -         false  null                            null  
gpt-4.1                           enabled   false  null                            null  
gpt-4.1-2025-04-14                enabled   false  null                            null  
gpt-4o                            -         false  null                            null  
gpt-4o-2024-05-13                 -         false  null                            null  
gpt-4o-2024-08-06                 -         false  null                            null  
gpt-4o-2024-11-20                 -         false  null                            null  
gpt-4o-mini                       -         false  null                            null  
gpt-4o-mini-2024-07-18            -         false  null                            null  
gpt-5.6-luna                      enabled   false  /responses+ws:/responses        null  null
gpt-5.6-luna-free-auto            -         false  /responses+ws:/responses        null  null
gpt-5.6-luna-utility              -         false  /responses+ws:/responses        null  null
gpt-5.6-sol                       disabled  false  /responses+ws:/responses        null  null
gpt-5.6-terra                     disabled  false  /responses+ws:/responses        null  null
gpt-6-astra                       disabled  false  /responses+ws:/responses        null  null
gpt-6-luna                        enabled   false  /responses+ws:/responses        null  null
gpt-6-sol                         disabled  false  /responses+ws:/responses        null  null
gpt-6.1-sol                       disabled  false  /responses+ws:/responses        null  null
kimi-k3                           disabled  false  /chat/completions               null  null
mai-code-1.1-flash                enabled   false  /responses+ws:/responses        null  null
text-embedding-3-small            -         false  null                            null  
text-embedding-3-small-inference  -         false  null                            null  
text-embedding-ada-002            -         false  null                            null  
== minimal probe per enabled model on its native endpoint
gpt-6-luna /responses -> HTTP 400 {"message":"The requested model is not supported.","code":"model_not_supported","param":"model","type":"invalid_request_error"}
gpt-5.6-luna /responses -> HTTP 400 {"message":"The requested model is not supported.","code":"model_not_supported","param":"model","type":"invalid_request_error"}
mai-code-1.1-flash /responses -> HTTP 400 {"message":"The requested model is not supported.","code":"model_not_supported","param":"model","type":"invalid_request_error"}
== token owner
{
  "login": "WyattLeoz",
  "type": "User"
}
== Copilot seat (copilot_internal/user)
{
  "copilot_plan": "individual",
  "access_type_sku": "free_limited_copilot",
  "chat_enabled": true,
  "is_mcp_enabled": true,
  "organization_login_list": [],
  "organization_list": [],
  "restricted_telemetry": true,
  "can_signup_for_limited": false,
  "quota_snapshots": {
    "chat": {
      "entitlement": 200,
      "remaining": 200,
      "unlimited": false,
      "overage_permitted": false
    },
    "completions": {
      "entitlement": 2000,
      "remaining": 1996,
      "unlimited": false,
      "overage_permitted": false
    },
    "premium_interactions": {
      "entitlement": 0,
      "remaining": 0,
      "unlimited": false,
      "overage_permitted": false
    }
  }
}
== models visible to integration agentic-workflows
claude-fable-5                    disabled  false  /v1/messages+/chat/completions  null  null
claude-fable-5.1                  disabled  false  /v1/messages+/chat/completions  null  null
claude-haiku-4.5                  enabled   false  /chat/completions+/v1/messages  null  null
```
