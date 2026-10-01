"""Verify every manifest file in an already unpacked judge bundle."""

import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    root = args.directory.resolve()
    manifest = json.loads((root / "bundle-manifest.json").read_text())
    for relative, expected in manifest["files"].items():
        file = (root / relative).resolve()
        if not file.is_relative_to(root):
            raise ValueError(f"Unsafe manifest path: {relative}")
        data = file.read_bytes()
        if len(data) != expected["bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError(f"Bundle mismatch: {relative}")
    print(json.dumps({"verified_files": len(manifest["files"]), "source_commit": manifest["source_commit"], "model_sha256": manifest["model_sha256"]}))


if __name__ == "__main__":
    main()
