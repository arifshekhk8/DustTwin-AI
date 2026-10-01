# Original website and browser checks

Implemented 1 October 2026 in `apps/web/` using React/TypeScript. This is an original interface, not an import of the unlicensed reference repository. Runtime assets, fonts, measured replays, scenario traces and evidence are local. Source links are optional external references.

## Run

```sh
.venv/bin/python scripts/build_public_data.py
cd apps/web
npm ci
npm run build
cd ../..
.venv/bin/python scripts/serve.py
```

Open <http://127.0.0.1:8000>. The built interface is served by the model API. For a saved-only backup, run `.venv/bin/python scripts/serve_static.py` and open <http://127.0.0.1:8001>. Neither serving mode requires Node after the website is built. Live inference needs the pinned Python model environment; saved replay needs only the Python standard library and a modern browser with gzip stream decompression.

## Contract and labels

- Measured replay consumes the API forecast, including artifact identity, baselines, exact inputs and sixteen features. It never fits or recomputes a different learned model in JavaScript. Future recorded actuals appear only at their target clock.
- Abort superseded replay requests; render only a snapshot matching the current episode and clock. Previously computed predictions are labelled `saved_inference` when the API is unavailable.
- Simulation consumes all four saved traces from one scenario. All strategies share the same clock; complete-window comparisons stay explicitly eight minutes while current litres are cumulative up to the selected clock. Changed assumptions rerun all four controllers through the API. Late custom responses cannot replace a newly selected case. The static fallback disables changing assumptions.
- Zone A north, B east, C south, D west, meteorological wind-from convention. Commands and delayed mist effects are separate. Controller-unavailable observations are labelled even though simulation truth remains visible for inspection.
- Honest held-out errors, false alerts, source attribution, proposed hardware, approved team details and a ten-minute presentation are included. No invented Team ID, member roles, contacts, confidence, exact measured-replay ETA or field savings.

## Verification

Run both local servers above, then `cd apps/web && npm run test:e2e`. Five browser checks cover the five fixture predictions to absolute tolerance 1e-8, shared API/display agreement, target reveal, speed/pause/reset/seek, deliberately delayed stale response, diagonal A+B commands, sensor loss, custom flow for every strategy, saved/live agreement, disabled fallback controls, all pages, local assets, presentation keys and 390-pixel mobile layout. External requests are denied in the fixture, static fallback and full-page journeys.

Production TypeScript/Vite build passes. Desktop and mobile screenshots were inspected; footer icon sizing was corrected after visual review. An initial saved/live assertion used a hardcoded replay time instead of the selected recording clock; the check now reads the actual clock and passes. No artifact or evaluation metric was altered. Twenty Python tests and the simulation trace verifier remain separate gates.

The automated browser checks do not verify a spoken team presentation, outdoor calibration or physical hardware. The offline package and timed software rehearsal are documented in `docs/offline-demo.md`.
