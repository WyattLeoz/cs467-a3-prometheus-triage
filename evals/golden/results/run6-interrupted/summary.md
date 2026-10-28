# Golden-set results: run6-interrupted

**4/10 cases pass.** Issues closed by a bot anywhere in the sandbox: 0 (closed by a maintainer: 1).

| Case | Expected | Labels applied | Comment | Result | Failed checks | Config commit | Run |
|------|----------|----------------|---------|--------|---------------|---------------|-----|
| A01 | NO_ACTION | — | no | PASS |  | `087bc648` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40462230995) |
| A02 | POSSIBLE_DUPLICATE | component/remote storage | yes | FAIL | outputs match declared decision | `087bc648` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40462874671) |
| A03 | NEEDS_INFO | component/tsdb | no | FAIL | labels within allowed set; declared decision accepted (ROUTE) | `087bc648` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40463761502) |
| A04 | POSSIBLE_DUPLICATE | component/promtool | yes | FAIL | outputs match declared decision | `087bc648` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40464562242) |
| G01 | GATED_SKIP | — | no | PASS |  | `087bc648` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40465414644) |
| G02 | NO_ACTION | — | no | PASS |  | `087bc648` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40465655567) |
| G03 | OTHER_PROJECT | component/config | no | FAIL | comment posted; labels within allowed set; comment cites /helm-charts|prometheus-operator/; declared decision accepted (ROUTE) | `087bc648` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40485929708) |
| G04 | OTHER_PROJECT | kind/more-info-needed | yes | FAIL | labels within allowed set; comment cites /postgres_exporter/; declared decision accepted (NEEDS_INFO) | `087bc648` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40486943006) |
| G05 | OTHER_PROJECT | component/agent | yes | FAIL | labels within allowed set; outputs match declared decision | `087bc648` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40487858832) |
| G06 | SUPPORT_QUESTION | kind/question | yes | PASS |  | `087bc648` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40488769755) |
