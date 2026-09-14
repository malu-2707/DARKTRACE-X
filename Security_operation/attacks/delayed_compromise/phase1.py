from __future__ import annotations

from datetime import datetime


def simulate_phase1(
    source_ip: str = "192.168.56.20",
    target_ip: str = "192.168.56.10",
) -> dict:
    """Generate the initial phase of a simulated delayed compromise."""

    return {
        "event_id": "COMPROMISE-PHASE1",
        "timestamp": datetime.now().isoformat(),
        "source": "attack_simulator",
        "event_type": "NETWORK_ALERT",
        "severity": "HIGH",
        "source_ip": source_ip,
        "destination_ip": target_ip,
        "destination_port": 22,
        "protocol": "TCP",
        "attack_type": "INITIAL_ACCESS",
        "mitre_technique": "T1078",
        "message": "Initial access simulated for delayed compromise scenario",
    }


if __name__ == "__main__":
    print(simulate_phase1())
