"""Stage local evidence and approved team details for the static fallback."""

import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    def read(path):
        return json.loads((ROOT / path).read_text())
    evidence = {"metadata": read("models/model-metadata.json"), "test": read("reports/evaluation/test-metrics.json"),
                "training": read("reports/training/validation-selection.json"), "fixture": read("reports/training/prediction-fixture.json")}
    (ROOT / "demo/evidence.json").write_text(json.dumps(evidence, separators=(",", ":")) + "\n")
    site = {"team": read("configs/team.json"), "build_parent_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "problem_source": {"title": "World Bank: In Bangladesh, an urgent call for clean air", "url": "https://blogs.worldbank.org/en/endpovertyinsouthasia/bangladesh-urgent-call-clean-air"},
            "costs": read("configs/feasibility.json") if (ROOT / "configs/feasibility.json").exists() else None}
    (ROOT / "demo/site.json").write_text(json.dumps(site, indent=2) + "\n")
    documents = ROOT / "demo/documents"
    documents.mkdir(parents=True, exist_ok=True)
    for relative in ("models/model-card.md", "docs/simulation.md", "docs/inference.md", "docs/feasibility.md", "docs/judge-script.md", "docs/offline-demo.md", "docs/third-party-notices.md"):
        if (ROOT / relative).exists():
            shutil.copyfile(ROOT / relative, documents / Path(relative).name)
    packet = ROOT / "output/pdf/dusttwin-judge-packet.pdf"
    if packet.exists():
        shutil.copyfile(packet, documents / packet.name)
    print("Staged approved team, frozen evidence and available documents for local/static use.")


if __name__ == "__main__":
    main()
