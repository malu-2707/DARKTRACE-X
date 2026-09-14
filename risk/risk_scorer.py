from __future__ import annotations

from normalizer.schema import Severity, SOCEvent


class RiskScorer:
    """Calculate a normalized SOC risk score from event characteristics."""

    SEVERITY_SCORE = {
        Severity.LOW: 20,
        Severity.MEDIUM: 40,
        Severity.HIGH: 70,
        Severity.CRITICAL: 90,
    }

    def calculate(self, event: SOCEvent) -> int:
        score = self.SEVERITY_SCORE.get(event.severity, 20)

        if event.mitre_technique:
            score += 5

        if event.attack_type:
            score += 5

        if event.destination_port in {22, 23, 3389}:
            score += 10

        return min(score, 100)

    def classify(self, score: int) -> Severity:
        if score >= 90:
            return Severity.CRITICAL
        if score >= 70:
            return Severity.HIGH
        if score >= 40:
            return Severity.MEDIUM
        return Severity.LOW


if __name__ == "__main__":
    from normalizer.schema import EventType

    event = SOCEvent(
        event_id="RISK-001",
        timestamp="2026-09-14T13:27:40+05:30",
        source="suricata",
        event_type=EventType.NETWORK_ALERT,
        severity=Severity.HIGH,
        source_ip="172.17.102.31",
        destination_ip="172.17.99.249",
        destination_port=22,
        attack_type="SSH_BRUTE_FORCE",
        mitre_technique="T1110",
    )

    scorer = RiskScorer()
    score = scorer.calculate(event)
    classification = scorer.classify(score)

    print(f"Risk score: {score}/100")
    print(f"Risk severity: {classification.value}")
