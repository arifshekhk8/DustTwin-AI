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

## D008 — Accept the newer raw laboratory task

Date: 1 October 2026. Status: accepted following file audit; supersedes D003's primary candidate and D007's pending selection. Use `10.17632/7f22n9v7hp.1`, raw `PM10(ug/m3)` from OPC-N3. Twelve laboratory recordings contain 53,717 rows. Exclude rolling-mean columns, analysed workbooks, other instruments and outdoor recordings from the initial task.

Freeze a 30-second latest-observed PM10 snapshot forecast with a 120-second inclusive lookback, causal one-second gridding and a maximum observation age of 1.5 seconds. Do not give learned models the event clock or drilling label. Put all recordings from groups 1/2 in training, group 3 in validation and group 4 in final test. This retains entire related experimental groups and does not claim a strict calendar ordering where dates are missing or overlap between groups.

The task is a preliminary laboratory monitor forecast, with one instrument/setup and a changed-condition final group. It does not establish outdoor boundary prediction or physical containment effectiveness. Configuration and audit evidence are in `configs/forecast-task.json` and `docs/dataset-audit.md`. D2 must implement and verify these rules before training begins.

## D009 — Freeze first fit and descriptive warning rules

Date: 1 October 2026. Status: accepted after D2 verification, before any learned model fit. Use sixteen PM10-only lag/statistic features, the seven previously planned ridge/tree candidates and the unchanged group split. Freeze full settings in `configs/training.json`. Fit scaling on training only, disable random early stopping, cap native threads at four and clip negative learned predictions to zero consistently. Choose using validation MAE, then RMSE, then simpler candidate order; keep the artifact trained on groups 1/2 only.

Freeze the illustrative warning experiment in `configs/demo-events.json` before final testing: 500 µg/m³ demo setting, five consecutive available snapshots, 60-second cooldown, one-to-one warning matches within the next 30 seconds. This is descriptive, not a health/regulatory threshold or a calibrated event-probability claim. Exact ETA still needs an explicitly predicted trajectory. Pin model dependencies in `requirements-model.txt`.

## D010 — Preserve the mixed held-out result

Date: 1 October 2026. Status: accepted after M2 evaluation of the artifact selected on validation. The trained model has test MAE 88.405 and RMSE 179.272 µg/m³. Persistence has 95.702/199.384; trailing mean has 81.565/200.713. Learned MAE improves on persistence by 7.62% but is worse than trailing mean by 8.39%; the ten-second-label recording is a material failure. Preserve the selected artifact, baseline comparison and negative evidence; do not retune against this test group.

The predeclared warning experiment yields 13 matched threshold runs and 15 false alerts for the model, versus 13 matches and 8 false alerts for trailing mean. The 18 runs are correlated crossings in only three test recordings. Only one of the three first onsets receives a valid advance learned warning. Integrate the learned forecast as an identifiable demonstration with baseline options, not as a proven field warning/control system. Keep site-control outcomes separate and simulated. Full evidence is in `reports/evaluation/` and `models/model-card.md`.

## D011 — Finish the remaining software today and record the team

Date: 1 October 2026. Status: directly requested by the user. Complete I1, S1, W1 and the software/offline presentation package today, proceeding through verification gates. This replaces the earlier 2 October implementation window; the deadline does not authorize invented evidence or hardware.

The user supplied team name CTRL_V and four members: Md. Arif Shekh, Din Muhammad Rezwoan, Md. Meherab Hossain Talukder and Sowad Hossain. Organizers have not supplied a Team ID; show that status, not a fabricated ID. Contact details and qualification/feedback are not supplied. Store exact approved display details in `configs/team.json`.

## D012 — Round 1 cost evidence and recovery scope

Date: 1 October 2026. Status: implemented within the authorized software scope. Use dated, cited public component listings as an indicative Round 1 worksheet, with stock/specification gaps and unpriced costs visible. Formal supplier quotes and a pressure/range-appropriate physical design remain Round 2 dependencies. Neither a partial subtotal nor simulated eight-minute consumption is a complete installed cost or field saving. The lower-cost candidate monitor differs from training OPC-N3; range and response prevent direct interchangeability.

The original website executes the frozen artifact through the local Python service; the standalone offline backup is explicitly saved inference and cannot rerun assumptions. A real ten-minute automated journey denied external browser requests and passed; physical Wi-Fi and the human spoken pitch were not tested. Record fresh-environment, archive and release checks separately.
