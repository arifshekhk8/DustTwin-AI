"""Start the offline-capable website and model on one local origin."""

import argparse
from pathlib import Path
import sys

import uvicorn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services/inference"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run("app:app", host="127.0.0.1", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
