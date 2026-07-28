

```plaintext
medsearch/
├── README.md                  # Vitrine recruteur (§11)
├── Makefile                   # Point d'entrée unique de TOUT
├── pyproject.toml             # Un seul package installable en editable (tu connais)
├── docker-compose.yml         # ES + Kibana + Prometheus + Grafana + API
├── .github/workflows/ci.yml   # lint + typage + tests + éval de régression
├── configs/                   # YAML versionnés : corpus, index, retrieval, eval
│   ├── corpus.yaml            #   sources, filtres PubMed, tailles de chunk
│   ├── index_v*.yaml          #   mappings ES, params HNSW — 1 fichier = 1 version d'index
│   └── retrieval.yaml         #   profondeurs, k RRF, profondeur rerank, flags query processing
├── src/medsearch/
│   ├── ingestion/             # fetch_pubmed.py, fetch_has.py, fetch_bdpm.py, fetch_mesh.py
│   ├── parsing/               # pdf_parser.py, bdpm_parser.py, schemas.py (Pydantic)
│   ├── chunking/              # chunker structurel + tests sur documents réels
│   ├── indexing/              # embeddings batch, création index ES, alias blue/green
│   ├── retrieval/             # bm25.py, dense.py, fusion.py (RRF), pipeline.py
│   ├── query/                 # spell.py, expansion.py, patient_norm.py, lang.py
│   ├── reranking/             # reranker.py, onnx_export.py, training/ (S10)
│   ├── evaluation/            # runner ir_measures, bootstrap, rapport auto
│   └── api/                   # app FastAPI, routes, middlewares métriques
├── data/                      # ⚠️ .gitignore sauf eval/ ; jamais de PDF sources commités
│   ├── raw/  interim/  processed/
│   └── eval/                  # queries.tsv, qrels_v1.tsv — VERSIONNÉ dans git (petit et précieux)
├── notebooks/                 # corpus_stats, analyses d'erreurs — exploratoire uniquement
├── scripts/                   # locustfile.py, scale_campaign.py, demo_space/
├── tests/
│   ├── unit/  integration/    # integration = contre un ES docker éphémère
│   └── regression/            # éval retrieval vs métriques de référence commitées
└── docs/
    ├── architecture.md  experiments_report.md  latency_report.md
    ├── decisions/             # ADR courts : « pourquoi pas Kafka », « go/no-go fine-tuning »…
    └── interview_prep.md
```