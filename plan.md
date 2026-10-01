# DustTwin project plan

Version 1.3. Created and updated 1 October 2026. All work dates use Asia/Dhaka.

## Objective and scope

Build a trained construction-dust forecasting model, evaluate it on unseen recorded observations, connect it to a working website and demonstrate proposed misting control in a software prototype. The judge should see what information the model received, what it predicted, what occurred later and why a zone was selected.

Round 1 uses recorded data and simulation only. Physical sensors, pumps, relays and a fabricated site model are deferred to Round 2. The supplied event information lists the Bangladesh zonal on 3 October 2026; use the registered team's latest organizer instructions if they change this date.

The desired final system predicts dust at construction-site boundaries. Available preliminary construction measurements may be near the source rather than at site boundaries. We will distinguish a learned sensor forecast from a simulated spatial/control response until boundary measurements support a stronger claim.

## Fixed technical starting point

- Primary pollutant: PM10. PM2.5 is an additional measured input or target only if the selected data actually contains it.
- First construction forecast target: latest-observed raw OPC-N3 PM10 snapshot 30 seconds ahead from the preceding 120 seconds, on a causal one-second elapsed grid. See the frozen `configs/forecast-task.json` for freshness and endpoint rules.
- First baselines: persistence and a causal trailing-average forecast.
- First learned models: regularized linear regression and one small tree ensemble using causal lag features. Choose the deployed model on validation data before inspecting final test results.
- Accepted first dataset: the 2024 Mendeley raw laboratory construction profiles, DOI `10.17632/7f22n9v7hp.1`. Twelve OPC-N3 recordings contain 53,717 rows. Use whole labelled experiment groups for train/validation/test as documented in the audit. The original 2020 candidate was rejected for this task because its released workbook contains ten-minute moving averages.
- Frontend: React/TypeScript, retaining the reviewed dashboard's useful interactions through an authorized import or an original implementation.
- Training and inference: Python, a reproducible training command and a local inference service. Freeze dependency versions when implementation begins.
- No paid training service is needed for the initial tabular models. Training is intended to run locally.

The accepted task demonstrates a laboratory monitor forecast. Missing calendar dates and repeated experimental conditions prevent claims of strict global chronology or cross-site reliability. If preparation exposes another suitability problem, change the task in an explicit decision record before training. Do not upsample hourly data and treat it as sub-minute measurements. The larger UCI Beijing dataset can support a separate hourly ambient benchmark, not evidence of construction-boundary performance.

## Milestones and gates

| ID | Work | Deliverables | Completion gate |
|---|---|---|---|
| P0 | Establish project and work history | Public repository, this plan, continuation notes, daily workflow | Documents pushed; daily continuation confirmed |
| D1 | Audit candidate data | Download manifest, hashes, schema, cadence/gaps, plots, coverage and decision | Raw construction files are usable; smoothing and sensor saturation are understood; target and horizon recorded |
| D2 | Freeze preparation and splits | Causal preprocessing, feature schema, split manifest, baseline predictions | No future data in inputs; no overlapping train/test target periods; units and missing values documented |
| M1 | Train candidate models | Reproducible scripts, fitted artifact, validation comparisons | Saved artifact loads and reproduces predictions; model choice is based on validation only |
| M2 | Evaluate once on held-out data | Metrics, forecast traces, event results, model card | All baselines included; scope and weaknesses reported; final test not used for tuning |
| I1 | Connect inference and replay | Validated API, replay timeline, model/source/version cards | Website shows predictions from the saved trained artifact; input snapshot and returned forecast can be inspected |
| S1 | Repair site simulation and control | Common plant model, four controllers, trace-based metrics | Equal environment/nozzle assumptions; meaningful threshold ETA; ambient floor preserved; realistic switching constraints |
| W1 | Complete the website | Problem, architecture, replay, simulation, results, team, proposed hardware | No fixed result claims; labels distinguish observations, predictions and simulation; build and key interactions pass |
| J1 | Prepare judge demonstration | Ten-minute story, offline demo, evidence packet, feasibility estimate | Full rehearsal works without external network; actual team details inserted; presentation matches implemented scope |

D1–M2 precede claims of model accuracy. I1 may be scaffolded after the API contract is frozen, but a model placeholder must remain labelled. S1 and W1 must use the final traces and saved artifact before the demo is considered integrated.

**Actual completion, 1 October:** P0, D1, D2, M1 and M2 pass their gates. The trained model is frozen; final MAE is 88.405 µg/m³ versus persistence 95.702 and trailing mean 81.565. Warning performance has material false alerts and first-onset misses. This mixed result is preserved in [the model card](models/model-card.md). I1, S1 and W1 pass their integration gates. J1 passes its software gate: documents, seven-page PDF, sourced cost basis, 600-second offline software rehearsal, fresh environment/unpacked archive checks and verified tagged release `round1-demo-v1` are complete. Human spoken rehearsal remains for the team.

## Schedule before the first round

These are planned completion windows, not guarantees. Advance by milestone gates and update `following.md` after every session.

### 1 October

1. Completed: publish P0 planning and configure the 09:00 daily continuation.
2. Completed in the first implementation session: audit/reject the 2020 processed file, acquire/audit the 2024 replacement and accept a raw laboratory PM10 task. The candidate troubleshooting limit remains two focused hours before recording a decision.
3. Completed in the first scheduled run: causal preparation, whole-group partitions and two baselines; all 51,996 prepared windows pass provenance/causality checks.
4. Completed: seven-candidate training, selected artifact/reload and final held-out evaluation. Small CPU fits on M4 took 0.2133 seconds total, excluding imports. Mixed baseline/warning results are documented without test tuning.

### Remaining work on 1 October / user deadline

5. Completed today: validated inference, six measured replay recordings, four common controllers and five frozen scenarios.
6. Completed today: original seven-page website, live/saved fallback, mobile layout and browser/API/fixture checks.
7. Completed today: sourced indicative costs, ten-minute story, seven-page PDF and actual 600-second offline software journey.
8. Completed final packaging: verified all 188 unpacked files, fresh live/saved startup and published the checked `round1-demo-v1` release. Hardware remains deferred; formal quotes and the human spoken pitch are not manufactured.

### 2 October

All software work is being completed on 1 October under D011. Check the frozen release on the presentation laptop, practice the spoken pitch with the team and fix only an actual reproducibility/usability problem. Daily continuation should stay quiet if there is no meaningful authorized task.

### 3 October

Run the local demo and presentation checklist before the event. Preserve the working demo release; make only necessary fixes with verification. After the event, record the team's actual feedback and qualification status before scheduling a hardware phase.

Daily continuation handles the next complete work package and updates the handoff. Additional sessions can advance the same queue. A scheduled run alone does not guarantee that all work fits before the event; the saved next task makes manual continuation straightforward.

## Dataset decision rules

Read [docs/dataset-shortlist.md](docs/dataset-shortlist.md) and [the completed first audit](docs/dataset-audit.md). Publish an audit before accepting any additional dataset.

1. Verify actual accessible files and reuse terms. Keep raw files outside Git; commit source/version information, hashes and reproducible download instructions.
2. Confirm timestamps or elapsed-time order, cadence, units, pollutant channels, sensor identities, experimental episodes and preprocessing. Do not infer missing wind measurements or sensor locations.
3. Use raw or demonstrably causal measurements. A centered or unexplained moving average can leak future information; reject it for forecasting claims or label it a descriptive dataset.
4. Split every simultaneous sensor by the same experiment timeline. A different sensor in the same experiment is not automatically an independent event.
5. A single 40-minute experiment permits a preliminary demonstration, not claims of cross-site, multi-weather or citywide reliability. If independent episodes exist, reserve whole episodes for evaluation.
6. If primary data is inaccessible or unsuitable, record why. Train on an appropriate measured alternative at its native horizon and identify that narrower task in the website. Keep construction-boundary control labelled simulated. The domain gap remains a limitation, not a solved result.

## What proves the model is working

Follow [docs/evaluation.md](docs/evaluation.md). Report MAE, RMSE and performance relative to persistence on the same samples. Include time-series plots, sample/episode counts, missing-data handling, prediction horizons and failures. Assess threshold-event recall, false alerts and warning timing only when enough events exist, with thresholds identified as demo settings.

A learned model may fail to beat persistence. Report that result and demonstrate the trained artifact honestly. Do not replace measured evaluation with attractive simulated percentages or retrain against the test set to improve the story. The chosen learned model and the operational baseline are separate, identifiable options.

## Integration and simulation boundaries

The trained model forecasts the monitored signal supported by its dataset. The spatial/control engine uses an explicit site layout, scenario wind, modeled transport and actuator assumptions. If training data lacks wind or boundary locations, those are simulation inputs, not learned features or field-validated outputs.

Measured replay initially shows real PM history, model forecasts and subsequently revealed recorded measurements. Site-control replay is a separate identified scenario. If a recorded near-source forecast is mapped to a site source-load proxy, the mapping and units must be shown as assumptions. Point concentration is not an emission rate; do not silently equate the two.

The four strategies share the same source event, weather timeline, observation noise/dropouts, nozzle effectiveness, initial state and pump limits. Only control information and decisions differ. Compute litres from flow times active time. Report concentration/exposure and water separately, with relay switching and missed boundaries where appropriate. Calculate ETA by forward prediction; show current exceedance and no expected crossing explicitly.

## Website fixes from the review

- Replace illustrative Results-page values with saved evaluation and simulation outputs.
- Preserve the measured background when suppressing the construction contribution.
- Include every relevant boundary risk, or disclose an actual capacity constraint that requires prioritization.
- Give predictive release/reactivation forecast awareness and both controllers minimum switching intervals.
- Make one prediction adapter own inference. The page must consume its returned prediction, not recompute a separate mock result.
- Distinguish low-risk, direction changes, diagonal exposure, high dust and unavailable-data behavior.
- Use one zone convention across the map, controller and proposed circuit. Mark a threshold-only circuit as such if it remains separate.
- Describe hardware imagery as proposed Round 2 design. Describe observed model limitations precisely.
- Display the actual registered team, at most four members, plus Team ID and Theme 2. Obtain accurate contact details from the team rather than inventing them.

## Round 2 direction

After recorded qualification/feedback, plan a controlled physical pilot: calibrate PM sensors and flow, use wind measurements, log independent events, compare forecast and control behavior, investigate humidity effects and distinguish background from site contribution. Hardware building is deferred until the team explicitly starts that phase. The software work can meanwhile improve data audits, robustness and deployment documentation.

## Work history and continuity

Commit and push each coherent verified milestone using a specific, natural message. Keep commits small enough to review, while including necessary related changes. Do not create empty commits, backdate work or split unrelated fragments just to increase the count. Do not add AI-contribution trailers or tags to commit messages.

At session start read `AGENTS.md`, `following.md`, this plan and recent Git history. Check the worktree and remote before editing. At session end record completed tasks, evidence, paths, decisions, remaining problems and the exact next command/task in `following.md`; commit and push that update. Verify remote/local HEAD equality. If GitHub is temporarily unavailable, retain commits and record that pushes are pending.

## Planning completion criteria

- Public repository exists under `arifshekhk8/DustTwin-AI`.
- Plan, dataset shortlist, evaluation protocol, architecture and presentation gates are concrete and cross-linked.
- `following.md` records the next action and actual implementation status.
- `AGENTS.md` makes the continuation instructions discoverable.
- Multiple meaningful planning commits are pushed and verified.
- Daily continuation is active at 09:00 Asia/Dhaka, with its result recorded.

References and dataset facts are documented in the linked shortlist. Actual model results are in `reports/training/`, `reports/evaluation/` and `models/model-card.md`. Simulated control metrics are published in `reports/simulation/` and remain separate from measured forecasting errors.
