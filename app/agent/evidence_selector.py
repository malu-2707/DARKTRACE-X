from typing import Any


class EvidenceSelector:
    def select(self, plan: dict[str, Any]) -> dict[str, Any]:
        selected_evidence = []

        for step in plan.get("steps", []):
            selected_evidence.append({
                "source": step,
                "required": True
            })

        return {
            "trace_id": plan.get("trace_id"),
            "evidence": selected_evidence,
            "status": "SELECTED"
        }


evidence_selector = EvidenceSelector()