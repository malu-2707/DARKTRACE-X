from __future__ import annotations
from datetime import datetime
def simulate_successful_ssh(
    source_ip: str = "192.168.56.20",
    target_ip: str = "192.168.56.10",
    username: str = "admin",
) -> dict:
    """Generate a simulated successful SSH login event."""

    return {
        "event_id": "SSH-SUCCESS-001",
        "timestamp": datetime.now().isoformat(),
        "source": "ssh_simulator",
        "event_type": "AUTHENTICATION",
        "severity": "HIGH",
        "source_ip": source_ip,
        "destination_ip": target_ip,
        "destination_port": 22,
        "protocol": "TCP",
        "username": username,
        "result": "SUCCESS",
        "message": "Successful SSH authentication detected",
    }


if __name__ == "__main__":
    print(simulate_successful_ssh())
