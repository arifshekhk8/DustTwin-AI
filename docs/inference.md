# Inference and measured replay — completed I1

1 October 2026, Asia/Dhaka. The local FastAPI service loads the pinned `ForecastModel` once and serializes model calls. Every prediction uses the frozen shared feature builder. No retraining, test tuning or arbitrary model upload is implemented.

## API contract

- `GET /health`: live readiness, model/artifact identity, task, horizon, grid interval and unavailable reason.
- `POST /v1/predict`: exact task, `OPC-N3`, `ug/m3`, `elapsed_seconds_per_recording`, 30-second horizon, integer issue time and 121 consecutive grid snapshots. Each snapshot includes its contributing native observation time. All snapshots end at issue time; observation times must be nondecreasing, at or before the snapshot and no more than 1.5 seconds old. These are prepared snapshots, not arbitrary irregular native rows. Native ingestion first needs the audited causal adapter.
- `GET /v1/replay`: six attributed validation/test recordings, source hashes and eligible clock bounds.
- `GET /v1/replay/{episode_id}?second=...`: only past measurements, current prediction and the forecast whose target has already matured at this clock. It never returns the current forecast's future recorded target.
- `GET /v1/evidence`: frozen model metadata, validation selection and final test evidence.

Responses include deterministic input snapshot hash, model/artifact/source, issue/target time, both baselines, the sixteen actual features, freshness, measured inference duration and explicit scope. A single endpoint yields “already exceeded”, “endpoint exceeds setting” or “endpoint below setting”; exact crossing ETA remains null. The illustrative 500 µg/m³ setting is not regulatory. The later site simulation must use a named trajectory method and a separate scope.

Malformed, duplicate/reordered/future/stale, wrong-unit/task/monitor/horizon, negative or nonfinite inputs receive 422 with specific errors. Missing live model receives 503 on prediction. Saved replay remains available with `saved_inference` clearly identified; it never presents cached output as a newly computed forecast.

## Offline replay export

`scripts/build_replay.py` exports six laboratory grids and outputs from the existing frozen artifact under `demo/replay/`. `index.json` pins every file hash and contains attribution, source DOI and CC BY 4.0 link. This export recomputes predictions for reproduction only; it performs no fit, parameter choice or new evaluation experiment.

The backing files contain entire saved recordings for offline use. The API returns only what is available at the chosen replay clock. The browser fallback will slice the same records by clock and label them as saved outputs. Inspecting a backing file is possible; controllers must never receive those future records.

## Verification

Fifteen focused Python tests pass. All five fixed validation fixtures agree with `POST /v1/predict` to eight decimal places. Tests cover future/duplicate/stale timestamps, nonfinite/negative data, wrong task/units/horizon/monitor, delayed actual-target reveal and equality of live/saved replay. The first snapshot at 120 seconds has no matured forecast; its recorded target is revealed at 150 seconds. Missing-model health, 503 and labelled backup behavior pass.

```sh
.venv/bin/python -m pip install -r requirements-service.txt
.venv/bin/python scripts/build_replay.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/serve.py
```

Python dependency versions are pinned. A deprecation notice from Starlette concerns its HTTPX test client; the pinned client passes the tests. Browser agreement and complete offline rehearsal are later gates; this milestone alone does not claim them.
