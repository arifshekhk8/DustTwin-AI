# DustTwin AI

DustTwin is a software prototype for forecasting construction dust and demonstrating how an urban construction site could select misting zones before dust reaches its perimeter.

For InnovateX Round 1, the project will combine a trained particulate-matter forecasting model, replay of recorded data, an interactive site simulation and traceable strategy comparisons. Physical sensors and misting hardware belong to Round 2.

## Current status

Planning and the first dataset audit are complete. The initial 2020 workbook was rejected for raw forecasting because it contains ten-minute moving averages. A newer verified dataset supplies twelve raw laboratory OPC-N3 recordings with 53,717 rows, accepted for a preliminary 30-second PM10 forecast. Causal preparation and model training are next. Inference services and the website have not been implemented here.

## Start here

- [plan.md](plan.md): scope, milestones, deliverables and acceptance criteria.
- [following.md](following.md): current state and the exact next actions.
- [AGENTS.md](AGENTS.md): instructions for future work sessions.
- [Dataset shortlist](docs/dataset-shortlist.md): primary sources and suitability checks.
- [Dataset audit](docs/dataset-audit.md): downloaded-file findings and quality plots.
- [Forecast task](configs/forecast-task.json): accepted signal, clock, freshness and group assignments.
- [Evaluation protocol](docs/evaluation.md): frozen task and evaluation gates.
- [Architecture](docs/architecture.md): model, API, replay and site-control boundaries.
- [Round 1 checklist](docs/round1-checklist.md): presentation readiness.

## Reference frontend

The existing [meherabmehu/DustTwin](https://github.com/meherabmehu/DustTwin) frontend was reviewed at `dbb7386e384827fbae7e4571357d2491f4103fdf`. This new repository starts with original project planning documents. Before importing that frontend, record permission to reuse its code or implement the required interface here using our own code. The source repository currently exposes no license.

## Reproduce the data audit

The current audit environment was verified on Python 3.14.6 / Apple M4. Downloads require `curl`; numeric extraction was also cross-checked with bundled Python 3.12 libraries.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-audit.txt
.venv/bin/python scripts/download_data.py
.venv/bin/python scripts/audit_filtered_candidate.py
.venv/bin/python scripts/audit_raw_profiles.py
```

Original downloads are ignored by Git. Source versions, filenames and verified SHA-256 hashes are recorded in [the manifest](data/manifest.json). Small aggregate audit outputs and derived plots are committed. No trained-model metrics exist yet.

## Dataset attribution

- **Accepted laboratory task:** Komiljon Askarov and Jae-ho Choi (2024), [Data on different particulate matter profiles produced in laboratory from construction activity and outdoor monitoring](https://data.mendeley.com/datasets/7f22n9v7hp/1), Mendeley Data V1, DOI `10.17632/7f22n9v7hp.1`, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Audit summaries/plots are derived from the original raw OPC-N3 files. Source files are unchanged; causal preparation changes will be recorded before training. This project is not endorsed by the dataset contributors.
- **Rejected raw-forecast candidate, descriptive audit only:** Daniel Cheriyan (2020), [Data on different sized particulate matter concentration produced from a construction activity](https://data.mendeley.com/datasets/6fd493866k/1), Mendeley Data V1, DOI `10.17632/6fd493866k.1`, CC BY 4.0. The audit plots the supplied ten-minute moving averages; originals are unchanged.

## Work and history

Work will be recorded in small, meaningful commits using the configured Git author, with a push after each completed milestone. Each session updates `following.md` with results, validation, unresolved issues and the next task. Daily continuation is active at 09:00 Asia/Dhaka in the current Codex chat. The local computer and app must be running; setup details are recorded in `following.md`.
