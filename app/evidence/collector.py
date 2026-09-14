from typing import Any


class EvidenceCollector:
    def collect(self, selected_evidence: dict[str, Any]) -> dict[str, Any]:
        collected = []

        for item in selected_evidence.get("evidence", []):
            collected.append({
                "source": item["source"],
                "status": "COLLECTED",
                "data": {}
            })

        return {
            "trace_id": selected_evidence.get("trace_id"),
            "evidence": collected,
            "status": "COLLECTED"
        }


evidence_collector = EvidenceCollector()