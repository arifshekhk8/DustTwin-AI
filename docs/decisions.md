# Project decisions

Created 1 October 2026. Add dated decisions here when evidence changes the task; keep prior reasons visible.

## D001 — Round 1 software scope

Status: accepted by the user. Build a real trained model, fix/integrate the website and demonstrate the prototype in software. Hardware is deferred to Round 2 and requires the team's instruction to start that phase.

## D002 — New public repository

Status: accepted by the user. Work in `arifshekhk8/DustTwin-AI`, with meaningful commits and pushes after milestones. Use natural commit messages and no AI-contribution tags. The original repository is a reference; it is not the new remote.

## D003 — Preliminary data and model choices

Status: proposed, dependent on D1 audit. Audit the 2020 Mendeley raw construction dataset first. Prefer measured PM10 at an audited monitor; attempt a 30-second horizon with a 120-second lookback only if cadence and file quality support it. Compare regularized linear regression and a small tree ensemble against persistence and a causal trailing mean.

Neither a dataset nor a model has been accepted yet. Native-hourly ambient forecasting is a possible separately labelled fallback; it does not establish the construction task. Record exact sensor, target, cadence, horizon, preprocessing and independent episode count after the audit.

## D004 — Separate measured forecasting and site control

Status: accepted planning design. A recorded monitor forecast demonstrates learned inference. Site transport, wind, actuator response and containment are explicit simulation assumptions unless the accepted measurements support them. Evaluate controllers in one shared environment without access to hidden future events.

## D005 — Frontend reuse

Status: accepted implementation route. No reuse license was visible in the reviewed source. Start an original React/TypeScript interface unless source permission or a license is documented. Do not treat public visibility as permission to copy source.

## D006 — Daily work

Status: authorized by the user. Configure daily continuation at 09:00 Asia/Dhaka in the current chat. Each run reads the handover, advances the next milestone, verifies changes and commits/pushes actual progress. Scheduling setup and the automation ID belong in `following.md`.

## D007 — Reject the released 2020 file for raw short-horizon training

Date: 1 October 2026. Status: accepted from downloaded-file evidence. The checksum-verified workbook contains PM10 ten-minute moving averages, not the advertised raw PM10/PM2.5/PM1 channels. Smoothing alignment is undocumented. It cannot support the proposed 30-second raw concentration task or establish causality of the input windows.

Retain this file as descriptive, processed construction data. Do not train on it and claim raw short-horizon accuracy. Inspect the newer 2024 construction/outdoor dataset before choosing an ambient fallback. The forecast horizon and monitor remain unfrozen until a suitable measured task passes the audit. See `docs/dataset-audit.md` and `reports/data-audit/mendeley-2020-summary.json`.
