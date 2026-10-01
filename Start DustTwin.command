#!/bin/zsh
set -e
cd "$(dirname "$0")"
if [[ ! -x .venv/bin/python ]]; then
  print "Live setup is missing. Follow docs/offline-demo.md, or open Start Saved Replay.command."
  read "task_reply?Press Return to close. "
  exit 1
fi
exec .venv/bin/python scripts/launch_demo.py
