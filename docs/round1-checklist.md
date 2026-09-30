# Round 1 demonstration and readiness

This checklist is a delivery gate. No item below has been completed by writing this document. The supplied competition material describes a ten-minute presentation and a team limit of four. Confirm the registered team's current organizer instructions before the event.

## Ten-minute presentation

| Time | Show | Evidence required |
|---|---|---|
| 0:00–1:15 | Construction dust problem and a specific local context | Attributed local example; avoid unsupported health or citywide-impact claims |
| 1:15–2:00 | Current control approaches and the proposed contribution | Explain forecast-guided zone selection and the exposure/water tradeoff |
| 2:00–3:00 | Data, target and model | Actual source, monitor, horizon, split and limitations |
| 3:00–5:00 | Recorded-data replay | Past inputs, trained forecast, persistence and later actual readings; model/artifact identity visible |
| 5:00–6:30 | Site-control scenario | Wind convention, boundary selection, commands and common environment for all strategies |
| 6:30–7:30 | Results | Held-out model errors and separately labelled simulated water/exposure results |
| 7:30–8:30 | Deployment and economics | Proposed hardware architecture, cost basis, water/power assumptions and maintenance |
| 8:30–9:30 | Limitations and Round 2 validation | Dataset coverage, sensor calibration, mist/humidity effects and physical pilot plan |
| 9:30–10:00 | Summary and team | Completed software prototype, actual registered team and next validation step |

Do not let a slow demo consume the evidence section. Prepare a short saved replay of the same verified session for recovery.

## Model and data gates

- [ ] Raw files acquired with source/version, reuse terms and hashes recorded.
- [ ] Audit supports the selected pollutant, cadence, monitor and forecast horizon.
- [ ] Causal preparation and chronological partitions are frozen before training.
- [ ] A saved learned artifact loads and reproduces the recorded predictions.
- [ ] Held-out MAE and RMSE include persistence and trailing-average comparisons on identical samples.
- [ ] Model card reports sample/episode counts, failures and the limits of a short experiment.
- [ ] No model improvement is claimed unless the measurements support it; a weaker model result is disclosed.

## Website and simulation gates

- [ ] One known input produces matching evaluation, API and browser predictions.
- [ ] Measured observations, learned predictions and simulated outcomes have clear labels and units.
- [ ] Replay only exposes observations as its clock advances; future targets are unavailable to controllers.
- [ ] Reset reproduces the same trace; pause and speed controls preserve the time accounting.
- [ ] No control, continuous, reactive and predictive strategies share source/weather events and actuator limits.
- [ ] Water is integrated from active flow and time; concentrations and switching counts come from traces.
- [ ] Background concentration is preserved when suppressing construction contribution.
- [ ] Crossing displays distinguish already exceeded, future crossing and no crossing within the horizon.
- [ ] Low risk, eastward travel, diagonal exposure, wind change and data loss are checked.
- [ ] Results pages contain computed values and identify the scenario, time window and assumptions.
- [ ] Physical diagrams and sensors are labelled as proposed Round 2 hardware.

## Proposed economics worksheet

Build `docs/feasibility.md` during implementation. Obtain dated supplier quotations before filling prices; the table below contains planning quantities, not a purchased bill of materials. Compare a minimal pilot with the eventual site configuration.

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

- [ ] Team ID, Theme 2, actual member names (at most four) and approved contact details are supplied by the team.
- [ ] Local construction context and source citations are included.
- [ ] The accepted model, permitted replay data, website and service are available on the presentation laptop.
- [ ] Setup instructions work from a fresh environment with pinned dependencies and artifact checksums.
- [ ] The complete ten-minute rehearsal works with the external network disconnected.
- [ ] A saved inference replay and screenshots/video are prepared as a labelled backup.
- [ ] A working demo version is tagged with the actual artifact and data versions.
- [ ] After the event, actual judge feedback and qualification status are recorded before starting hardware work.

## Go/no-go decision

An integrated AI demo requires the trained artifact, real held-out results and a working prediction path. If the data gate fails, present the simulation and the recorded limitation clearly; do not describe a heuristic or synthetic-data demonstration as a validated construction model. Freeze the best verified build before the event and record every incomplete gate in `following.md`.
