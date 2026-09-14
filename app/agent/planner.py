from typing import Any


class InvestigationPlanner:
    def create_plan(self, alert: dict[str, Any]) -> dict[str, Any]:
        return {
            "trace_id": alert.get("trace_id"),
            "objective": "Investigate the security alert",
            "steps": [
                "collect_asset_context",
                "collect_auth_logs",
                "collect_process_context",
                "collect_network_context"
            ],
            "status": "PLANNED"
        }


planner = InvestigationPlanner()