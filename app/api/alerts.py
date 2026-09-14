from uuid import uuid4

from fastapi import APIRouter

from app.schemas.alert import AlertCreate
from app.queue.redis_client import redis_client


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.post("/")
def create_alert(alert: AlertCreate):
    trace_id = str(uuid4())

    redis_client.xadd(
        "soc_alerts",
        {
            "trace_id": trace_id,
            "event_id": alert.event_id,
            "source": alert.source,
            "source_ip": str(alert.source_ip),
            "destination_ip": str(alert.destination_ip),
            "destination_port": str(alert.destination_port or ""),
            "protocol": alert.protocol,
            "alert_type": alert.alert_type,
            "mitre_technique": alert.mitre_technique or "",
            "severity": alert.severity,
            "timestamp": alert.timestamp.isoformat()
        }
    )

    return {
        "status": "success",
        "message": "Alert ingested successfully",
        "trace_id": trace_id,
        "stream": "soc_alerts",
        "alert": alert.model_dump(mode="json")
    }


@router.get("/")
def get_alerts():
    return {
        "status": "success",
        "message": "Alerts API working",
        "alerts": []
    }


@router.get("/{alert_id}")
def get_alert(alert_id: int):
    return {
        "status": "success",
        "alert_id": alert_id,
        "message": f"Alert {alert_id} fetched"
    }