from __future__ import annotations
from datetime import datetime
def simulate_ssh_bruteforce(
    source_ip: str = "192.168.56.20",
    target_ip: str = "192.168.56.10",
    attempts: int = 10,
) -> list[dict]:
    """Generate simulated SSH brute-force events."""

    events = []

    for attempt in range(1, attempts + 1):
        events.append(
            {
                "event_id": f"SSH-BRUTE-{attempt:03d}",
                "timestamp": datetime.now().isoformat(),
                "source": "ssh_simulator",
                "event_type": "AUTHENTICATION",
                "severity": "HIGH",
                "source_ip": source_ip,
                "destination_ip": target_ip,
                "destination_port": 22,
                "protocol": "TCP",
                "username": "admin",
                "result": "FAILED",
                "attack_type": "SSH_BRUTE_FORCE",
                "mitre_technique": "T1110",
                "message": f"Simulated SSH login attempt {attempt}",
            }
        )

    return events


if __name__ == "__main__":
    for event in simulate_ssh_bruteforce():
        print(event)
