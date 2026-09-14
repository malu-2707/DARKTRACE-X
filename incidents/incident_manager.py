from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable
from uuid import uuid4

from normalizer.schema import Severity, SOCEvent


@dataclass
class Incident:
    """Represents a correlated security incident."""

    incident_id: str
    created_at: datetime
    severity: Severity
    title: str
    events: list[SOCEvent] = field(default_factory=list)
    status: str = "OPEN"
    risk_score: int = 0

    def add_event(self, event: SOCEvent) -> None:
        self.events.append(event)

    def to_dict(self) -> dict:
        return {
            "incident_id": self.incident_id,
            "created_at": self.created_at.isoformat(),
            "severity": self.severity.value,
            "title": self.title,
            "status": self.status,
            "risk_score": self.risk_score,
            "event_count": len(self.events),
            "event_ids": [event.event_id for event in self.events],
        }


class IncidentManager:
    """Create incidents from correlated SOC events."""

    def create_incident(
        self,
        events: Iterable[SOCEvent],
        risk_score: int = 0,
    ) -> Incident:
        events = list(events)

        if not events:
            raise ValueError("Cannot create an incident without events")

        severity = max(
            events,
            key=lambda event: self._severity_value(event.severity),
        ).severity

        attack_types = sorted(
            {
                event.attack_type
                for event in events
                if event.attack_type
            }
        )

        title = " / ".join(attack_types) or "Security Event"

        created_at = min(
            self._timestamp(event)
            for event in events
        )

        return Incident(
            incident_id=f"INC-{uuid4().hex[:8].upper()}",
            created_at=created_at,
            severity=severity,
            title=title,
            events=events,
            risk_score=risk_score,
        )

    def _severity_value(self, severity: Severity) -> int:
        return {
            Severity.LOW: 1,
            Severity.MEDIUM: 2,
            Severity.HIGH: 3,
            Severity.CRITICAL: 4,
        }.get(severity, 0)

    def _timestamp(self, event: SOCEvent) -> datetime:
        timestamp = event.timestamp

        if isinstance(timestamp, datetime):
            return timestamp

        return datetime.fromisoformat(
            str(timestamp).replace("Z", "+00:00")
        )


if __name__ == "__main__":
    from normalizer.schema import EventType

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

    incident = IncidentManager().create_incident(
        events,
        risk_score=90,
    )

    print(f"Incident ID: {incident.incident_id}")
    print(f"Title: {incident.title}")
    print(f"Severity: {incident.severity.value}")
    print(f"Risk score: {incident.risk_score}/100")
    print(f"Status: {incident.status}")
    print(f"Event count: {len(incident.events)}")
