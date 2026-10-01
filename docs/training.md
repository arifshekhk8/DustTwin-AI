# Initial training run

Protocol frozen before fitting, 1 October 2026 (Asia/Dhaka). This document will link the actual run once complete.

Use [training.json](../configs/training.json) and [features.json](../configs/features.json) without additional searches. Fit three StandardScaler → Ridge pipelines (alpha 0.1, 1, 10), and four histogram gradient-boosting regressors (depth 2/3 × 50/100 iterations). All use the same sixteen causal features and unchanged group split. No event clock, duration labels, PM rolling means or test labels enter fitting/selection. Equal window weighting makes longer recordings contribute more samples; overlapping windows remain dependent.

Fit the scaler using training only. Disable the tree model's automatic early stopping: its default can use an internal validation split with more than 10,000 samples ([official API](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html)). Fix all parameters, seed and a four-thread maximum in the configuration. Save estimator parameters actually used, dependency versions, host information, training commit and wall-clock fit times. Timings are observed on this Mac, not a promise for other machines.

Clip negative learned predictions to zero consistently during selection, evaluation and inference; report how many were clipped. No upper clipping. Select by pooled validation MAE, then RMSE, then candidate order. Preserve both baseline results even if better. Do not refit with validation or test. The selected learned artifact remains separately identifiable from a stronger operational baseline if it loses.

Save the fitted pipeline/estimator under ignored `models/artifacts/`, plus public metadata, hashes and a fixed validation fixture. Reload in a fresh process and compare the fixture. Load only the locally generated, hash-verified artifact; serialized Python model files require a trusted source and matching library versions ([official persistence guidance](https://scikit-learn.org/stable/model_persistence.html)). `requirements-model.txt` pins this environment.

Before inspecting test performance, [demo-events.json](../configs/demo-events.json) freezes an illustrative 500 µg/m³ operating threshold, five-snapshot persistence, 60-second cooldown and 30-second warning matching. This is not a regulatory limit. Report descriptive event counts and failed warnings with the limited recording count. An endpoint prediction cannot give an exact crossing ETA.
