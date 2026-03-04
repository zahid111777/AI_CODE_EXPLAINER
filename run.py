"""
run.py — Single-command launcher for AI Code Explainer.

Usage:
    python run.py

Starts:
    • FastAPI backend  →  http://localhost:8000
    • Streamlit frontend  →  http://localhost:8501
"""

import subprocess
import sys
import os
import time
import signal
import threading
import urllib.request
import urllib.error

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))

BACKEND_CMD = [
    sys.executable, "-m", "uvicorn",
    "backend.src.main:app",
    "--host", "0.0.0.0",
    "--port", "8000",
    "--reload",
]

FRONTEND_CMD = [
    sys.executable, "-m", "streamlit", "run",
    os.path.join(ROOT, "frontend", "frontend.py"),
    "--server.port", "8501",
    "--server.headless", "false",
]

# ── Colour helpers ─────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def tag(label: str, color: str) -> str:
    return f"{color}{BOLD}[{label}]{RESET}"

# ── Stream output from a process ──────────────────────────────────────────────
def stream(proc: subprocess.Popen, label: str, color: str) -> None:
    for line in iter(proc.stdout.readline, b""):
        print(f"{tag(label, color)} {line.decode(errors='replace').rstrip()}", flush=True)

# ── Health-check: wait until backend /health returns 200 ──────────────────────
def wait_for_backend(url: str = "http://localhost:8000/health",
                     timeout: int = 30) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(1)
    return False

# ── Main launcher ──────────────────────────────────────────────────────────────
def main() -> None:
    print(f"\n{BOLD}{CYAN}{'='*54}{RESET}")
    print(f"{BOLD}{CYAN}   🤖  AI Code Explainer — Unified Launcher{RESET}")
    print(f"{BOLD}{CYAN}{'='*54}{RESET}\n")

    # ── Start backend ─────────────────────────────────────────────────────────
    print(f"{tag('BACKEND', GREEN)}  Starting FastAPI on http://localhost:8000 …")
    backend = subprocess.Popen(
        BACKEND_CMD,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    threading.Thread(
        target=stream, args=(backend, "BACKEND ", GREEN), daemon=True
    ).start()

    # Wait until backend is actually accepting requests
    print(f"{tag('BACKEND', GREEN)}  Waiting for backend to be ready …")
    if not wait_for_backend(timeout=30):
        print(f"{tag('ERROR', RED)}  Backend did not start within 30 s. "
              "Check the [BACKEND] logs above for errors.")
        backend.terminate()
        sys.exit(1)

    print(f"{tag('BACKEND', GREEN)}  ✅  Backend is ready.\n")

    # ── Start frontend ────────────────────────────────────────────────────────
    print(f"{tag('FRONTEND', YELLOW)}  Starting Streamlit on http://localhost:8501 …")
    frontend = subprocess.Popen(
        FRONTEND_CMD,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    threading.Thread(
        target=stream, args=(frontend, "FRONTEND", YELLOW), daemon=True
    ).start()

    print(f"\n{BOLD}{GREEN}  ✅  Both services are running!{RESET}")
    print(f"  • Backend  →  {CYAN}http://localhost:8000{RESET}")
    print(f"  • Frontend →  {CYAN}http://localhost:8501{RESET}")
    print(f"\n  Press {BOLD}Ctrl+C{RESET} to stop everything.\n")

    # ── Graceful shutdown on Ctrl+C ───────────────────────────────────────────
    def shutdown(sig, frame):
        print(f"\n{tag('LAUNCHER', RED)}  Shutting down …")
        for proc in (frontend, backend):
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
        print(f"{tag('LAUNCHER', RED)}  All processes stopped. Goodbye!\n")
        sys.exit(0)

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Keep main thread alive
    backend.wait()
    frontend.wait()


if __name__ == "__main__":
    main()
