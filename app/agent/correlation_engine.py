from typing import Any


class CorrelationEngine:
    def correlate(self, evidence: dict[str, Any]) -> dict[str, Any]:
        items = evidence.get("evidence", [])

        correlated_events = []

        for item in items:
            correlated_events.append({
                "source": item.get("source"),
                "status": item.get("status"),
                "data": item.get("data", {})
            })

        return {
            "trace_id": evidence.get("trace_id"),
            "correlated_events": correlated_events,
            "event_count": len(correlated_events),
            "status": "CORRELATED"
        }


correlation_engine = CorrelationEngine()