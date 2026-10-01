"""Open a ready local demo; use only standard-library launch dependencies."""

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen
import webbrowser

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--saved", action="store_true")
    args = parser.parse_args()
    port = 8001 if args.saved else 8000
    base = f"http://127.0.0.1:{port}"

    def ready():
        try:
            with urlopen(base + ("/index.html" if args.saved else "/health"), timeout=.5) as response:
                body = response.read()
            return b"DustTwin" in body if args.saved else json.loads(body).get("ready") is True
        except (URLError, ValueError, TimeoutError):
            return False

    if ready():
        print("DustTwin is already running. Opening the local dashboard.")
        webbrowser.open(base)
        return
    script = ROOT / "scripts" / ("serve_static.py" if args.saved else "serve.py")
    server = subprocess.Popen([sys.executable, str(script)], cwd=ROOT)
    try:
        deadline = time.monotonic() + 20
        while not ready():
            if server.poll() is not None:
                raise SystemExit("The local server could not start. Check the message above and docs/offline-demo.md.")
            if time.monotonic() >= deadline:
                raise SystemExit("The model did not become ready. Use Start Saved Replay.command for the backup.")
            time.sleep(.15)
        print(f"Ready: {base}. Keep this window open; Control-C stops the demo.")
        webbrowser.open(base)
        server.wait()
    except KeyboardInterrupt:
        pass
    finally:
        if server.poll() is None:
            server.terminate()
            server.wait(timeout=5)


if __name__ == "__main__":
    main()
