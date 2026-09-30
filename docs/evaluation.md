# Forecast and control evaluation protocol

Status: protocol proposed before file audit and training. Change dataset-dependent choices through a decision record, before final testing.

## First measured-data task

Given the previous 120 seconds of recorded PM10, predict PM10 30 seconds later at the same monitor. Use measured PM2.5 or weather only if actually available at prediction time. Select an eligible unsaturated OPC monitor by a documented deterministic rule during the audit; do not choose a monitor using final test performance. Keep single-monitor forecasting as the first deliverable.

For true two-second sampling, a history contains 60 sampling intervals and the target is 15 intervals ahead. Verify endpoint inclusion explicitly in code. Do not bridge gaps by silently treating irregular records as evenly spaced. Work with elapsed seconds where civil timestamps/timezone are absent, and retain this clock type in exports.

## Data preparation and separation

1. Preserve original observations and file hashes. Record every filter, rejected row and conversion.
2. Sort by experiment, sensor and time; resolve duplicates deterministically. Derive inputs only from observations at or before forecast issue time.
3. Reserve the earliest 60% of an experiment timeline for training, the next 20% for validation and the final 20% for test. Apply the same boundaries to simultaneous sensors. For multiple independent experiments, prefer whole-experiment holdout and record that alternative before fitting.
4. Construct samples whose full history and target lie within their assigned partition. This conservatively removes windows overlapping partition boundaries. No training target or feature value may come from validation or test periods.
5. Fit preprocessing and normalization on training only. Avoid bidirectional interpolation, centered smoothing and backfilling from future values. Training-only fitted imputation or causal forward filling may be used when justified; score only targets actually observed.
6. Keep test labels inaccessible to model selection. If the last segment contains only one activity, report that regime limitation; do not repeatedly move split boundaries to find a favorable result.

The forty-minute candidate is one experiment. Many overlapping windows and co-located sensors do not create many independent construction events. Record both sample counts and independent episode counts.

## Baselines and model selection

- Persistence: `prediction(t + H) = observed PM10(t)`.
- Trailing mean: mean of observed PM10 over the preceding 60 seconds, with a fixed rule for available history.
- Learned baseline: ridge regression using causal lag values and trailing statistics, with alpha chosen from 0.1, 1 and 10.
- Candidate: one small gradient-boosted tree ensemble, initially depths 2/3 and 50/100 iterations. Disable any default random holdout that violates the chronological protocol. Freeze all other parameters, seed and dependency versions.

Features: recent PM10 lags, past-only mean/std/slope over 30/60/120 seconds and actual measured optional channels. Exclude future activity labels, retrospective event identity, total-future statistics and simulator hidden state. If pooling monitors later, preserve monitor identity and use the common timeline split.

Choose the learned model by validation MAE, then RMSE and simplicity. Retraining on combined train/validation is a documented later choice; keep the initial selection run and artifact reproducible. Evaluate the selected frozen artifact on test once. Do not force the learned model to win; persistence can be competitive.

## Outputs and reporting

Save `models/model-card.md`, feature/schema configuration, split manifest, training settings, model artifact hash and JSON metrics. Store test forecast traces with issue time, horizon, actual target time, observed value, each prediction and input-availability mask. Calculate MAE/RMSE on the same eligible target samples for every model. Report sample counts, error by activity where metadata supports it, PM range and limitations. Show actual-versus-forecast plots and residuals.

Report improvement over persistence as `100 * (MAE_persistence - MAE_model) / MAE_persistence` when the denominator is positive. This is forecast error improvement, not pollution reduction. Do not publish an accuracy percentage for regression without defining it.

Uncertainty intervals are optional before Round 1. If implemented, use a dedicated calibration partition and evaluate coverage; do not invent confidence values or style standard residual bands as calibrated probabilities. Training loss, feature importance and a trend explanation are not proof of an individual prediction's correctness.

## Event warnings

Use a named demo operating threshold chosen without test tuning. Define an event as a threshold crossing with a stated persistence duration and cooldown. Match warnings to events using a fixed forecast window. Report recall, precision/false alerts and first-warning lead time with event counts. If too few independent crossings exist, report descriptively rather than claiming stable event accuracy.

Show “already exceeded” for current exceedance, a finite ETA only for a predicted future crossing, and “no crossing within H” otherwise. A single endpoint forecast supports concentration at that endpoint; it does not determine exact within-horizon crossing time. Exact ETA requires an explicit predicted trajectory and must name its method.

## Separate control simulation experiment

Use one shared environment runner for no control, continuous, reactive and predictive control. Freeze geometry, event timeline, weather, sensor observation model, pump capacity, nozzle response and initial state. Give all controllers the same information availability and actuator timing constraints, except for the predictor available to predictive control.

Evaluate low risk, an eastward plume, diagonal exposure, a wind shift and a data-loss case. Save seeds/configs and generate all chart values from traces. Report mean/peak boundary PM, sampled exceedance duration, integrated exposure proxy, litres, zone duty and switching. Define whether aggregation is maximum across boundaries, mean across boundaries or per-boundary; use the same rule for all controllers.

For a one-second simulation, litres are the sum of each active interval's configured litres/minute multiplied by interval seconds/60. Keep ambient PM separate from the source contribution. Treat humidity effects, nozzle effectiveness and transport parameters as assumptions until calibrated. Simulated suppression values cannot establish causal effects in the recorded experiment, which contains no matched intervention trial.

## Required checks

- Feature timestamps and forecast targets enforce the selected horizon and partition boundaries.
- A gap/sensor change does not silently become a continuous training window.
- The saved artifact reloads and reproduces a small fixed prediction fixture.
- API and offline replay agree on the same input snapshot and artifact.
- No-control water is zero; pause freezes simulation time/water; flow and durations determine litres.
- Every controller uses the same environment assumptions; every threshold-risk boundary is handled or explicitly capacity-limited.
- Results-page numbers equal saved evaluation/experiment outputs and use consistent units.

Run focused tests for these risks when implementing. Documentation-only planning does not require placeholder implementation tests.
