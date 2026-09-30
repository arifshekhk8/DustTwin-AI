# Working on DustTwin

## Start every session

1. Work in this repository, not the sibling reference checkout.
2. Read `following.md`, `plan.md`, `docs/decisions.md` and the document for the next milestone.
3. Inspect the worktree, recent commits and remote state before editing. Preserve unrelated or concurrent changes. Never reset or force-push to erase them.
4. Advance the first incomplete milestone whose prerequisites are satisfied. Update the plan explicitly when evidence changes a decision.

## Scope and evidence

Round 1 is a software prototype: measured-data forecasting, a website and a separately identified site-control simulation. Do not build or purchase hardware. Hardware starts only after the team explicitly authorizes Round 2 work.

Audit downloaded data before training. Keep original files, processed bulk data and large artifacts outside ordinary Git; commit provenance, terms, hashes and repeatable acquisition instructions. Do not commit credentials, private registration documents or invented team details.

Use causal features and chronological splits. Fit preprocessing only on training data. Select the model on validation data and retain the final test for evaluation. Report all baseline results honestly, including when the learned model is weaker. Do not claim boundary accuracy from near-source data or sub-minute forecasts from hourly measurements.

Use a single validated prediction path and a common simulation environment for all control strategies. Derive numbers from traces. Separate observed concentrations, model outputs and simulated control outcomes throughout reports and the website.

The reviewed `meherabmehu/DustTwin` source has no recorded reuse license. Use it as a reference; implement our own interface unless permission or a suitable license is recorded. This permits implementation to proceed without waiting for an import.

## Verification and Git

Verify each change in proportion to its remaining risk. For model/integration milestones, check leakage, artifact reload, API/browser agreement and water accounting as specified in the plan. For planning edits, check consistency, document links and whitespace. Record actual commands and outcomes; do not report an unrun check as passing.

Use the configured Git author. Commit each coherent verified milestone with a natural, specific message and push it. Do not add AI-contribution tags or authorship trailers. Do not create empty commits, backdate commits, inflate activity or claim work happened when it did not.

After each session update `following.md` with completed work, evidence, decisions, unresolved issues and the exact next action. Commit and push that checkpoint. Confirm local HEAD matches GitHub; if a push fails, retain the commit and record it as pending.

## Daily continuation

The daily session continues this same plan. Read the handover first, perform the next useful work package, verify it and publish meaningful progress. If a dataset or service is unavailable, record evidence and advance independent authorized tasks where possible. If a decision needs team input, identify it clearly without inventing an answer.

After the presentation, continue reproducibility and software quality work within the agreed scope. Do not infer qualification or judge feedback. When all software gates pass and no useful authorized work remains, report readiness and avoid repeated cosmetic changes or empty commits.
