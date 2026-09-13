from __future__ import annotations

from datetime import datetime
from typing import Any

from normalizer.schema import SOCAlert, Severity


def collect_alert(
    event_id: str,
    source: str,
    attack_type: str,
    severity: Severity = Severity.MEDIUM,
    source_ip: str | None = None,
    destination_ip: str | None = None,
    destination_port: int | None = None,
    protocol: str | None = None,
    mitre_technique: str | None = None,
    message: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> SOCAlert:
    """Create a normalized SOC alert from detection data."""

    return SOCAlert(
        event_id=event_id,
        timestamp=datetime.now(),
        source=source,
        severity=severity,
        source_ip=source_ip,
        destination_ip=destination_ip,
        destination_port=destination_port,
        protocol=protocol,
        attack_type=attack_type,
        mitre_technique=mitre_technique,
        message=message,
        metadata=metadata or {},
    )


if __name__ == "__main__":
    alert = collect_alert(
        event_id="EVT-001",
        source="suricata",
        attack_type="SSH_BRUTE_FORCE",
        severity=Severity.HIGH,
        source_ip="192.168.56.20",
        destination_ip="192.168.56.10",
        destination_port=22,
        protocol="TCP",
        mitre_technique="T1110",
        message="Multiple SSH authentication attempts detected",
    )

    print(alert.model_dump_json(indent=2))
