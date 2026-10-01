# Continue from here

Last updated: 1 October 2026, Asia/Dhaka, after D2–M2 in the first scheduled continuation. Read this file with `AGENTS.md`, `plan.md` and `docs/decisions.md` before editing.

## Repository and scope

- Workspace: `/Users/arif/Documents/Techfest, IIT Bombay/DustTwin-AI`.
- Public remote: <https://github.com/arifshekhk8/DustTwin-AI>, branch `main`.
- Round 1 is software: a trained monitor forecast, recorded replay, website and explicitly simulated site control. Hardware remains deferred.
- Commit/push coherent verified milestones with the configured author and natural messages, without AI-contribution tags or authorship trailers.

## Current state

**P0, D1, D2, M1 and M2 are complete. I1 is next.** The selected model is `hist_gb_depth3_iter100`, trained only on groups 1/2 and chosen using group 3 validation. The artifact reloads and reproduces the fixture; held-out results are published honestly. No water saving has been computed. No inference service or website exists in this new repository yet.

I1 integration, S1 simulation, W1 website and J1 presentation remain incomplete. Keep measured forecasting separate from simulated site control throughout these remaining milestones.

## Accepted data and frozen choices

- Source: Komiljon Askarov and Jae-ho Choi (2024), DOI `10.17632/7f22n9v7hp.1`, CC BY 4.0. Attribution is in the README and audit.
- A verified 5,312,710-byte nested ZIP is under ignored `data/raw/mendeley-7f22n9v7hp-v1/`.
- Twelve laboratory OPC-N3 recordings have 53,717 rows, about 14.94 recorded hours, in four labelled experiment groups. Two outdoor recordings contain 7,692 more rows and are excluded from the first model.
- Select raw `PM10(ug/m3)`. Exclude `RollMean_*`, analysed workbooks and other instruments. First features use past PM10 only.
- Native logging cadence is approximately one second. Three lab files have no calendar date. Some rounded clocks have duplicates/gaps. No invented dates or strictly chronological group ordering.
- Freeze a one-second elapsed grid with the latest raw reading at or before each grid time. Keep the last original row for duplicate timestamps and count removals. Snapshots older than 1.5 seconds are unavailable.
- Use a 120-second inclusive history (121 snapshots), forecasting the latest observed snapshot 30 seconds ahead. Reject any window with unavailable history or target. Never bridge recordings.
- Whole-group partitions: groups 1/2 training, group 3 validation, group 4 final test. Group 4 is labelled temperature increased, a disclosed changed-condition test. Raw row counts are not prepared window counts.
- Do not use event elapsed time, drilling labels, episode identity or future activity context as learned features.
- Authoritative configuration: `configs/forecast-task.json`; decision D008; methods in `docs/evaluation.md`.

## Completed this implementation session

1. Added pinned acquisition configuration, `scripts/download_data.py` and `data/manifest.json`, with filenames, versions, sizes, license terms and SHA-256 hashes. Atomic downloads and cached verification work.
2. Audited `6fd493866k.1`. The actual file contains only PM10 ten-minute moving averages, contrary to its raw multi-pollutant description. A3 has 270 missing initial rows. Rejected it for raw 30-second forecasting in D007; retained descriptive audit evidence.
3. Found and acquired `7f22n9v7hp.1`. A 60-second download timeout was too short on this connection; a 300-second allowance completed the verified file.
4. Added `src/dusttwin/data.py` and `scripts/audit_raw_profiles.py`. The archive contains 56 files, including fourteen raw OPC CSV recordings. Archives are read in memory without blindly extracting paths.
5. Published distributions, cadence diagnostics, member hashes and quality plots in `reports/data-audit/`. No OPC pair shares an identical ten-row PM triplet sequence. This checks duplicate content, not statistical independence.
6. Accepted the narrower laboratory task in D008. Updated the plan, evaluation protocol and README. Five meaningful implementation commits were pushed through `ef42ae3` before this checkpoint.

## Evidence and verification

Read `docs/dataset-audit.md` for actual counts, field choices, quality policies and limits. `reports/data-audit/` contains JSON summaries for both candidates, the 2024 inventory and visually inspected profile plots. These are measured-data audit plots, not AI predictions.

The local `.venv` uses Python 3.14.6. Exact audit dependencies are in `requirements-audit.txt`; installed training dependencies are pinned in `requirements-model.txt`. Extraction was independently cross-checked with bundled Python 3.12/numpy/openpyxl.

```sh
.venv/bin/python scripts/download_data.py
.venv/bin/python scripts/audit_filtered_candidate.py
.venv/bin/python scripts/audit_raw_profiles.py
```

Both completed downloads and cached reruns passed their published hash checks. Originals are unchanged. Direct checks passed for raw-column selection, known OLE-date conversion, time-only parsing, 53,717 lab rows, the 56-file inventory and twelve disjoint partitioned lab recordings. All inspected pollutant/context fields were finite and populated; no negative PM was found. Both plots were visually inspected. Links and whitespace passed. These are D1 quality checks, not trained-model tests.

## First daily run: completed D2

Added shared causal preparation, sixteen frozen PM10 features, prepared partitions and per-recording grids retaining contributing native observation times/ages/row indices. Removed eighteen duplicate rows. Prepared 24,818 training, 12,113 validation and 15,065 test windows. No remaining candidate window fails freshness. See `docs/preparation.md` and `reports/preparation/split-manifest.json`.

Six focused preparation tests passed. Independent native-file verification passed for all 51,996 windows. Validation persistence MAE/RMSE: 150.493/392.608 µg/m³; trailing mean: 132.725/407.965 µg/m³. At the D2 checkpoint, no final test model errors had been inspected. Model libraries were installed and pinned before fitting.

## First daily run: completed M1

Pinned `requirements-model.txt` and froze seven candidates plus descriptive event rules in `5050bb2` before fitting. Selected depth-3, 100-iteration histogram boosting by validation MAE (117.186 µg/m³; RMSE 305.217), versus persistence 150.493/392.608. Validation MAE improvement is 22.13%, not pollution reduction or final accuracy. All candidate/per-recording results and settings are in `reports/training/validation-selection.json`.

The M4 used 0.2133 seconds for all seven fits and 0.3163 seconds for the run excluding imports. The 54,679-byte artifact is ignored at `models/artifacts/pm10-initial.joblib`; its SHA-256 is `d78f1b37269f72af45933e01722968fb13ed82178f6d8b3e4c5584d46cec09c7`. Metadata, dependency/config/source hashes and the fixed fixture are public. Fresh-process verification passed for feature and history inference. Training-only scaling and disabled random early stopping passed. Test remained unscored until this selected artifact was committed/pushed in `435c93a`.

## First daily run: completed M2

Evaluated the frozen artifact once on all 15,065 eligible group-4 windows. Test MAE/RMSE (µg/m³): model **88.405/179.272**, persistence **95.702/199.384**, trailing mean **81.565/200.713**. Model MAE is 7.62% below persistence but 8.39% above trailing mean. It fails materially on the ten-second-label recording and abrupt rises; the model/selection has not been changed to improve test results. D010 records this decision.

At the frozen illustrative 500 µg/m³ setting, the model matches 13/18 threshold runs with 15 false alerts, versus trailing mean 13/18 with 8 false alerts. Only one of three first onsets has a valid advance learned warning. Runs recross within three recordings and are not independent activity events. A 30-second forecast horizon is not a promise of 30-second warning lead.

Saved full compressed traces, pooled/per-recording errors, threshold-run results and three visually inspected plots in `reports/evaluation/`. `models/model-card.md` states the results and limits. Twelve focused tests pass with the artifact present. `scripts/verify_evaluation.py` independently recalculated every published pooled/per-recording error from the 15,065 CSV rows and checked freshness, time/horizon, masks and hashes. Evaluation reruns verify frozen evidence without model selection or rescoring.

Model release `pm10-model-v1` and `scripts/download_model.py` are the publication/verification step after this M2 commit. Preserve this initial artifact/evidence. Do not run a new search using group 4; a later research task needs a new untouched evaluation group/site.

## Exact next task: I1 inference and measured replay

1. Inspect worktree/history/remote and read `docs/architecture.md`, the model card and D010. Confirm the saved/downloaded model hash. Use `.venv/bin/python scripts/verify_model.py`; do not redo selection or evaluate a replacement on group 4.
2. Pin FastAPI/service dependencies. Implement the planned local service under `services/inference/`, loading `ForecastModel` once. Validate task/OPC-N3 monitor, units, clock, issue time, causal history and frozen freshness. No future values, arbitrary model uploads or fabricated confidence/ETA.
3. Define the replay contract from actual per-recording grids and the frozen artifact. Keep native observation times/freshness visible; reveal actual targets only when the recorded clock reaches them. Return both labelled baselines with the learned output. Preserve input-snapshot IDs and discard stale responses.
4. Check exact agreement between the saved fixture/shared history inference and API, plus missing/stale data, malformed/nonfinite inputs, wrong task/units/horizon and future timestamps. Save an attributed local replay/evidence fixture for offline use. Do not claim browser agreement until a browser interface exists.
5. Commit/push verified I1 and update this handover. Then S1 shared strategy simulation, W1 original React/TypeScript interface and J1 offline ten-minute rehearsal. Read the reference review for known water/ambient/zone/switching defects; derive simulation numbers from traces.

## Remaining dependencies and limits

- One laboratory instrument/setup does not establish outdoor boundary forecasting, calibrated reference accuracy or misting effectiveness. Site transport/control remains a labelled simulation.
- Original frontend reuse permission is not recorded. Implement our own interface unless a license or permission is supplied; this need not block progress.
- Actual Team ID, registered members/contact details, current organizer instructions, supplier prices and judge feedback require real team/source information.
- Supplied event information lists the zonal on 3 October 2026. Prioritize verified local/offline software. Hardware requires explicit team instruction.

## Reference review and daily continuation

The original review is `/Users/arif/Documents/Techfest, IIT Bombay/DustTwin_Review.md`, at source commit `dbb7386e384827fbae7e4571357d2491f4103fdf`. Its heuristic-engine results and 26 tests do not verify this new project.

The app confirmed ACTIVE daily continuation `continue-dusttwin-daily` at 09:00 Asia/Dhaka, targeting chat `01a0da1e-d23f-7c61-8109-073351b29767`. The first scheduled run on 1 October completed D2, M1 and M2. The next scheduled run is 2 October at 09:00 Dhaka, or a manual session can advance I1 sooner. The computer and Codex app must be running.

## Git verification

D1 was verified through `444c624`; today's D2 (`9b04d27`), frozen fit rules (`5050bb2`) and M1 (`435c93a`) were committed/pushed. M2 tests, source/array/artifact/evidence hashes and whitespace pass. Bulk data, environment and fitted binary remain ignored by ordinary Git. Publish M2, upload/verify the release artifact, then commit the final handover and confirm clean worktree and local/`origin/main`/GitHub HEAD equality. If a push fails, record it as pending.
