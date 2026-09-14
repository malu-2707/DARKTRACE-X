from pathlib import Path


def reset_environment() -> None:
    """Remove generated demo files and reset the SOC simulation state."""

    generated_files = [
        Path("telemetry/demo_events.json"),
    ]

    for file_path in generated_files:
        if file_path.exists():
            file_path.unlink()
            print(f"Removed: {file_path}")

    print("SOC environment reset complete.")


if __name__ == "__main__":
    reset_environment()
