from typing import Any


class ApprovalPolicy:
    def evaluate(self, policy_result: dict[str, Any]) -> dict[str, Any]:
        policy_action = policy_result.get("policy_action")

        if policy_action == "REQUIRE_APPROVAL":
            approval_required = True
            action_status = "PENDING_APPROVAL"
        else:
            approval_required = False
            action_status = "AUTO_ALLOWED"

        return {
            "trace_id": policy_result.get("trace_id"),
            "approval_required": approval_required,
            "action_status": action_status,
            "status": "APPROVAL_EVALUATED"
        }


approval_policy = ApprovalPolicy()