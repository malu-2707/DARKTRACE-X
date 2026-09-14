from __future__ import annotations

from datetime import datetime

from normalizer.schema import AuthenticationEvent


def collect_authentication(
    event_id: str,
    source: str,
    username: str,
    result: str,
    source_ip: str | None = None,
    destination_ip: str | None = None,
    message: str | None = None,
) -> AuthenticationEvent:
    """Create a normalized authentication event."""

    return AuthenticationEvent(
        event_id=event_id,
        timestamp=datetime.now(),
        source=source,
        username=username,
        result=result,
        source_ip=source_ip,
        destination_ip=destination_ip,
        message=message,
    )


if __name__ == "__main__":
    event = collect_authentication(
        event_id="AUTH-001",
        source="sshd",
        username="admin",
        result="FAILED",
        source_ip="192.168.56.20",
        destination_ip="192.168.56.10",
        message="Failed SSH authentication attempt",
    )

    print(event.model_dump_json(indent=2))
