from pathlib import Path


def check_file(path: str) -> bool:
    file_path = Path(path)
    return file_path.exists() and file_path.stat().st_size > 0


def health_check() -> bool:
    required_files = [
        "normalizer/schema.py",
        "normalizer/normalize_alert.py",
        "normalizer/normalize_auth.py",
        "normalizer/normalize_process.py",
        "normalizer/normalize_network.py",
        "collectors/alert_collector.py",
        "collectors/auth_collector.py",
        "collectors/network_collector.py",
        "collectors/process_collector.py",
        "collectors/packet_collector.py",
    ]

    results = {file: check_file(file) for file in required_files}

    for file, status in results.items():
        print(f"{'OK' if status else 'MISSING'}: {file}")

    return all(results.values())


if __name__ == "__main__":
    status = health_check()
    print(f"SOC health status: {'HEALTHY' if status else 'INCOMPLETE'}")
