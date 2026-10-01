"""Fetch the pinned public model release; verify before atomic installation."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
URL = "https://github.com/arifshekhk8/DustTwin-AI/releases/download/pm10-model-v1/pm10-initial.joblib"


def verified(path: Path, metadata: dict) -> bool:
    return path.is_file() and path.stat().st_size == metadata["artifact_bytes"] and hashlib.sha256(path.read_bytes()).hexdigest() == metadata["artifact_sha256"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional verification destination; default is the model metadata path")
    args = parser.parse_args()
    metadata = json.loads((ROOT / "models/model-metadata.json").read_text())
    destination = args.output if args.output else ROOT / metadata["artifact_file"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    if verified(destination, metadata):
        print("Cached model matches the pinned release checksum.")
        return
    with tempfile.TemporaryDirectory(dir=destination.parent) as directory:
        temporary = Path(directory) / "download.joblib"
        subprocess.run(["curl", "--fail", "--location", "--retry", "2", "--max-time", "120", "--silent", "--show-error", "--output", str(temporary), URL], check=True)
        if not verified(temporary, metadata):
            raise ValueError("Release size/checksum differs; existing artifact was preserved")
        temporary.replace(destination)
    print(f"Verified {metadata['model_id']}: {metadata['artifact_bytes']} bytes, SHA-256 {metadata['artifact_sha256']}")


if __name__ == "__main__":
    main()
