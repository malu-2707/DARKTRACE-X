from __future__ import annotations

from datetime import datetime

from normalizer.schema import NetworkConnectionEvent


def collect_network_connection(
    event_id: str,
    source: str,
    destination_ip: str,
    destination_port: int,
    source_ip: str | None = None,
    protocol: str | None = None,
    message: str | None = None,
) -> NetworkConnectionEvent:
    """Create a normalized network connection event."""

    return NetworkConnectionEvent(
        event_id=event_id,
        timestamp=datetime.now(),
        source=source,
        source_ip=source_ip,
        destination_ip=destination_ip,
        destination_port=destination_port,
        protocol=protocol,
        message=message,
    )


if __name__ == "__main__":
    event = collect_network_connection(
        event_id="NET-001",
        source="network_monitor",
        source_ip="192.168.56.20",
        destination_ip="192.168.56.10",
        destination_port=22,
        protocol="TCP",
        message="SSH connection observed",
    )

    print(event.model_dump_json(indent=2))
