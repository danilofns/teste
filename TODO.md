# TODO — Dashboard de Produtividade (ContraDito / VeritasIA)

- [x] Criar `docs/productivity/collect_metrics.py` (script idempotente; usa PyGithub; gera `docs/productivity/metrics.json` no schema da spec)
- [x] Criar `docs/productivity/requirements.txt` (PyGithub)

- [x] Criar workflow `.github/workflows/metrics.yml` (cron domingo 03:00 UTC + workflow_dispatch; roda script; commita metrics.json no branch main)

- [x] Criar `docs/productivity/index.html` (página estática responsiva; carrega metrics.json; renderiza 7 gráficos + 3 tabelas de ranking)

- [x] Validar localmente: `python docs/productivity/collect_metrics.py` (checagem sintática) + `metrics.json` mock

- [x] Rodar sanity check: JSON válido + console sem erros (ao menos com um metrics.json mock)


