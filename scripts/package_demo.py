"""Archive a clean source snapshot, built offline assets and verified model."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/releases/dusttwin-round1-demo-v1.zip"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    state = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
    if state.strip():
        raise SystemExit("Commit the verified source/checkpoint before creating the release archive.")
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    files = {ROOT / path for path in tracked if path and (ROOT / path).is_file()}
    dist = ROOT / "apps/web/dist"
    artifact = ROOT / "models/artifacts/pm10-initial.joblib"
    if not (dist / "index.html").exists() or not artifact.exists():
        raise SystemExit("Build the website and verify/download the pinned fitted artifact first.")
    for directory in ("demo", "reports"):
        for source in (ROOT / directory).rglob("*"):
            if source.is_file():
                staged = dist / source.relative_to(ROOT)
                if not staged.is_file() or sha(staged) != sha(source):
                    raise SystemExit(f"Static evidence is stale: {source.relative_to(ROOT)}. Rebuild apps/web before packaging.")
    metadata = json.loads((ROOT / "models/model-metadata.json").read_text())
    if sha(artifact) != metadata["artifact_sha256"]:
        raise SystemExit("Fitted artifact hash does not match frozen metadata.")
    files.add(artifact)
    files.update(p for p in dist.rglob("*") if p.is_file())
    manifest = {"schema_version": 1, "built_at_utc": datetime.now(timezone.utc).isoformat(),
                "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "source_worktree_clean": True, "model_sha256": metadata["artifact_sha256"],
                "scope": "Round 1 software. Live inference needs Python 3.14 + pinned packages; saved replay needs Python standard library and a modern browser.",
                "files": {str(p.relative_to(ROOT)): {"sha256": sha(p), "bytes": p.stat().st_size} for p in sorted(files)}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(files):
            archive.write(path, "DustTwin-AI/" + str(path.relative_to(ROOT)))
        archive.writestr("DustTwin-AI/bundle-manifest.json", json.dumps(manifest, indent=2) + "\n")
    info = {"archive": OUT.name, "bytes": OUT.stat().st_size, "sha256": sha(OUT),
            "source_commit": manifest["source_commit"], "files": len(files), "model_sha256": metadata["artifact_sha256"]}
    OUT.with_suffix(".sha256").write_text(f'{info["sha256"]}  {OUT.name}\n')
    OUT.with_suffix(".json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps(info))


if __name__ == "__main__":
    main()
