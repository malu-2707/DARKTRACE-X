cat > normalizer/normalize_network.py <<'PY'
from __future__ import annotations

from typing import Any

from normalizer.schema import NetworkConnectionEvent


def normalize_network(data: dict[str, Any]) -> NetworkConnectionEvent:
    """Normalize a raw network connection event."""

    return NetworkConnectionEvent.model_validate(
        {
            "event_id": data["event_id"],
            "timestamp": data["timestamp"],
            "source": data["source"],
            "severity": data.get("severity", "MEDIUM"),
            "source_ip": data.get("source_ip"),
            "destination_ip": data["destination_ip"],
            "destination_port": data["destination_port"],
            "source_port": data.get("source_port"),
            "protocol": data.get("protocol"),
            "hostname": data.get("hostname"),
            "message": data.get("message"),
            "metadata": data.get("metadata", {}),
        }
    )
PY
