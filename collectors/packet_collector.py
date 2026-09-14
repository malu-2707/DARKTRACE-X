from __future__ import annotations

from datetime import datetime
from typing import Any

from normalizer.schema import SOCEvent, EventType, Severity


def collect_packet(
    event_id: str,
    source: str,
    source_ip: str | None = None,
    destination_ip: str | None = None,
    source_port: int | None = None,
    destination_port: int | None = None,
    protocol: str | None = None,
    severity: Severity = Severity.MEDIUM,
    metadata: dict[str, Any] | None = None,
) -> SOCEvent:
    """Create a normalized packet metadata event."""

    return SOCEvent(
        event_id=event_id,
        timestamp=datetime.now(),
        source=source,
        event_type=EventType.PACKET_METADATA,
        severity=severity,
        source_ip=source_ip,
        destination_ip=destination_ip,
        source_port=source_port,
        destination_port=destination_port,
        protocol=protocol,
        metadata=metadata or {},
    )


if __name__ == "__main__":
    event = collect_packet(
        event_id="PKT-001",
        source="packet_monitor",
        source_ip="192.168.56.20",
        destination_ip="192.168.56.10",
        source_port=45678,
        destination_port=22,
        protocol="TCP",
    )

    print(event.model_dump_json(indent=2))
