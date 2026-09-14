from __future__ import annotations

from typing import Any

from normalizer.schema import ProcessEvent


def normalize_process(data: dict[str, Any]) -> ProcessEvent:
    """Normalize a raw process event."""

    return ProcessEvent.model_validate(
        {
            "event_id": data["event_id"],
            "timestamp": data["timestamp"],
            "source": data["source"],
            "severity": data.get("severity", "MEDIUM"),
            "source_ip": data.get("source_ip"),
            "destination_ip": data.get("destination_ip"),
            "source_port": data.get("source_port"),
            "destination_port": data.get("destination_port"),
            "protocol": data.get("protocol"),
            "hostname": data.get("hostname"),
            "process": data["process"],
            "parent_process": data.get("parent_process"),
            "message": data.get("message"),
            "metadata": data.get("metadata", {}),
        }
    )
