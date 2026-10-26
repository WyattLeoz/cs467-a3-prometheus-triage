# Golden-set results: run4-final

**5/13 cases pass.** Issues closed anywhere in the sandbox: 0.

| Case | Expected | Labels applied | Comment | Result | Failed checks | Run |
|------|----------|----------------|---------|--------|---------------|-----|
| A01 | NO_ACTION | — | no | FAIL | skill loaded (skill tool call); deterministic check output read | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40198028497) |
| A02 | POSSIBLE_DUPLICATE | component/remote storage | yes | PASS |  | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40198526621) |
| A03 | NEEDS_INFO | component/tsdb | no | FAIL | labels within allowed set | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40199127264) |
| G01 | GATED_SKIP | — | no | PASS |  | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40199713185) |
| G02 | NO_ACTION | — | no | FAIL | outputs vetted and published | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40219466338) |
| G03 | OTHER_PROJECT | component/otlp | yes | FAIL | labels within allowed set | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40243401707) |
| G04 | OTHER_PROJECT | kind/more-info-needed | yes | FAIL | labels within allowed set; comment cites /postgres_exporter/ | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40244041347) |
| G05 | OTHER_PROJECT | — | yes | PASS |  | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40244718505) |
| G06 | SUPPORT_QUESTION | kind/question | yes | PASS |  | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40245382423) |
| G07 | NEEDS_INFO | kind/more-info-needed | yes | PASS |  | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40267374610) |
| G08 | NEEDS_INFO | component/remote storage | no | FAIL | comment posted; labels within allowed set | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40268140038) |
| G09 | POSSIBLE_DUPLICATE | component/otlp | no | FAIL | comment posted; comment cites /17437/ | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40268907609) |
| G10 | POSSIBLE_DUPLICATE | component/api | yes | FAIL | comment cites /17512/ | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40269544339) |
