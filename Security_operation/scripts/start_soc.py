from __future__ import annotations

import subprocess
import sys


def run_health_check() -> int:
    """Run the SOC health check before starting."""
    result = subprocess.run(
        [sys.executable, "scripts/health_check.py"],
        check=False,
    )
    return result.returncode


def start_soc() -> None:
    """Start the SOC processing environment."""

    print("Starting SOC environment...")

    if run_health_check() != 0:
        print("SOC health check failed.")
        return

    print("SOC environment is ready.")


if __name__ == "__main__":
    start_soc()
