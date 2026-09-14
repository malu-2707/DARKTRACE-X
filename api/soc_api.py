from __future__ import annotations

from typing import Any

from fastapi import FastAPI

from ai.alert_analyzer import AIAlertAnalyzer
from incidents.incident_manager import IncidentManager
from normalizer.schema import EventType, Severity, SOCEvent
from risk.risk_scorer import RiskScorer

app = FastAPI(
    title="DARKTRACE-X SOC API",
    version="1.0.0",
    description="Security Operations Center alert analysis API.",
)

risk_scorer = RiskScorer()
incident_manager = IncidentManager()
analyzer = AIAlertAnalyzer()


def build_demo_events() -> list[SOCEvent]:
    return [
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


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "DARKTRACE-X SOC API",
        "status": "online",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }


@app.get("/api/incidents")
def get_incidents() -> dict[str, Any]:
    events = build_demo_events()

    risk_score = max(
        risk_scorer.calculate(event)
        for event in events
    )

    incident = incident_manager.create_incident(
        events,
        risk_score=risk_score,
    )

    analysis = analyzer.analyze(
        events,
        risk_score=risk_score,
    )

    return {
        "incident": incident.to_dict(),
        "analysis": analysis.to_dict(),
    }


@app.get("/api/alerts")
def get_alerts() -> dict[str, Any]:
    events = build_demo_events()

    return {
        "count": len(events),
        "alerts": [
            {
                "event_id": event.event_id,
                "source": event.source,
                "event_type": event.event_type.value,
                "severity": event.severity.value,
                "source_ip": event.source_ip,
                "destination_ip": event.destination_ip,
                "destination_port": event.destination_port,
                "attack_type": event.attack_type,
                "mitre_technique": event.mitre_technique,
            }
            for event in events
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.soc_api:app",
        host="127.0.0.1",
        port=8001,
        reload=False,
    )
