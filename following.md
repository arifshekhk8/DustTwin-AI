# Continue from here

Last updated: 1 October 2026, 11:40 Asia/Dhaka. Read with `AGENTS.md`, `plan.md` and `docs/decisions.md`; inspect the worktree and remote before editing.

## Current state

**P0, D1, D2, M1, M2, I1, S1, W1 and J1 software gates are complete.** The project is ready for the Round 1 software demonstration today. No further long training step is pending. The team still needs to practice its spoken pitch, check the venue projector and confirm any organizer updates. Hardware remains deferred until the team explicitly starts Round 2.

- Workspace: `/Users/arif/Documents/Techfest, IIT Bombay/DustTwin-AI`.
- Public repo: <https://github.com/arifshekhk8/DustTwin-AI>, branch `main`.
- Verified release: <https://github.com/arifshekhk8/DustTwin-AI/releases/tag/round1-demo-v1>.
- Release tag/source: `38e2b15149064efd6cf5e15fd593a1e8aa906412`.
- Archive: `output/releases/dusttwin-round1-demo-v1.zip`, 10,031,653 bytes, SHA-256 `ffd3a22dfc7cc833a1dbe2ba9b5cef214abc1eb07ffc9f9c0b7c0de8eab34a36`.
- Archive contains 188 file-hashed source/runtime/evidence assets plus its manifest. GitHub asset sizes/digests and an anonymous public download match local files. Final readiness reports/handover on main follow the frozen runtime tag; they do not alter the released model or demo.

## Open the demo

Double-click `Start DustTwin.command`: local live inference at <http://127.0.0.1:8000>. The launcher waits for readiness; keep its terminal open. Confirm **Local model ready**. Python 3.14.6 packages are installed in `.venv`; the built website is in ignored `apps/web/dist/`.

Double-click `Start Saved Replay.command`: labelled saved-only backup at <http://127.0.0.1:8001>. It uses the Python standard library and does not execute the model or rerun assumptions. Modern browser gzip-stream support is needed. Read `docs/offline-demo.md` for fresh setup and recovery. The archive contains a ready build and model, but no Python runtime/environment or raw training data.

Website: Overview, AI replay, Site experiment, Evidence & results, Round 2 design, Our team and Present. Printable packet: `output/pdf/dusttwin-judge-packet.pdf`. Full script: `docs/judge-script.md`. Five labelled screenshot backups are under `demo/backup/`. Primary and saved presentation servers are running in this session; they may need restarting in a later app session.

## Frozen data/model: preserve

- Askarov and Choi (2024), Mendeley V1, DOI `10.17632/7f22n9v7hp.1`, CC BY 4.0. Twelve lab OPC-N3 records / 53,717 raw rows; one setup. Outdoor records excluded. The 2020 candidate contained undocumented ten-minute averages and was rejected for raw short-horizon training.
- Causal latest-past one-second grid; keep last original duplicate row; maximum native observation age 1.5 s. A 120-second inclusive history has 121 snapshots. Forecast the latest observed PM10 snapshot at t+30. No episode clock/label or future activity features.
- Whole groups 1/2 train (24,818 windows), 3 validates/selects (12,113), 4 tests (15,065). Missing dates prevent strict global chronology. Group 4 is labelled temperature increased. Windows overlap and are correlated.
- Sixteen PM10 lag/statistic features; seven predefined candidates. Depth-3/100-iteration histogram boosting selected by validation MAE, trained only on groups 1/2. No test tuning/refit.
- Artifact: `models/artifacts/pm10-initial.joblib`, 54,679 bytes, SHA-256 `d78f1b37269f72af45933e01722968fb13ed82178f6d8b3e4c5584d46cec09c7`. Original artifact release `pm10-model-v1` remains available. Config/source/dependency hashes are part of loader/evaluation verification. Do not casually change preparation/model/training files and invalidate them.
- M4 total fit time for all seven models: 0.2133 s, excluding imports. Local CPU is sufficient; no GPU/Kaggle step remains.

## Honest results

Final test MAE/RMSE in ug/m3: model 88.405/179.272; persistence 95.702/199.384; trailing mean 81.565/200.713. Learned MAE is 7.62% below persistence but 8.39% above the mean. Ten-second-label record, abrupt rises and peaks are weaknesses. Model has 13/18 matched correlated threshold runs and 15 false alerts; mean 13/18 and 8 false alerts. Only one of three first onsets receives advance learned warning. A 30-second horizon is not guaranteed warning lead.

Simulation is distinct and uncalibrated: one common plant, four controllers, five cases. A north/B east/C south/D west; meteorological wind-from; preserved background; equal delay/minimum switching; causal synthetic proxy input. Endpoint-to-trajectory/spatial mapping and mist fraction are assumptions. Every metric is trace-derived. East case over 480 s: continuous 16.000 L / 86 s above setting, reactive 1.250 L / 122 s, predictive 1.842 L / 86 s. Continuous has lower mean concentration and greater water use; predictive uses more water than reactive in higher-risk cases. No physical suppression, field boundary accuracy or daily savings claim.

## Actual checks

- Twenty Python tests pass; all 51,996 prepared windows had provenance/causality verified earlier. Five model fixtures reproduce to 1e-8. Held-out metrics independently recomputed from all 15,065 exported rows.
- Simulation verifier passes all 20 runs / 9,600 intervals: water, concentrations/metrics, ambient floor, minimum switching, capacity, schema and hashes.
- Production TypeScript/Vite build and five browser journeys pass (last full run 8.4 s). Checks include fixture/API/display agreement, clock-only actual reveal, pause/reset/speed/seek, stale-response rejection, service-loss/recovery labels, diagonal A+B risk, dropout, custom flow for all strategies, saved/live equality, documents, all pages, presentation controls and 390-pixel layout.
- A real 600.002-second browser journey passed with every external request denied, zero external attempts/page errors. Physical Wi-Fi was not switched off; a human spoken pitch was not rehearsed. Final packaging/status-label changes have separate browser checks.
- All seven PDF pages rendered and visually inspected. Native vector plot uses unchanged target-aligned exported rows. No clipping/overlap. PDF files are explicitly binary in Git; their cross-reference whitespace must not be edited as prose.
- Fresh Python 3.14.6 environment installed exact service packages, passed dependency checks and reproduced five fixtures. The freshly unpacked archive passed 188 file hashes, live/saved startup, forecast/simulation agreement and seven document downloads per mode, with external browser requests denied. Only this M4/macOS live platform is verified.
- During packaging, a notice file had been trimmed after the static build, creating a harmless text-hash mismatch. Rebuilt/repacked and verified the final archive. The packager now rejects any stale demo/report file before freezing a clean source snapshot. Screenshot file-URL spaces were decoded after recovering the original captured files unchanged.
- Reports: `reports/readiness/checks.json`, `fresh-environment.json`, `offline-rehearsal.json`, `bundle-check.json`, `release-check.json`.

## Team and economics

CTRL_V / Theme 2: Md. Arif Shekh; Din Muhammad Rezwoan; Md. Meherab Hossain Talukder; Sowad Hossain. Team ID not issued according to the user. Contacts, member roles, qualification and judge feedback are not supplied/invented. `configs/team.json` is authoritative.

Dated indicative five-monitor component listing subtotal: USD 369.00 plus BDT 3440.28, kept as separate currencies. Not formal quotes or complete installed cost. Unpriced protection/nozzles/reference calibration/installation remain visible. Candidate sensor is out of stock and differs from OPC-N3 in range/cadence; valves also out of stock. Pump specifications conflict. The physical design cannot be approved from these listings. See `configs/feasibility.json`, `docs/feasibility.md` and D012.

## Exact next action / daily continuation

No unfinished Round 1 software milestone remains. First inspect the working tree and remote, then verify the existing release/launch on the presentation laptop. If there is no actual reproducibility, integration or usability issue, stay quiet and do not generate cosmetic or empty commits. Preserve the frozen release. Team action: practice `docs/judge-script.md` for ten minutes, check the projector and supply real organizer changes/feedback if any.

The user-authorized ACTIVE heartbeat `continue-dusttwin-daily` runs at 09:00 Asia/Dhaka in this chat. The computer/app must be on. Do not pause it without the user's request. After the event, record qualification/feedback only when the team supplies it. New model research needs an untouched evaluation dataset/site; hardware needs an explicit team instruction.

For a necessary fix: use the original implementation here, preserve concurrent changes, verify proportionately, commit/push coherent work with the configured Git author and no AI-contribution trailers, and update this handover. Do not copy the unlicensed reference source or manufacture metrics/activity. Rebuild static evidence before creating another archive. Optional PDF rebuilding uses `requirements-packet.txt`; serving/inference does not require those PDF packages.

## Git checkpoint

Implementation commits in this follow-up include I1 `03ced1e`, S1 `f3d7024`, W1 `d4ff437`, judge materials `206403b`, binary/notices `0c0efb0` and final archive guard `38e2b15`; all pushed. The runtime release/tag is verified at `38e2b15`. Commit/push this final readiness checkpoint and confirm local HEAD, origin/main and GitHub main match with a clean worktree. Read its resulting hash from Git next session; it cannot be embedded in its own file. Raw/processed data, `.venv`, verification temp files, built dist and release archives remain ignored.
