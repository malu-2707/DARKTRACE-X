from typing import Any


SEVERITY_SCORES = {
    "LOW": 25,
    "MEDIUM": 50,
    "HIGH": 75,
    "CRITICAL": 100,
}


class ScoringEngine:
    def calculate_score(
        self,
        alert: dict[str, Any],
        correlation: dict[str, Any]
    ) -> dict[str, Any]:

        severity = str(
            alert.get("severity", "LOW")
        ).upper()

        base_score = SEVERITY_SCORES.get(
            severity,
            SEVERITY_SCORES["LOW"]
        )

        event_count = correlation.get("event_count", 0)

        correlation_bonus = min(event_count * 5, 20)

        final_score = min(
            base_score + correlation_bonus,
            100
        )

        if final_score >= 80:
            risk_level = "CRITICAL"
        elif final_score >= 60:
            risk_level = "HIGH"
        elif final_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "trace_id": correlation.get("trace_id"),
            "base_score": base_score,
            "correlation_bonus": correlation_bonus,
            "score": final_score,
            "risk_level": risk_level,
            "status": "SCORED"
        }


scoring_engine = ScoringEngine()