from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

from normalizer.schema import EventType, Severity, SOCEvent


def map_event_type(event_type: str) -> EventType:
    """Map Suricata event types to the SOC event model."""
    if event_type == "alert":
        return EventType.NETWORK_ALERT
    if event_type in {"flow", "dns", "http", "ssh"}:
        return EventType.NETWORK_CONNECTION
    return EventType.PACKET_METADATA


def map_severity(alert: dict[str, Any]) -> Severity:
    """Map Suricata priority to SOC severity."""
    priority = alert.get("alert", {}).get("severity")

    if priority == 1:
        return Severity.CRITICAL
    if priority == 2:
        return Severity.HIGH
    if priority == 3:
        return Severity.MEDIUM
    return Severity.LOW


def normalize_suricata_event(event: dict[str, Any]) -> SOCEvent:
    """Convert one Suricata EVE event into a SOCEvent."""

    event_type = event.get("event_type", "unknown")
    alert = event.get("alert", {})

    attack_type = alert.get(
        "signature",
        f"SURICATA_{event_type.upper()}",
    )

    mitre_technique = None

    metadata = {
        "suricata_event_type": event_type,
        "flow_id": event.get("flow_id"),
        "community_id": event.get("community_id"),
        "interface": event.get("in_iface"),
        "alert": alert,
    }

    return SOCEvent(
        event_id=str(
            event.get(
                "event_id",
                f"SURI-{event.get('timestamp', 'UNKNOWN')}-{event.get('flow_id', '')}",
            )
        ),
        timestamp=event["timestamp"],
        source="suricata",
        event_type=map_event_type(event_type),
        severity=map_severity(event),
        source_ip=event.get("src_ip"),
        destination_ip=event.get("dest_ip"),
        source_port=event.get("src_port"),
        destination_port=event.get("dest_port"),
        protocol=event.get("proto"),
        attack_type=attack_type,
        mitre_technique=mitre_technique,
        message=alert.get("signature"),
        metadata=metadata,
    )


def read_suricata_events(
    eve_file: str | Path,
    limit: int | None = None,
) -> Iterator[SOCEvent]:
    """Read Suricata EVE JSON lines and yield normalized SOC events."""

    path = Path(eve_file)

    if not path.exists():
        raise FileNotFoundError(f"Suricata EVE file not found: {path}")

    count = 0

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            try:
                event = json.loads(line)
                yield normalize_suricata_event(event)
                count += 1
            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                continue

            if limit is not None and count >= limit:
                break


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Read and normalize Suricata EVE JSON events."
    )

    parser.add_argument(
        "--file",
        default="suricata/logs/eve.json",
        help="Path to Suricata EVE JSON",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of events to read",
    )

    args = parser.parse_args()

    count = 0

    for event in read_suricata_events(args.file, args.limit):
        print(
            f"{event.event_id} | "
            f"{event.event_type.value} | "
            f"{event.source_ip} -> "
            f"{event.destination_ip}:{event.destination_port} | "
            f"{event.severity.value}"
        )
        count += 1

    print(f"Normalized Suricata events: {count}")
