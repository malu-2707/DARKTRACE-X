from __future__ import annotations

from datetime import datetime


def simulate_phase2(
    source_ip: str = "192.168.56.20",
    target_ip: str = "192.168.56.10",
) -> dict:
    """Generate the follow-up phase of a simulated delayed compromise."""

    return {
        "event_id": "COMPROMISE-PHASE2",
        "timestamp": datetime.now().isoformat(),
        "source": "attack_simulator",
        "event_type": "PROCESS_ACTIVITY",
        "severity": "CRITICAL",
        "source_ip": source_ip,
        "destination_ip": target_ip,
        "attack_type": "PERSISTENCE",
        "mitre_technique": "T1053",
        "hostname": "web-server-01",
        "message": "Delayed compromise phase 2: simulated persistence activity detected",
        "metadata": {
            "phase": 2,
            "indicator": "scheduled_task",
            "simulation": True,
        },
    }


if __name__ == "__main__":
    print(simulate_phase2())
