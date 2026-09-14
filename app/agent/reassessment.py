from typing import Any


class ReassessmentEngine:
    def reassess(self, verification: dict[str, Any]) -> dict[str, Any]:
        verification_status = verification.get(
            "verification_status"
        )

        if verification_status == "VERIFIED":
            outcome = "SUCCESS"
            reassessment_required = False

        elif verification_status == "NOT_EXECUTED":
            outcome = "PENDING"
            reassessment_required = True

        else:
            outcome = "FAILED"
            reassessment_required = True

        return {
            "trace_id": verification.get("trace_id"),
            "outcome": outcome,
            "reassessment_required": reassessment_required,
            "status": "REASSESSED"
        }


reassessment_engine = ReassessmentEngine()