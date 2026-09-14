from typing import Any

from app.response.firewall import firewall


class ResponseService:
    def execute(self, approval: dict[str, Any]) -> dict[str, Any]:
        trace_id = approval.get("trace_id")
        action_status = approval.get("action_status")
        ip_address = approval.get("ip_address")

        if action_status == "PENDING_APPROVAL":
            return {
                "trace_id": trace_id,
                "action": "BLOCK_IP",
                "status": "WAITING_FOR_APPROVAL"
            }

        if action_status == "AUTO_ALLOWED":
            if not ip_address:
                return {
                    "trace_id": trace_id,
                    "action": "BLOCK_IP",
                    "status": "FAILED",
                    "error": "IP address required"
                }

            firewall_result = firewall.block_ip(ip_address)

            return {
                "trace_id": trace_id,
                "action": "BLOCK_IP",
                "ip": ip_address,
                "firewall": firewall_result,
                "status": (
                    "ACTION_EXECUTED"
                    if firewall_result["status"] == "BLOCKED"
                    else "ACTION_FAILED"
                )
            }

        return {
            "trace_id": trace_id,
            "action": "NONE",
            "status": "NO_ACTION"
        }


response_service = ResponseService()