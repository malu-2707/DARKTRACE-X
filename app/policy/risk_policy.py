from typing import Any


class RiskPolicyGate:
    def evaluate(self, decision: dict[str, Any]) -> dict[str, Any]:
        score = decision.get("score", 0)
        risk_level = decision.get("risk_level", "LOW")
        requested_decision = decision.get("decision", "MONITOR")

        if score >= 80 and risk_level == "CRITICAL":
            action = "REQUIRE_APPROVAL"
        elif score >= 60:
            action = "REQUIRE_APPROVAL"
        else:
            action = "MONITOR"

        return {
            "trace_id": decision.get("trace_id"),
            "score": score,
            "risk_level": risk_level,
            "requested_decision": requested_decision,
            "policy_action": action,
            "status": "POLICY_EVALUATED"
        }


risk_policy_gate = RiskPolicyGate()