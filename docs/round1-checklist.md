# Round 1 demonstration and readiness

This checklist is a delivery gate. Status updated from actual implementation/verification on 1 October 2026; supporting reports are in `reports/readiness/`. The supplied competition material describes a ten-minute presentation and a team limit of four. Confirm the registered team's current organizer instructions before the event.

## Ten-minute presentation

| Time | Show | Evidence required |
|---|---|---|
| 0:00–0:45 | Introduce CTRL_V and the software prototype | Round 1 scope, no physical hardware claim |
| 0:45–1:45 | Local problem, existing approaches and contribution | World Bank context; continuous/reactive comparison |
| 1:45–2:45 | Data, target and model | Actual source, monitor, horizon, group split and limits |
| 2:45–4:15 | Measured-data replay | Past inputs, trained forecast, both baselines and later actual |
| 4:15–5:15 | Held-out results | Mixed errors, false alerts and onset failures |
| 5:15–6:45 | Site-control replay | Wind convention, diagonal risk, commands and equal plant |
| 6:45–7:45 | Water/exposure tradeoff | Saved eight-minute metrics and clear simulation assumptions |
| 7:45–9:00 | Deployment, economics and pilot gates | Dated listing basis, quote gaps, calibration and hardware deferral |
| 9:00–10:00 | Summary and team | Completed software, four approved members and validation next step |

Do not let a slow demo consume the evidence section. Prepare a short saved replay of the same verified session for recovery.

## Model and data gates

- [x] Raw files acquired with source/version, reuse terms and hashes recorded.
- [x] Audit supports the selected pollutant, cadence, monitor and forecast horizon.
- [x] Causal preparation and whole-group partitions are frozen before training; within-record clocks are ordered, strict global chronology is not claimed (D008).
- [x] A saved learned artifact loads and reproduces the recorded predictions.
- [x] Held-out MAE and RMSE include persistence and trailing-average comparisons on identical samples.
- [x] Model card reports sample/episode counts, failures and the limits of a short experiment.
- [x] No model improvement is claimed unless the measurements support it; a weaker model result is disclosed.

## Website and simulation gates

- [x] One known input produces matching evaluation, API and browser predictions.
- [x] Measured observations, learned predictions and simulated outcomes have clear labels and units.
- [x] Replay only exposes observations as its clock advances; future targets are unavailable to controllers.
- [x] Reset reproduces the same trace; pause and speed controls preserve the time accounting.
- [x] No control, continuous, reactive and predictive strategies share source/weather events and actuator limits.
- [x] Water is integrated from active flow and time; concentrations and switching counts come from traces.
- [x] Background concentration is preserved when suppressing construction contribution.
- [x] Crossing displays distinguish already exceeded, future crossing and no crossing within the horizon.
- [x] Low risk, eastward travel, diagonal exposure, wind change and data loss are checked.
- [x] Results pages contain computed values and identify the scenario, time window and assumptions.
- [x] Physical diagrams and sensors are labelled as proposed Round 2 hardware.

## Proposed economics worksheet

Build `docs/feasibility.md` during implementation. Dated supplier listings support indicative Round 1 costs; obtain formal quotations before procurement (D012). the table below contains planning quantities, not a purchased bill of materials. Compare a minimal pilot with the eventual site configuration.

| Item | Initial quantity basis | Evidence to obtain |
|---|---|---|
| PM monitors | 3–5 proposed nodes; placement and reference needs decide final count | Measurement range, calibration, humidity response, quote |
| Wind measurement | One proposed site instrument, subject to siting assessment | Direction/speed accuracy and usable placement |
| Controller and connectivity | One hub plus node links as needed | Offline operation, power and communication assumptions |
| Misting zones | Four proposed directional zones | Nozzle flow, coverage, valve and pump capacity |
| Power, tubing, enclosure and installation | Sized for the pilot | Pump duty, protection and installation quote |
| Maintenance and calibration | Documented schedule | Cleaning, reference comparison, replacement and labour |

Estimate water as the sum of zone flow × active duration, with units shown. Estimate electrical energy from rated/verified power × duty time. Recurring cost includes water, energy and maintenance. Report estimated cost and uncertainty separately from measured demo results. Do not extrapolate an eight-minute simulation to a daily saving without a declared operating schedule.

## Event and offline readiness

- [x] Approved CTRL_V/Theme 2/four-member display details are inserted. Team ID is labelled not issued; unprovided contacts are omitted.
- [x] Local construction context and source citations are included.
- [x] The accepted model, permitted replay data, website and service are available on the presentation laptop.
- [x] Pinned Python packages installed in a clean local environment; five model fixture predictions and artifact checks passed. Unpacked release startup is the final packaging check.
- [x] The 600-second software journey passes with all external browser requests denied. Physical Wi-Fi is not switched off; human spoken rehearsal is separate.
- [x] A saved inference replay and screenshots/video are prepared as a labelled backup.
- [ ] Final archive/fresh-unpack check and tagged release published with actual artifact/data versions (in progress).
- [ ] Team practices spoken delivery and checks venue projection (team action).
- [ ] After the event, record actual judge feedback/qualification only when supplied; hardware requires an explicit team instruction.

## Go/no-go decision

An integrated AI demo requires the trained artifact, real held-out results and a working prediction path. If the data gate fails, present the simulation and the recorded limitation clearly; do not describe a heuristic or synthetic-data demonstration as a validated construction model. Freeze the best verified build before the event and record every incomplete gate in `following.md`.
