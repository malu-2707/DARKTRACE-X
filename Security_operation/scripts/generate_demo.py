from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def generate_demo(output_file: str = "telemetry/demo_events.json") -> None:
    """Generate sample SOC telemetry for demonstration."""

    events = [
        {
            "event_id": "DEMO-001",
            "timestamp": datetime.now().isoformat(),
            "source": "suricata",
            "event_type": "NETWORK_ALERT",
            "severity": "HIGH",
            "source_ip": "192.168.56.20",
            "destination_ip": "192.168.56.10",
            "destination_port": 22,
            "protocol": "TCP",
            "attack_type": "SSH_BRUTE_FORCE",
            "mitre_technique": "T1110",
            "message": "Multiple SSH authentication attempts detected",
        },
        {
            "event_id": "DEMO-002",
            "timestamp": datetime.now().isoformat(),
            "source": "sshd",
            "event_type": "AUTHENTICATION",
            "severity": "MEDIUM",
            "source_ip": "192.168.56.20",
            "destination_ip": "192.168.56.10",
            "username": "admin",
            "result": "FAILED",
            "message": "Failed SSH authentication attempt",
        },
    ]

    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(events, indent=2), encoding="utf-8")

    print(f"Generated {len(events)} demo events: {path}")


if __name__ == "__main__":
    generate_demo()
