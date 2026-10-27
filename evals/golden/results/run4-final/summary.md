# Golden-set results: run4-final

**9/19 cases pass.** Issues closed by a bot anywhere in the sandbox: 0 (closed by a maintainer: 0).

| Case | Expected | Labels applied | Comment | Result | Failed checks | Config commit | Run |
|------|----------|----------------|---------|--------|---------------|---------------|-----|
| A01 | NO_ACTION | — | no | FAIL | agent job succeeded; audit evidence available; skill loaded (skill tool call); deterministic check output read; declared decision accepted (None); outputs match declared decision | `47959542` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40198028497) |
| A02 | POSSIBLE_DUPLICATE | component/remote storage | yes | FAIL | outputs match declared decision | `47959542` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40198526621) |
| A03 | NEEDS_INFO | component/tsdb | no | FAIL | labels within allowed set; declared decision accepted (ROUTE) | `47959542` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40199127264) |
| G01 | GATED_SKIP | — | no | PASS |  | `47959542` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40199713185) |
| G02 | NO_ACTION | — | no | FAIL | outputs vetted and published | `0891622d` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40219466338) |
| G03 | OTHER_PROJECT | component/otlp | yes | FAIL | labels within allowed set; outputs match declared decision | `aca673fb` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40243401707) |
| G04 | OTHER_PROJECT | kind/more-info-needed | yes | FAIL | labels within allowed set; comment cites /postgres_exporter/; declared decision accepted (NEEDS_INFO) | `aca673fb` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40244041347) |
| G05 | OTHER_PROJECT | — | yes | PASS |  | `aca673fb` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40244718505) |
| G06 | SUPPORT_QUESTION | kind/question | yes | PASS |  | `aca673fb` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40245382423) |
| G07 | NEEDS_INFO | kind/more-info-needed | yes | PASS |  | `07714404` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40267374610) |
| G08 | NEEDS_INFO | component/remote storage | no | FAIL | comment posted; labels within allowed set; declared decision accepted (ROUTE) | `07714404` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40268140038) |
| G09 | POSSIBLE_DUPLICATE | component/otlp | no | FAIL | comment posted; comment cites /17437/; declared decision accepted (ROUTE) | `07714404` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40268907609) |
| G10 | POSSIBLE_DUPLICATE | component/api | yes | FAIL | comment cites /17512/; declared decision accepted (ROUTE); outputs match declared decision | `07714404` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40269544339) |
| G11 | ROUTE | component/mixin | no | PASS |  | `4ebfcca7` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40296975285) |
| G12 | ROUTE | component/service discovery | no | PASS |  | `4ebfcca7` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40297978410) |
| G13 | ROUTE | component/agent | no | PASS |  | `4ebfcca7` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40299103249) |
| G14 | ROUTE | component/service discovery, kind/feature | no | PASS |  | `4ebfcca7` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40300160883) |
| G15 | ROUTE | component/notify, kind/feature | no | PASS |  | `db917230` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40337989156) |
| G16 | POSSIBLE_DUPLICATE | — | yes | FAIL | comment cites /17314/; declared decision accepted (SECURITY) | `db917230` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40339096027) |
