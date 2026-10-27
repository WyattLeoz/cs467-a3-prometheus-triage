# Golden-set results: run2

**9/19 cases pass.** Issues closed by a bot anywhere in the sandbox: 0 (closed by a maintainer: 0).

| Case | Expected | Labels applied | Comment | Result | Failed checks | Config commit | Run |
|------|----------|----------------|---------|--------|---------------|---------------|-----|
| A01 | NO_ACTION | — | no | PASS |  | `b6428fc1` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40024334167) |
| A02 | POSSIBLE_DUPLICATE | component/tsdb | yes | FAIL | labels within allowed set; outputs match declared decision | `473873c9` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40025252072) |
| A03 | NEEDS_INFO | — | no | FAIL | declared decision accepted (ROUTE); outputs match declared decision | `6769ac41` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40026233992) |
| G01 | GATED_SKIP | — | no | PASS |  | `0e6607e6` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40027081084) |
| G02 | NO_ACTION | — | no | PASS |  | `2729a503` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40027444395) |
| G03 | OTHER_PROJECT | — | no | FAIL | outputs vetted and published; comment posted; comment cites /helm-charts|prometheus-operator/; outputs match declared decision | `e7cf7383` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40052768985) |
| G04 | OTHER_PROJECT | kind/more-info-needed | yes | FAIL | labels within allowed set; comment cites /postgres_exporter/; declared decision accepted (NEEDS_INFO) | `e67bef1a` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40072337381) |
| G05 | OTHER_PROJECT | — | yes | PASS |  | `e67bef1a` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40072852557) |
| G06 | SUPPORT_QUESTION | kind/question | yes | PASS |  | `6befc5ca` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40073313293) |
| G07 | NEEDS_INFO | kind/more-info-needed | yes | PASS |  | `6befc5ca` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40073843243) |
| G08 | NEEDS_INFO | kind/more-info-needed | yes | PASS |  | `8dc8a4fb` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40092757184) |
| G09 | POSSIBLE_DUPLICATE | — | no | FAIL | outputs vetted and published; comment posted; comment cites /17437/; declared decision accepted (ROUTE); outputs match declared decision | `8dc8a4fb` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40093315965) |
| G10 | POSSIBLE_DUPLICATE | component/api | yes | PASS |  | `897f4a6f` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40114590367) |
| G11 | ROUTE | component/mixin | no | PASS |  | `897f4a6f` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40115335252) |
| G12 | ROUTE | — | no | FAIL | agent job succeeded; required labels present; declared decision accepted (None); outputs match declared decision | `4d5c6a1e` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40137333324) |
| G13 | ROUTE | — | no | FAIL | outputs vetted and published; required labels present; outputs match declared decision | `281568d0` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40138003590) |
| G14 | ROUTE | kind/feature | no | FAIL | required labels present | `281568d0` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40138851031) |
| G15 | ROUTE | — | no | FAIL | outputs vetted and published; outputs match declared decision | `4f884d42` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40156979740) |
| G16 | POSSIBLE_DUPLICATE | — | yes | FAIL | comment cites /17314/; declared decision accepted (SECURITY) | `4f884d42` | [run](https://github.com/WyattLeoz/cs467-a3-prometheus-triage/actions/runs/40157510681) |
