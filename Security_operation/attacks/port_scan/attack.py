from __future__ import annotations

from datetime import datetime


def simulate_port_scan(
    source_ip: str = "192.168.56.20",
    target_ip: str = "192.168.56.10",
    ports: list[int] | None = None,
) -> list[dict]:
    """Generate simulated port-scan events."""

    if ports is None:
        ports = [21, 22, 23, 80, 443, 8080]

    events = []

    for port in ports:
        events.append(
            {
                "event_id": f"PORT-SCAN-{port}",
                "timestamp": datetime.now().isoformat(),
                "source": "network_scanner",
                "event_type": "NETWORK_ALERT",
                "severity": "MEDIUM",
                "source_ip": source_ip,
                "destination_ip": target_ip,
                "destination_port": port,
                "protocol": "TCP",
                "attack_type": "PORT_SCAN",
                "mitre_technique": "T1046",
                "message": f"Simulated port scan against port {port}",
            }
        )

    return events


if __name__ == "__main__":
    for event in simulate_port_scan():
        print(event)
