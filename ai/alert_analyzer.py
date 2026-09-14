from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from normalizer.schema import Severity, SOCEvent


@dataclass
class AlertAnalysis:
    risk_score: int
    severity: Severity
    attack_summary: str
    findings: list[str]
    recommendations: list[str]

    def to_dict(self) -> dict:
        return {
            "risk_score": self.risk_score,
            "severity": self.severity.value,
            "attack_summary": self.attack_summary,
            "findings": self.findings,
            "recommendations": self.recommendations,
        }


class AIAlertAnalyzer:
    """Analyze SOC events and produce explainable security findings."""

    def analyze(
        self,
        events: Iterable[SOCEvent],
        risk_score: int,
    ) -> AlertAnalysis:
        events = list(events)

        if not events:
            raise ValueError("Cannot analyze an empty event set")

        attack_types = sorted(
            {
                event.attack_type
                for event in events
                if event.attack_type
            }
        )

        mitre_ids = sorted(
            {
                event.mitre_technique
                for event in events
                if event.mitre_technique
            }
        )

        sources = sorted(
            {
                event.source
                for event in events
                if event.source
            }
        )

        findings: list[str] = []
        recommendations: list[str] = []

        if "SSH_BRUTE_FORCE" in attack_types:
            findings.append(
                "Repeated SSH authentication activity indicates possible "
                "credential brute-force behavior."
            )
            recommendations.append(
                "Investigate the source IP and consider temporary blocking "
                "after validating the activity."
            )

        if len(sources) > 1:
            findings.append(
                "Multiple security telemetry sources corroborate the activity."
            )

        if mitre_ids:
            findings.append(
                f"MITRE ATT&CK techniques observed: {', '.join(mitre_ids)}."
            )

        if risk_score >= 90:
            severity = Severity.CRITICAL
        elif risk_score >= 70:
            severity = Severity.HIGH
        elif risk_score >= 40:
            severity = Severity.MEDIUM
        else:
            severity = Severity.LOW

        if not recommendations:
            recommendations.append(
                "Review the affected asset, source activity, and related logs."
            )

        attack_summary = (
            "Correlated activity involving "
            + ", ".join(attack_types or ["unknown activity"])
            + "."
        )

        return AlertAnalysis(
            risk_score=risk_score,
            severity=severity,
            attack_summary=attack_summary,
            findings=findings,
            recommendations=recommendations,
        )


if __name__ == "__main__":
    from normalizer.schema import EventType

    events = [
        SOCEvent(
            event_id="WAZUH-001",
            timestamp="2026-09-14T13:27:40+05:30",
            source="wazuh",
            event_type=EventType.AUTHENTICATION,
            severity=Severity.HIGH,
            source_ip="172.17.102.31",
            destination_ip="172.17.99.249",
            destination_port=22,
            attack_type="SSH_AUTH_FAILURE",
            mitre_technique="T1110",
        ),
        SOCEvent(
            event_id="SURI-001",
            timestamp="2026-09-14T13:27:45+05:30",
            source="suricata",
            event_type=EventType.NETWORK_ALERT,
            severity=Severity.HIGH,
            source_ip="172.17.102.31",
            destination_ip="172.17.99.249",
            destination_port=22,
            attack_type="SSH_BRUTE_FORCE",
            mitre_technique="T1110",
        ),
    ]

    analysis = AIAlertAnalyzer().analyze(events, risk_score=90)

    print(f"Risk score: {analysis.risk_score}/100")
    print(f"Severity: {analysis.severity.value}")
    print(f"Summary: {analysis.attack_summary}")

    print("Findings:")
    for finding in analysis.findings:
        print(f"  - {finding}")

    print("Recommendations:")
    for recommendation in analysis.recommendations:
        print(f"  - {recommendation}")
