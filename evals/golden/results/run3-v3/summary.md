# Golden-set results: run3-v3

**2/5 cases pass.** Issues closed by a bot anywhere in the sandbox: 0 (closed by a maintainer: 0).

| Case | Expected | Labels applied | Comment | Result | Failed checks | Config commit | Run |
|------|----------|----------------|---------|--------|---------------|---------------|-----|
| A02 | POSSIBLE_DUPLICATE | component/remote storage | yes | FAIL | outputs match declared decision | `a8aa7063` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40157992984) |
| G12 | ROUTE | component/service discovery | no | PASS |  | `e0438ecf` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40175318180) |
| G13 | ROUTE | component/agent | no | PASS |  | `e0438ecf` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40175815108) |
| G14 | ROUTE | — | no | FAIL | outputs vetted and published; required labels present; outputs match declared decision | `44229edc` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40195543914) |
| G15 | ROUTE | component/api, kind/feature | no | FAIL | labels within allowed set | `44229edc` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40196176702) |
