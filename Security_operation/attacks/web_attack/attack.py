from __future__ import annotations

from datetime import datetime


def simulate_web_attack(
    source_ip: str = "192.168.56.20",
    target_ip: str = "192.168.56.10",
) -> list[dict]:
    """Generate simulated web attack events."""

    attacks = [
        ("WEB-001", "/login.php", "SQL_INJECTION", "T1190"),
        ("WEB-002", "/admin", "PATH_TRAVERSAL", "T1190"),
        ("WEB-003", "/upload", "MALICIOUS_UPLOAD", "T1505"),
    ]

    events = []

    for event_id, path, attack_type, technique in attacks:
        events.append(
            {
                "event_id": event_id,
                "timestamp": datetime.now().isoformat(),
                "source": "web_monitor",
                "event_type": "NETWORK_ALERT",
                "severity": "HIGH",
                "source_ip": source_ip,
                "destination_ip": target_ip,
                "destination_port": 80,
                "protocol": "HTTP",
                "attack_type": attack_type,
                "mitre_technique": technique,
                "message": f"Simulated web attack against {path}",
            }
        )

    return events


if __name__ == "__main__":
    for event in simulate_web_attack():
        print(event)
