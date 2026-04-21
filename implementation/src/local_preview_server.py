from __future__ import annotations

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os

PORT = 8787


def main() -> None:
    site_dir = Path(__file__).resolve().parents[1] / "output" / "site"
    os.chdir(site_dir)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler)
    print(f"Serving {site_dir} at http://0.0.0.0:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
