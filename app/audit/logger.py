from datetime import datetime, timezone
from typing import Any


class AuditLogger:
    def log(self, event: dict[str, Any]) -> dict[str, Any]:
        audit_record = {
            "trace_id": event.get("trace_id"),
            "event": event,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "status": "RECORDED"
        }

        return audit_record


audit_logger = AuditLogger()