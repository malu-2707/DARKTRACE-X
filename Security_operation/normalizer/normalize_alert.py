from __future__ import annotations

from typing import Any

from normalizer.schema import SOCAlert, Severity


def normalize_alert(data: dict[str, Any]) -> SOCAlert:
    """Normalize a raw security alert into SOCAlert."""

    return SOCAlert.model_validate(
        {
            "event_id": data["event_id"],
            "timestamp": data["timestamp"],
            "source": data["source"],
            "severity": data.get("severity", Severity.MEDIUM),
            "source_ip": data.get("source_ip"),
            "destination_ip": data.get("destination_ip"),
            "source_port": data.get("source_port"),
            "destination_port": data.get("destination_port"),
            "protocol": data.get("protocol"),
            "attack_type": data["attack_type"],
            "mitre_technique": data.get("mitre_technique"),
            "asset_id": data.get("asset_id"),
            "hostname": data.get("hostname"),
            "message": data.get("message"),
            "metadata": data.get("metadata", {}),
        }
    )
