"""Serve the saved offline website using only the Python standard library."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parents[1] / "apps/web/dist")
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()
    if not (args.directory / "index.html").is_file():
        parser.error("Built website unavailable. Build apps/web first or use the offline archive.")
    print(f"Saved replay: http://127.0.0.1:{args.port} (no live inference)", flush=True)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(SimpleHTTPRequestHandler, directory=str(args.directory)))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    main()
