# DustTwin: ten-minute judge demonstration

CTRL_V / Theme 2. Members: Md. Arif Shekh; Din Muhammad Rezwoan; Md. Meherab Hossain Talukder; Sowad Hossain. Team ID: not issued by organizers according to the team. No roles/contact details are invented. This timing replaces the earlier draft allocation in the checklist and matches the website presentation.

## 0:00–0:45 / Introduce the prototype

“We are CTRL_V. DustTwin is our software prototype for construction-site dust forecasting and selective misting. Today we will show a trained model, its actual test results and a simulated control loop. Physical hardware is planned for Round 2.” Open Overview and show the proposed site illustration.

## 0:45–1:45 / Problem and contribution

“World Bank reporting identifies major construction with traffic among Dhaka's studied pollution settings. A site operator needs to decide where and when to spray while accounting for water. We compare continuous spraying, reactive thresholds and forecast-guided zone decisions.” The World Bank supports the local motivation, not this system's effectiveness. Identify the monitored source and four proposed boundaries; do not claim a citywide or health impact.

## 1:45–2:45 / Real data and task

“We audited the downloadable files before accepting the task. An earlier candidate contained undocumented ten-minute averages, so we rejected it for short-horizon forecasting. Our accepted Askarov/Choi 2024 CC BY data contains twelve laboratory OPC-N3 recordings. We use raw PM10, a causal one-second grid and 120 seconds of past readings to forecast a 30-second endpoint. Groups 1/2 train, group 3 selects and group 4 tests.” Disclose the single laboratory setup and changed-temperature test group. Thousands of overlapping windows are not independent experiments.

## 2:45–4:15 / Show AI working

Open AI replay, group 4 / 90-second drilling label. This label is context, not a learned feature. Show current observation, model endpoint and the two baselines. Play at 1× or 2× briefly, pause, and open the input/artifact detail. Explain that sixteen PM10 lag/statistic features enter a fitted boosting model. The API executes the saved artifact on the laptop; the browser displays its response.

Seek forward 30 seconds and inspect a matured forecast's earlier issue time, target time and recorded actual. It is revealed only when the clock reaches the target. No future observations go to the model. A single endpoint provides no exact crossing ETA or calibrated confidence. In saved-only fallback, explicitly say these predictions were computed earlier; AI is not executing in that browser mode.

## 4:15–5:15 / Honest held-out results

Open Evidence & results. “Model MAE is 88.405 µg/m³; persistence is 95.702 and trailing mean is 81.565 on the same 15,065 held-out windows. The model improves on persistence by 7.62% but loses to the mean on MAE. Its RMSE is lower than both. We preserved this result instead of retuning on test data.” Show per-recording failures and abrupt rises. “At the predeclared demo warning setting, only one of three first onsets gets an advance learned warning; false alerts remain material.” A 30-second horizon is not 30 seconds of reliable warning.

## 5:15–6:45 / Shared site experiment

Open Site experiment, “Two exposed boundaries,” seek 100 s and use Predictive. A north and B east should both be commanded. Wind from 225° travels toward 45°. Compare Reactive at the same clock, then the complete eight-minute table. Source proxy, transport, boundary response and mist effectiveness are explicitly synthetic assumptions. The learned endpoint is mapped through a stated, uncalibrated source path and transport rollout. Controllers see past observations only, with the same actuator delay and minimum on/off times.

If time allows, show East-to-north wind shift at 220 s and Sensor interruption at 110 s. The interruption label explains unavailable inputs and the common constrained fallback. Simulated truth displayed for inspection is not supplied to controllers during loss.

## 6:45–7:45 / Water and exposure tradeoff

“For the east case, continuous uses 16.000 L, reactive 1.250 L and predictive 1.842 L over the same eight minutes, at the assumed 0.5 L/min per active zone. Predictive has 86 seconds above the demo setting, reactive 122. Continuous has the lowest mean concentration and the greatest water use. Predictive uses more water than reactive in higher-risk cases.” All numbers derive from traces; they are not physical water savings. Explain maximum-boundary metrics, threshold choices and ambient preservation. Do not claim every metric improves.

## 7:45–9:00 / Deployment and economics

Open Round 2 design. “A proposed pilot combines source/boundary monitors, wind, acquisition nodes, a local inference hub and isolated valve commands with logging and manual override.” Show dated supplier listings: the five-monitor candidate subtotal is USD 369 plus BDT 3440.28, in separate currencies. It excludes unpriced parts, range-appropriate monitors, calibration and installation. Out-of-stock parts and inconsistent pump specifications are visible. This is a cost basis, not an approved or complete hardware build.

The candidate monitor differs from OPC-N3 and cannot capture all replay peaks at the trained cadence. Round 2 must establish suitable range/cadence, reference calibration, humidity/mist interference, actual nozzle flow/coverage, pressure, electrical protection and independent outdoor events. Compare measured water and exposure only after those gates. Do not promise payback or qualification.

## 9:00–10:00 / Close with evidence and team

“Our Round 1 delivery is working software: the frozen trained artifact, honest baselines, an inspectable replay, fair simulated strategies and an offline demonstration. We are asking for feedback on the pilot design and its validation. We have not built the physical hardware or established field effectiveness.” Show the four team members, available evidence packet and public repository. Leave time for the transition to questions.

## Questions to prepare for

- **Why not use the mean if it has lower MAE?** It is a credible baseline/operational option. The learned artifact is a preliminary experiment; its lower RMSE is not enough to claim universal superiority. A new model needs new untouched evaluation evidence.
- **Does it predict dust at a real boundary?** No. It forecasts the recorded laboratory monitor; spatial mapping/control is a separate illustrative simulation.
- **How much water will a real site save?** Unknown until flow/coverage and independent comparable site activities are measured. The eight-minute simulated litres are not a daily estimate.
- **Where is the hardware?** Round 1 is software. The architecture and cost dependencies are proposed for an explicitly authorized Round 2.
- **Why so many test windows but few events?** Windows overlap within three records from one setup; uncertainty and warning reliability cannot be inferred as though they were independent events.
- **What if internet/model service fails?** The live model works without internet after setup. The static backup is labelled saved inference and preserves the same predictions, plots and traces.

Practice the spoken story with the team and a real ten-minute timer. The automated software rehearsal checks application stability and offline recovery, not spoken delivery or projector readability at the venue.
