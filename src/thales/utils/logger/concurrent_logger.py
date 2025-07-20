#!/usr/bin/env python3
"""Concurrent-safe logging setup using `concurrent-log-handler`.

This standalone module shows how to create a single, size‑rotated log file that
all Python processes in your project can write to safely.  It includes:

* `setup_logging()` – configure a `ConcurrentRotatingFileHandler` and console
  handler.
* `get_logger()` – convenience wrapper around `logging.getLogger()`.
* `main()` – demo that spawns several `multiprocessing` workers, each writing
  to the **same** `logs/debug.log` file without clobbering each other.

Requirements:
    pip install concurrent-log-handler

Usage (run from repo root):
    python concurrent_logging_setup.py
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Final

from concurrent_log_handler import ConcurrentRotatingFileHandler

# ---------------------------------------------------------------------------
# 1.  Decide where the shared log should live (absolute path)
# ---------------------------------------------------------------------------
REPO_ROOT: Final[Path] = Path(__file__).resolve().parent  # adjust if needed
LOG_DIR: Final[Path] = REPO_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE: Final[Path] = LOG_DIR / "debug.log"

# ---------------------------------------------------------------------------
# 2.  Configure logging
# ---------------------------------------------------------------------------

def setup_logging(
    log_file: Path = LOG_FILE,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB per file
    backup_count: int = 5,
    log_level: int = logging.DEBUG,
) -> None:
    """Set up a concurrent‑safe rotating file + console logger.

    Call this **once per process** (main and every worker).  Using ``force=True``
    ensures that re‑invocations in sub‑processes replace any default handlers
    added by libraries such as multiprocessing or celery.
    """

    # Format includes the process ID so interleaved lines are easy to tell apart.
    fmt = "%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s"

    file_handler = ConcurrentRotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
        use_gzip=True,  # compress rotated backups
    )
    file_handler.setFormatter(logging.Formatter(fmt))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(fmt))

    # `force=True` wipes any existing root handlers, preventing duplicates.
    logging.basicConfig(level=log_level, handlers=[file_handler, console_handler], force=True)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger configured by :pyfunc:`setup_logging`."""
    return logging.getLogger(name)


# ---------------------------------------------------------------------------
# 3.  Demo – write from main + 3 worker processes
# ---------------------------------------------------------------------------

def main() -> None:
    import multiprocessing as mp

    setup_logging()  # configure in the main process
    root_log = get_logger(__name__)
    root_log.info("Start main process; spawning workers…")

    def worker(n: int) -> None:  # executed in new process
        setup_logging()  # each process sets up its own handlers
        log = get_logger(f"worker-{n}")
        for i in range(3):
            log.debug("worker %d loop %d", n, i)

    procs = [mp.Process(target=worker, args=(i,)) for i in range(3)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    root_log.info("All workers finished.  Check %s", LOG_FILE)


if __name__ == "__main__":
    main()
