# DustTwin AI

DustTwin is a software prototype for forecasting construction dust and demonstrating how an urban construction site could select misting zones before dust reaches its perimeter.

For InnovateX Round 1, the project will combine a trained particulate-matter forecasting model, replay of recorded data, an interactive site simulation and traceable strategy comparisons. Physical sensors and misting hardware belong to Round 2.

## Current status

Planning and dataset reconnaissance are complete. Training, inference services and the website implementation have not started in this repository. Dataset pages have been checked; downloadable files and model suitability still need an audit.

## Start here

- [plan.md](plan.md): scope, milestones, deliverables and acceptance criteria.
- [following.md](following.md): current state and the exact next actions.
- [AGENTS.md](AGENTS.md): instructions for future work sessions.
- [Dataset shortlist](docs/dataset-shortlist.md): primary sources and suitability checks.
- [Evaluation protocol](docs/evaluation.md): proposed forecast task and evaluation gates, to freeze after the raw-data audit.
- [Architecture](docs/architecture.md): model, API, replay and site-control boundaries.
- [Round 1 checklist](docs/round1-checklist.md): presentation readiness.

## Reference frontend

The existing [meherabmehu/DustTwin](https://github.com/meherabmehu/DustTwin) frontend was reviewed at `dbb7386e384827fbae7e4571357d2491f4103fdf`. This new repository starts with original project planning documents. Before importing that frontend, record permission to reuse its code or implement the required interface here using our own code. The source repository currently exposes no license.

## Work and history

Work will be recorded in small, meaningful commits using the configured Git author, with a push after each completed milestone. Each session updates `following.md` with results, validation, unresolved issues and the next task. Daily continuation is active at 09:00 Asia/Dhaka in the current Codex chat. The local computer and app must be running; setup details are recorded in `following.md`.
