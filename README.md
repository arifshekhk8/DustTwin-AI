# DustTwin AI

DustTwin is a software prototype for forecasting construction dust and demonstrating how an urban construction site could select misting zones before dust reaches its perimeter.

For InnovateX Round 1, the project combines a trained particulate-matter forecasting model, replay of recorded data, an interactive site simulation and traceable strategy comparisons. Physical sensors and misting hardware belong to Round 2.

## Current status

The data audit, causal preparation, model training and held-out evaluation are complete. The saved model predicts laboratory PM10 30 seconds ahead from two minutes of past readings. On 15,065 held-out windows, its MAE is **88.405 µg/m³**, compared with persistence **95.702** and trailing mean **81.565**. The learned model improves on persistence but loses to the trailing mean on MAE; warnings and abrupt-onset prediction remain weak. See the [model card](models/model-card.md) for full results and failures.

The model, validated local inference service, original seven-page website and fair four-strategy/five-case simulation are implemented. Twenty Python tests, five browser journeys, all 9,600 simulation intervals and a real ten-minute software rehearsal with external browser requests denied pass. The seven-page judge packet is visually verified. No field boundary accuracy, misting effectiveness or physical water savings have been demonstrated.

## Open the demonstration

On the prepared Mac, double-click **Start DustTwin.command** and confirm **Local model ready**. It opens <http://127.0.0.1:8000> after the server is ready. Keep its terminal open.

For a saved-only backup, use **Start Saved Replay.command** at <http://127.0.0.1:8001>. This mode shows previously computed predictions and traces; it does not execute the learned model or rerun assumptions.

The [Round 1 release](https://github.com/arifshekhk8/DustTwin-AI/releases/tag/round1-demo-v1) includes the ready-built offline archive, frozen model, evidence and PDF. See [offline instructions](docs/offline-demo.md) for another computer or a source checkout. Saved mode needs only Python 3 and a modern browser. Live mode requires Python 3.14 and the pinned service packages installed once. No internet or Node is needed during the prepared demonstration.

The website includes Overview, AI replay, Site experiment, Evidence & results, Round 2 design, Our team and Present. The user-supplied team is **CTRL_V**, Theme 2; all four approved names are displayed. Team ID is labelled not issued. The team must still practice spoken delivery and check venue projection; software checks do not verify a human presentation.

## Start here

- [plan.md](plan.md): scope, milestones, deliverables and acceptance criteria.
- [following.md](following.md): current state and the exact next actions.
- [AGENTS.md](AGENTS.md): instructions for future work sessions.
- [Dataset shortlist](docs/dataset-shortlist.md): primary sources and suitability checks.
- [Dataset audit](docs/dataset-audit.md): downloaded-file findings and quality plots.
- [Forecast task](configs/forecast-task.json): accepted signal, clock, freshness and group assignments.
- [Causal preparation](docs/preparation.md): exact features, eligible windows, provenance and validation baselines.
- [Training comparison](docs/training.md): seven candidates, selection and actual M4 fit timings.
- [Model card](models/model-card.md): final errors, warning failures, limitations and artifact.
- [Evaluation protocol](docs/evaluation.md): frozen task and evaluation gates.
- [Architecture](docs/architecture.md): model, API, replay and site-control boundaries.
- [Round 1 checklist](docs/round1-checklist.md): presentation readiness.
- [Website and browser checks](docs/website.md): build, playback and live/saved modes.
- [Inference contract](docs/inference.md): validated causal input and API.
- [Simulation evidence](docs/simulation.md): common plant, five cases and mixed results.
- [Feasibility and costs](docs/feasibility.md): dated listings, missing quotes and pilot gates.
- [Ten-minute judge script](docs/judge-script.md): timed story and likely questions.
- [Judge PDF](output/pdf/dusttwin-judge-packet.pdf): printable evidence packet.
- [Readiness reports](reports/readiness): actual checks and offline rehearsal scope.
- [Third-party notices](docs/third-party-notices.md): redistributed frontend licenses.

## Reference frontend

The existing [meherabmehu/DustTwin](https://github.com/meherabmehu/DustTwin) frontend was reviewed at `dbb7386e384827fbae7e4571357d2491f4103fdf`. This repository implements its own original interface; no reference source was imported because a reuse license was not recorded.

## Reproduce the data audit

The current audit environment was verified on Python 3.14.6 / Apple M4. Downloads require `curl`; numeric extraction was also cross-checked with bundled Python 3.12 libraries.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-audit.txt
.venv/bin/python scripts/download_data.py
.venv/bin/python scripts/audit_filtered_candidate.py
.venv/bin/python scripts/audit_raw_profiles.py
```

Original downloads and bulk prepared arrays are ignored by Git. Source versions, filenames and verified SHA-256 hashes are recorded in [the manifest](data/manifest.json). Audit outputs, trained-model metadata, evaluation metrics, compressed forecast traces and derived plots are committed.

Prepare and verify the frozen forecast task:

```sh
.venv/bin/python scripts/prepare_data.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/verify_preparation.py
```

## Use the trained model

Use Python 3.14 and the pinned model environment. Install once, then fetch the [54.7 kB fitted model release](https://github.com/arifshekhk8/DustTwin-AI/releases/tag/pm10-model-v1):

```sh
.venv/bin/python -m pip install -r requirements-model.txt
.venv/bin/python scripts/download_model.py
.venv/bin/python scripts/verify_model.py
.venv/bin/python -m unittest discover -s tests -v
```

The downloader checks the pinned size and SHA-256 before installing. Model inference and its fixture work without network after setup. Final evidence is in [reports/evaluation](reports/evaluation); `scripts/verify_evaluation.py` checks metrics against the complete exported traces after data preparation. `scripts/evaluate_model.py` verifies frozen evidence on subsequent runs rather than selecting a different model.

To reproduce training, acquire/prepare the data, install `requirements-model.txt` and run `scripts/train_models.py`. Keep the published initial evidence/artifact intact. Do not tune against the now-revealed test group; a new model research experiment needs a new untouched evaluation set.

## Dataset attribution

- **Accepted laboratory task:** Komiljon Askarov and Jae-ho Choi (2024), [Data on different particulate matter profiles produced in laboratory from construction activity and outdoor monitoring](https://data.mendeley.com/datasets/7f22n9v7hp/1), Mendeley Data V1, DOI `10.17632/7f22n9v7hp.1`, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Audit summaries/plots are derived from the original raw OPC-N3 files. Source files are unchanged; causal preparation changes will be recorded before training. This project is not endorsed by the dataset contributors.
- **Rejected raw-forecast candidate, descriptive audit only:** Daniel Cheriyan (2020), [Data on different sized particulate matter concentration produced from a construction activity](https://data.mendeley.com/datasets/6fd493866k/1), Mendeley Data V1, DOI `10.17632/6fd493866k.1`, CC BY 4.0. The audit plots the supplied ten-minute moving averages; originals are unchanged.

## Work and history

Work will be recorded in small, meaningful commits using the configured Git author, with a push after each completed milestone. Each session updates `following.md` with results, validation, unresolved issues and the next task. Daily continuation is active at 09:00 Asia/Dhaka in the current Codex chat. The local computer and app must be running; setup details are recorded in `following.md`.
