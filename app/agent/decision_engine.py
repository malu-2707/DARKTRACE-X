from typing import Any


class DecisionEngine:
    def decide(self, scoring: dict[str, Any]) -> dict[str, Any]:
        score = scoring.get("score", 0)
        risk_level = scoring.get("risk_level", "LOW")

        if score >= 80:
            decision = "RESPOND"
        elif score >= 60:
            decision = "REVIEW"
        else:
            decision = "MONITOR"

        return {
            "trace_id": scoring.get("trace_id"),
            "score": score,
            "risk_level": risk_level,
            "decision": decision,
            "status": "DECIDED"
        }


decision_engine = DecisionEngine()