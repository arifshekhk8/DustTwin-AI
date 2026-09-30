# Continue from here

Last updated: 1 October 2026, Asia/Dhaka, after the first manual implementation session. Read this file with `AGENTS.md`, `plan.md` and `docs/decisions.md` before editing.

## Repository and scope

- Workspace: `/Users/arif/Documents/Techfest, IIT Bombay/DustTwin-AI`.
- Public remote: <https://github.com/arifshekhk8/DustTwin-AI>, branch `main`.
- Round 1 is software: a trained monitor forecast, recorded replay, website and explicitly simulated site control. Hardware remains deferred.
- Commit/push coherent verified milestones with the configured author and natural messages, without AI-contribution tags or authorship trailers.

## Current state

**P0 and D1 are complete. D2 is next.** The initial construction workbook was downloaded and rejected for raw forecasting. A newer raw laboratory dataset is downloaded, audited and accepted. Task and partition rules are frozen. No model has been trained. No model accuracy or water saving has been demonstrated. No inference service or website exists in this new repository yet.

D2 preparation/baselines, M1 training, M2 final evaluation, I1 integration, S1 simulation, W1 website and J1 presentation remain incomplete. D2 has its configuration but no implementation. No final model test error has been computed.

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

The local `.venv` uses Python 3.14.6. Exact dependencies are in `requirements-audit.txt`. Extraction was independently cross-checked with bundled Python 3.12/numpy/openpyxl. Training dependencies are not installed yet.

```sh
.venv/bin/python scripts/download_data.py
.venv/bin/python scripts/audit_filtered_candidate.py
.venv/bin/python scripts/audit_raw_profiles.py
```

Both completed downloads and cached reruns passed their published hash checks. Originals are unchanged. Direct checks passed for raw-column selection, known OLE-date conversion, time-only parsing, 53,717 lab rows, the 56-file inventory and twelve disjoint partitioned lab recordings. All inspected pollutant/context fields were finite and populated; no negative PM was found. Both plots were visually inspected. Links and whitespace passed. These are D1 quality checks, not trained-model tests.

## Exact next task: D2 causal preparation

1. Check `git status --short`, recent history and `origin/main`. Read D008, the task configuration, evaluation protocol and parser. Reuse the completed audit; do not restart source selection.
2. Implement `src/dusttwin/preparation.py` and `scripts/prepare_data.py`. Use per-recording elapsed clocks, deterministic duplicate handling and causal one-second snapshots. Preserve contributing observation time/age. Never interpolate from future readings.
3. Build 121-snapshot histories and 30-second targets only where all required snapshots pass freshness. Record window exclusions/reasons. Keep group assignments fixed; put bulk prepared arrays under ignored `data/processed/`.
4. Add focused checks for future leakage, exact target time, duplicate handling, stale gaps and recording/partition separation. Verify them before training.
5. Produce persistence and preceding-60-second trailing-mean predictions on identical eligible samples. Publish validation baseline metrics and prepared split counts/manifests. Keep final test model errors for M2; do not tune against them.
6. Commit/push verified D2 and refresh this file. Then advance to M1: pin model dependencies, train planned ridge/small gradient-tree candidates, choose on validation, save/reload the artifact and measure actual M4 training time.

## Remaining dependencies and limits

- One laboratory instrument/setup does not establish outdoor boundary forecasting, calibrated reference accuracy or misting effectiveness. Site transport/control remains a labelled simulation.
- Original frontend reuse permission is not recorded. Implement our own interface unless a license or permission is supplied; this need not block progress.
- Actual Team ID, registered members/contact details, current organizer instructions, supplier prices and judge feedback require real team/source information.
- Supplied event information lists the zonal on 3 October 2026. Prioritize verified local/offline software. Hardware requires explicit team instruction.

## Reference review and daily continuation

The original review is `/Users/arif/Documents/Techfest, IIT Bombay/DustTwin_Review.md`, at source commit `dbb7386e384827fbae7e4571357d2491f4103fdf`. Its heuristic-engine results and 26 tests do not verify this new project.

The app previously confirmed ACTIVE daily continuation `continue-dusttwin-daily` at 09:00 Asia/Dhaka, targeting chat `01a0da1e-d23f-7c61-8109-073351b29767`. This session was manual; no scheduled run has completed in the recorded history. The computer and Codex app must be running. The next run starts with D2, verifies progress, commits/pushes and refreshes this handover.

## Git verification

All five D1 milestones were confirmed on GitHub through `ef42ae3`. Source hashes, document links and whitespace passed. Bulk data and the environment are untracked. Publish this checkpoint, then verify clean worktree and local/`origin/main`/GitHub HEAD equality before ending. If a push fails, record it as pending.
