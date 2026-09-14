from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

from normalizer.schema import SOCEvent


class AlertDeduplicator:
    """Remove repeated alerts occurring within a configurable time window."""

    def __init__(self, window_seconds: int = 60):
        self.window = timedelta(seconds=window_seconds)

    def deduplicate(self, events: Iterable[SOCEvent]) -> list[SOCEvent]:
        result: list[SOCEvent] = []
        seen: dict[str, datetime] = {}

        for event in events:
            timestamp = self._timestamp(event)
            key = self._dedup_key(event)

            previous = seen.get(key)

            if previous is not None and timestamp - previous <= self.window:
                continue

            seen[key] = timestamp
            result.append(event)

        return result

    def _dedup_key(self, event: SOCEvent) -> str:
        return "|".join([
            str(event.source),
            str(event.event_type),
            str(event.attack_type),
            str(event.source_ip or ""),
            str(event.destination_ip or ""),
            str(event.destination_port or ""),
        ])

    def _timestamp(self, event: SOCEvent) -> datetime:
        timestamp = event.timestamp

        if isinstance(timestamp, datetime):
            return timestamp

        return datetime.fromisoformat(
            str(timestamp).replace("Z", "+00:00")
        )


if __name__ == "__main__":
    from normalizer.schema import EventType, Severity

    events = [
        SOCEvent(
            event_id="ALERT-001",
            timestamp="2026-09-14T13:27:40+05:30",
            source="suricata",
            event_type=EventType.NETWORK_ALERT,
            severity=Severity.HIGH,
            source_ip="172.17.102.31",
            destination_ip="172.17.99.249",
            destination_port=22,
            attack_type="SSH_BRUTE_FORCE",
        ),
        SOCEvent(
            event_id="ALERT-002",
            timestamp="2026-09-14T13:27:45+05:30",
            source="suricata",
            event_type=EventType.NETWORK_ALERT,
            severity=Severity.HIGH,
            source_ip="172.17.102.31",
            destination_ip="172.17.99.249",
            destination_port=22,
            attack_type="SSH_BRUTE_FORCE",
        ),
        SOCEvent(
            event_id="ALERT-003",
            timestamp="2026-09-14T13:29:00+05:30",
            source="suricata",
            event_type=EventType.NETWORK_ALERT,
            severity=Severity.HIGH,
            source_ip="172.17.102.31",
            destination_ip="172.17.99.249",
            destination_port=22,
            attack_type="SSH_BRUTE_FORCE",
        ),
    ]

    deduplicated = AlertDeduplicator(window_seconds=60).deduplicate(events)

    print(f"Input alerts: {len(events)}")
    print(f"After deduplication: {len(deduplicated)}")

    for event in deduplicated:
        print(
            f"{event.event_id} | "
            f"{event.attack_type} | "
            f"{event.source_ip} -> "
            f"{event.destination_ip}:{event.destination_port}"
        )
