# Run and recover the Round 1 demo

## On this prepared Mac

Double-click `Start DustTwin.command` in the project folder. It starts the local model service and opens <http://127.0.0.1:8000>. Keep the terminal open; Control-C stops the server. No internet is required once dependencies, built website and the verified model are present. The health/status badge must say “Local model ready” for live inference.

For the saved-only backup, double-click `Start Saved Replay.command`. It serves the built website at <http://127.0.0.1:8001>, using Python's standard library. The page must say “Saved replay mode.” It displays previously computed model outputs and all scenario traces; it cannot execute the trained model or rerun changed assumptions. This is a labelled recovery mode, not a live AI claim.

## Another computer / fresh setup

Download the `round1-demo-v1` release archive and unzip it. The archive contains a ready-built website, attributed replay data, evidence/plots, PDF packet, source code/configuration and the frozen model binary, with a SHA-256 file manifest. It excludes bulk source data, installed environments, credentials and node_modules. Use modern Chromium, Chrome, Edge or Safari with gzip stream support.

Saved mode: run `python3 scripts/serve_static.py` from the unpacked folder; no package installation or Node is needed. On macOS the saved launcher opens the browser. Use the PDF packet and `demo/backup/` screenshots if a local browser server is unavailable.

For live inference, install **Python 3.14** once while internet is available:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-service.txt
.venv/bin/python scripts/verify_model.py
.venv/bin/python scripts/serve.py
```

The fitted model is included and verified against metadata; do not download it again unless absent. This release does not bundle Python or a portable virtual environment. Different Python/model dependency versions are not claimed to reproduce the live binary. The static fallback avoids that setup dependency.

For a source checkout, also build once with `cd apps/web && npm ci && npm run build`, after `.venv/bin/python scripts/build_public_data.py`. Node is a build dependency only. Source checks can recreate the model release via `scripts/download_model.py` without raw training data; full retraining needs the audited acquisition/preparation pipeline.

## Offline checks

With both servers running, `cd apps/web && npm run test:e2e` verifies live/saved agreement and main interactions. `node offline-rehearsal.mjs` runs a real ten-minute browser journey with every non-loopback request denied. It includes live replay, actual target reveal, honest results, diagonal control, wind shift, sensor loss, economics, team/presentation and saved recovery. The result, elapsed time and exact scope are published in `reports/readiness/`; physical Wi-Fi is not switched off by the check.

The archive manifest is verified after extraction to a fresh temporary folder; the unpacked saved server and complete local document downloads are checked in a browser. Dependency installation from a fresh virtual environment is a separate live portability gate. A team member must still rehearse the spoken pitch and check the projector at the venue. No such human rehearsal is claimed here.

Rebuild the printable packet, if needed, with the optional pinned `requirements-packet.txt` and `python scripts/build_judge_pdf.py`. Restage public documents and rebuild the website afterward. The distributed frontend notices are included locally in `demo/documents/third-party-notices.md`; retain them with copies.

## Before presenting

Connect power, open the live dashboard and PDF, check the ready badge and run a measured replay. Keep the saved launcher and extracted archive accessible. Close unnecessary laptop applications, confirm the projected page is readable, and use the nine timed presentation sections. Source links are optional; do not rely on them loading during the pitch.

Team ID has not been issued according to the team. Contact details, current organizer changes, qualification and judge feedback remain absent until supplied. Hardware requires an explicit team instruction after the event; the daily continuation should verify readiness or repair an actual problem, not create cosmetic/empty commits.
