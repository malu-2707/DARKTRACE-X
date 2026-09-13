from __future__ import annotations

from datetime import datetime

from normalizer.schema import ProcessEvent


def collect_process(
    event_id: str,
    source: str,
    process: str,
    parent_process: str | None = None,
    hostname: str | None = None,
    message: str | None = None,
) -> ProcessEvent:
    """Create a normalized process activity event."""

    return ProcessEvent(
        event_id=event_id,
        timestamp=datetime.now(),
        source=source,
        process=process,
        parent_process=parent_process,
        hostname=hostname,
        message=message,
    )


if __name__ == "__main__":
    event = collect_process(
        event_id="PROC-001",
        source="process_monitor",
        process="suspicious_demo_process",
        parent_process="sshd",
        hostname="server-01",
        message="Suspicious process detected",
    )

    print(event.model_dump_json(indent=2))
