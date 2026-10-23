# Component map (prometheus/prometheus @ 22c287a, 2026-10-22)

Sources: upstream wiki "Label Names and Descriptions", upstream MAINTAINERS.md,
and the upstream directory tree (`upstream/TREE.txt`). Owners are for routing
context only — the agent never @-mentions them.

| Label | Code / topic | Typical keywords | Owners (MAINTAINERS.md) |
|-------|--------------|------------------|-------------------------|
| `component/agent` | `tsdb/agent`, `--agent` mode | agent mode, WAL in agent | @kgeckhart |
| `component/api` | `web/api/v1` | HTTP API, `/api/v1/...`, OpenAPI | general |
| `component/config` | `config/`, CLI flags | prometheus.yml parsing, flags | general |
| `component/documentation` | `docs/` | docs typo, unclear docs | general |
| `component/mixin` | `documentation/prometheus-mixin` | alerts.libsonnet, dashboards | @metalmatze |
| `component/notify` | `notifier/` | sending alerts to Alertmanager, notification queue | general |
| `component/otlp` | `storage/remote/otlptranslator`, OTLP receiver | OTLP, OpenTelemetry ingestion | @ArthurSens, @jesusvazquez |
| `component/promql` | `promql/` | query language, functions, histograms in queries | @vpranckaitis |
| `component/promtool` | `cmd/promtool` | promtool check/test/backfill | @dgl |
| `component/remote storage` | `storage/remote` | remote_write, remote_read, RW 2.0 | @cstyan, @tomwilkie, @alexgreenbank |
| `component/rules` | `rules/` | recording/alerting rule evaluation, alert state | general |
| `component/scraping` | `scrape/`, `model/textparse` | scrape loop, exposition parsing, relabeling at scrape | general |
| `component/service discovery` | `discovery/` | `*_sd_configs`, EC2/Azure/Kubernetes/Consul/file SD | per-SD owners |
| `component/tests` | tests, CI flakes | flaky test | general |
| `component/tsdb` | `tsdb/` | blocks, WAL, compaction, head, OOO | @codesome, @jesusvazquez |
| `component/ui` | `web/ui` | web UI, graph page, alerts page | @juliusv |
| `component/web` | `web/` (non-UI, non-API) | listen address, TLS, external URL | general |
| `component/wal` | WAL replay/segments | WAL replay | general |

Notes
- Rule evaluation that sends to Alertmanager: `component/rules` if the problem is
  *when* an alert fires/resolves, `component/notify` if it is *delivery*.
- Templates used in alert annotations (`template/`) have no dedicated label;
  use `component/rules`.
- Container-image CVE scanner reports concern the release process, not a code
  component; do not guess a component for them.
