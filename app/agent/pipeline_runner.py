import asyncio

from app.agent.orchestrator import (
    initialize_consumer_group,
    get_next_alert,
)
from app.agent.pipeline import run_investigation
from app.realtime.websocket import connection_manager


async def process_next_alert():
    initialize_consumer_group()

    alert_message = get_next_alert()

    if alert_message is None:
        return {
            "status": "NO_ALERT"
        }

    alert = alert_message["data"]

    result = run_investigation(alert)

    await connection_manager.broadcast({
        "trace_id": alert.get("trace_id"),
        "event": "INVESTIGATION_COMPLETED",
        "status": "COMPLETED",
        "audit": result["audit"]
    })

    return {
        "status": "PROCESSED",
        "message_id": alert_message["message_id"],
        "result": result
    }


if __name__ == "__main__":
    result = asyncio.run(process_next_alert())
    print(result)