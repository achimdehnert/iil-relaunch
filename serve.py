#!/usr/bin/env python3
"""
IIL Relaunch — Dev & Staged Server

Usage:
  python serve.py dev       →  localhost:9000  (working directory, live-edit)
  python serve.py staged    →  localhost:9001  (git main, read-only snapshot)
  python serve.py both      →  starts both
"""

import http.server
import os
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading

PORTS = {"dev": 9000, "staged": 9001}


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Suppress noisy log lines for assets."""

    def log_message(self, format, *args):
        # Only log HTML requests, not assets
        if ".html" in str(args[0]) or "GET / " in str(args[0]) or "HEAD" in str(args[0]):
            super().log_message(format, *args)


def serve(directory: str, port: int, label: str):
    handler = lambda *a, **kw: QuietHandler(*a, directory=directory, **kw)
    with socketserver.ThreadingTCPServer(("", port), handler) as httpd:
        httpd.allow_reuse_address = True
        print(f"  [{label.upper()}]  http://localhost:{port}/  →  {directory}")
        httpd.serve_forever()


def create_staged_snapshot() -> str:
    """Export git HEAD (main) to a temp directory."""
    tmp = tempfile.mkdtemp(prefix="iil-staged-")
    repo = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(
        ["git", "archive", "--format=tar", "HEAD"],
        cwd=repo,
        stdout=subprocess.PIPE,
        check=True,
    ).stdout
    # Use git archive piped to tar extract
    proc = subprocess.run(
        f"git -C {repo} archive HEAD | tar -x -C {tmp}",
        shell=True,
        check=True,
    )
    return tmp


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "dev"
    repo_dir = os.path.dirname(os.path.abspath(__file__))

    if mode not in ("dev", "staged", "both"):
        print(f"Usage: python serve.py [dev|staged|both]")
        sys.exit(1)

    print("─── IIL Relaunch Server ───────────────────────")

    threads = []

    if mode in ("dev", "both"):
        t = threading.Thread(target=serve, args=(repo_dir, PORTS["dev"], "dev"), daemon=True)
        t.start()
        threads.append(t)

    if mode in ("staged", "both"):
        staged_dir = create_staged_snapshot()
        t = threading.Thread(target=serve, args=(staged_dir, PORTS["staged"], "staged"), daemon=True)
        t.start()
        threads.append(t)

    print("─── Ctrl+C to stop ───────────────────────────\n")

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
