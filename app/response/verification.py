from typing import Any


class VerificationService:
    def verify(self, response_result: dict[str, Any]) -> dict[str, Any]:
        trace_id = response_result.get("trace_id")
        status = response_result.get("status")

        if status == "ACTION_EXECUTED":
            verified = True
            verification_status = "VERIFIED"
        elif status == "WAITING_FOR_APPROVAL":
            verified = False
            verification_status = "NOT_EXECUTED"
        else:
            verified = False
            verification_status = "NO_ACTION_TO_VERIFY"

        return {
            "trace_id": trace_id,
            "action": response_result.get("action"),
            "verified": verified,
            "verification_status": verification_status,
            "status": "VERIFICATION_COMPLETED"
        }


verification_service = VerificationService()