# Continue from here

Last updated: 1 October 2026, 10:19 Asia/Dhaka, after D2–M2 and release verification in the first scheduled continuation. Read this file with `AGENTS.md`, `plan.md` and `docs/decisions.md` before editing.

## Repository and scope

- Workspace: `/Users/arif/Documents/Techfest, IIT Bombay/DustTwin-AI`.
- Public remote: <https://github.com/arifshekhk8/DustTwin-AI>, branch `main`.
- Round 1 is software: a trained monitor forecast, recorded replay, website and explicitly simulated site control. Hardware remains deferred.
- Commit/push coherent verified milestones with the configured author and natural messages, without AI-contribution tags or authorship trailers.

## Current state

**P0 through W1 are complete. J1 is next.** The local service, measured replay and common site simulation exist. Twenty Python tests pass; all twenty scenario/controller runs have independently verified trace-derived metrics. The user requires all remaining software work today (D011). Website, browser agreement and offline presentation still need completion.

W1 now passes build and browser gates; J1 packaging and timed rehearsal are running. Keep measured forecasting separate from simulated site control throughout these remaining milestones.

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

Published prerelease [First measured PM10 forecast](https://github.com/arifshekhk8/DustTwin-AI/releases/tag/pm10-model-v1), tag `pm10-model-v1` at M2 commit `6497074`. Five uploaded assets include the fitted model, metadata, model card, validation selection and final metrics. GitHub's binary size/SHA-256 match the local artifact. `scripts/download_model.py --output tmp/model-download-check/pm10-initial.joblib` independently downloaded and verified the public asset; a cached rerun passed. Local model inference is usable offline after setup; the full website/judge demo is not built yet.

Preserve this initial artifact/evidence. Do not run a new search using group 4; a later research task needs a new untouched evaluation group/site. Published source hashes and local Markdown links also passed verification.

## I1 implementation completed in the follow-up session

Added `src/dusttwin/inference.py`, `replay.py`, the local FastAPI app and launcher; pinned service requirements. Exported six CC BY attributed, hash-pinned recording/forecast files under `demo/replay/`. Shared feature/model path, strict freshness/time validation, no future target reveal and unavailable-model saved fallback pass tests. Read `docs/inference.md` for the exact implemented contract.

The team is CTRL_V with the four user-supplied names in `configs/team.json`. Team ID has not been issued. Contact/qualification are not invented. Finish the remaining software today per D011, rather than waiting for tomorrow's automation.

## Earlier I1 handover (completed; retained for context)

1. Inspect worktree/history/remote and read `docs/architecture.md`, the model card and D010. Confirm the saved/downloaded model hash. Use `.venv/bin/python scripts/verify_model.py`; do not redo selection or evaluate a replacement on group 4.
2. Pin FastAPI/service dependencies. Implement the planned local service under `services/inference/`, loading `ForecastModel` once. Validate task/OPC-N3 monitor, units, clock, issue time, causal history and frozen freshness. No future values, arbitrary model uploads or fabricated confidence/ETA.
3. Define the replay contract from actual per-recording grids and the frozen artifact. Keep native observation times/freshness visible; reveal actual targets only when the recorded clock reaches them. Return both labelled baselines with the learned output. Preserve input-snapshot IDs and discard stale responses.
4. Check exact agreement between the saved fixture/shared history inference and API, plus missing/stale data, malformed/nonfinite inputs, wrong task/units/horizon and future timestamps. Save an attributed local replay/evidence fixture for offline use. Do not claim browser agreement until a browser interface exists.
5. Commit/push verified I1 and update this handover. Then S1 shared strategy simulation, W1 original React/TypeScript interface and J1 offline ten-minute rehearsal. Read the reference review for known water/ambient/zone/switching defects; derive simulation numbers from traces.

## S1 completed in the follow-up session

Implemented one common site plant, four controllers and five frozen cases. The predictor uses only observed past synthetic source-proxy readings; spatial mapping and the endpoint-to-trajectory method are explicit simulation assumptions. Background is preserved; wind-from conversion, two-edge risk, equal actuator timing and dropout fallback are implemented. Twenty tests pass, plus independent checks of all 9,600 intervals. Read `docs/simulation.md` for full mixed results. Predictive uses more water than reactive in the higher-risk cases; continuous has lower mean concentration and much greater water use. No physical effectiveness claim.

## Earlier S1 handover (completed)

Implement one common transport/actuator runner, no-control/continuous/reactive/predictive controllers, identical plant/nozzle assumptions, A=north/B=east/C=south/D=west, meteorological wind-from conversion, preserved background and equal switching limits. Predictive control may use only past source-proxy readings and the frozen artifact; spatial mapping and endpoint-to-trajectory assumptions must be explicit simulation assumptions. Freeze low-risk, east, diagonal, wind-shift and data-loss cases. Export all controller traces and derive every metric from them; verify determinism, water, ambient floor, risk coverage, unavailable input and ETA states. Then build W1 and J1 today.

## Exact next task: W1 original interface, then J1 today

Build the original React/TypeScript website in `apps/web/` with overview, measured replay, site experiment, honest results, proposed Round 2 hardware, CTRL_V team and presentation. Dependencies are installed/pinned with zero reported vulnerabilities. Consume the shared API; provide labelled saved replay/scenario fallback. Verify browser/API/fixture agreement, stale-response protection, pause/reset/speed/seek, custom assumptions and mobile layout. Then export the ten-minute presentation/evidence, cost basis and offline archive; rehearse without external requests, tag/release and push the final handover.

## Remaining dependencies and limits

- One laboratory instrument/setup does not establish outdoor boundary forecasting, calibrated reference accuracy or misting effectiveness. Site transport/control remains a labelled simulation.
- Original frontend reuse permission is not recorded. Implement our own interface unless a license or permission is supplied; this need not block progress.
- Actual Team ID, registered members/contact details, current organizer instructions, supplier prices and judge feedback require real team/source information.
- Supplied event information lists the zonal on 3 October 2026. Prioritize verified local/offline software. Hardware requires explicit team instruction.

## Reference review and daily continuation

The original review is `/Users/arif/Documents/Techfest, IIT Bombay/DustTwin_Review.md`, at source commit `dbb7386e384827fbae7e4571357d2491f4103fdf`. Its heuristic-engine results and 26 tests do not verify this new project.

The app confirmed ACTIVE daily continuation `continue-dusttwin-daily` at 09:00 Asia/Dhaka, targeting chat `01a0da1e-d23f-7c61-8109-073351b29767`. The first scheduled run on 1 October completed D2, M1 and M2. The next scheduled run is 2 October at 09:00 Dhaka, or a manual session can advance I1 sooner. The computer and Codex app must be running.

## Git verification

D1 was verified through `444c624`; today's D2 (`9b04d27`), frozen fit rules (`5050bb2`), M1 (`435c93a`) and M2 (`6497074`) were committed/pushed with the configured author. No contribution trailers or empty commits. At 10:19 Dhaka, local HEAD, `origin/main` and GitHub API HEAD all equal `64970744b318d3b87fe3e5bd995ee290de8c6c93`, with a clean worktree before this handover edit. The public release is verified.

Commit/push this final checkpoint and confirm equality/cleanliness again before ending. The final checkpoint hash is read from Git at the next session; it cannot be embedded in its own file. Bulk data, environment, temporary verification download and fitted binary remain ignored by ordinary Git. If the checkpoint push fails, record it as pending.

## W1 completed today

Original seven-page React/TypeScript dashboard built. Five Playwright journeys passed (8.1 seconds), including all five fixed fixture predictions to 1e-8, API/display agreement, clock-only actual reveal, delayed response rejection, playback, diagonal risk, dropout, changed flow and standalone saved fallback. All pages and 390-pixel mobile layouts pass; desktop/mobile screenshots were inspected and icon scaling repaired. Twenty Python tests and all 9,600 simulation intervals remain verified. Read `docs/website.md`.

J1 next: finish sourced feasibility notes, ten-minute script, PDF evidence packet, verified offline archive and tagged release. The ten-minute software rehearsal is active with external browser requests denied. Do not call it passed until its result exists. Human spoken rehearsal remains for the team.
