cat > normalizer/normalize_auth.py <<'PY'
from __future__ import annotations

from typing import Any

from normalizer.schema import AuthenticationEvent


def normalize_auth(data: dict[str, Any]) -> AuthenticationEvent:
    """Normalize a raw authentication event."""

    return AuthenticationEvent.model_validate(
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
            "username": data["username"],
            "result": data["result"],
            "hostname": data.get("hostname"),
            "message": data.get("message"),
            "metadata": data.get("metadata", {}),
        }
    )
PY
