from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Iterable

from normalizer.schema import SOCEvent


class EventCorrelator:
    """Correlate SOC events using source, destination and time proximity."""

    def __init__(self, window_seconds: int = 60):
        self.window = timedelta(seconds=window_seconds)

    def correlate(self, events: Iterable[SOCEvent]) -> list[list[SOCEvent]]:
        groups: dict[str, list[SOCEvent]] = defaultdict(list)

        for event in events:
            groups[self._correlation_key(event)].append(event)

        correlated: list[list[SOCEvent]] = []

        for group in groups.values():
            group.sort(key=self._timestamp)
            current: list[SOCEvent] = []

            for event in group:
                if not current:
                    current.append(event)
                elif self._timestamp(event) - self._timestamp(current[-1]) <= self.window:
                    current.append(event)
                else:
                    if len(current) > 1:
                        correlated.append(current)
                    current = [event]

            if len(current) > 1:
                correlated.append(current)

        return correlated

    def _correlation_key(self, event: SOCEvent) -> str:
        return "|".join([
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
            event_id="WAZUH-001",
            timestamp="2026-09-14T13:27:40+05:30",
            source="wazuh",
            event_type=EventType.AUTHENTICATION,
            severity=Severity.HIGH,
            source_ip="172.17.102.31",
            destination_ip="172.17.99.249",
            destination_port=22,
            attack_type="SSH_AUTH_FAILURE",
        ),
        SOCEvent(
            event_id="SURI-001",
            timestamp="2026-09-14T13:27:45+05:30",
            source="suricata",
            event_type=EventType.NETWORK_ALERT,
            severity=Severity.HIGH,
            source_ip="172.17.102.31",
            destination_ip="172.17.99.249",
            destination_port=22,
            attack_type="SSH_BRUTE_FORCE",
        ),
    ]

    groups = EventCorrelator(window_seconds=60).correlate(events)

    print(f"Correlated groups: {len(groups)}")

    for index, group in enumerate(groups, 1):
        print(f"Group {index}:")
        for event in group:
            print(
                f"  {event.source} | "
                f"{event.attack_type} | "
                f"{event.severity.value}"
            )
