from fastapi import FastAPI, WebSocket

from app.database import Base, engine
from app.models.alert import Alert
from app.models.evidence import Evidence

from app.api.alerts import router as alerts_router
from app.api.approvals import router as approvals_router

from app.realtime.websocket import connection_manager

from app.agent.pipeline import run_investigation


# Create database tables
Base.metadata.create_all(bind=engine)


# FastAPI application
app = FastAPI(
    title="Autonomous SOC Agent",
    description="Autonomous SOC investigation and response backend",
    version="1.0.0"
)


# API routers
app.include_router(alerts_router)
app.include_router(approvals_router)


# Root endpoint
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Autonomous SOC Agent Backend is running"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Investigation E2E endpoint
@app.post("/investigation/run")
async def run_investigation_endpoint(alert: dict):
    result = run_investigation(alert)

    await connection_manager.broadcast({
        "trace_id": alert.get("trace_id"),
        "event": "INVESTIGATION_COMPLETED",
        "status": "COMPLETED",
        "audit": result["audit"]
    })

    return result


# WebSocket dashboard endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except Exception:
        connection_manager.disconnect(websocket)


# Dashboard broadcast test
@app.post("/dashboard/test-broadcast")
async def test_broadcast():
    message = {
        "trace_id": "TEST-DASHBOARD-001",
        "event": "AUDIT_RECORDED",
        "status": "RECORDED"
    }

    await connection_manager.broadcast(message)

    return {
        "status": "success",
        "message": "Broadcast sent"
    }