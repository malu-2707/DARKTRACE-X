from fastapi import APIRouter
from pydantic import BaseModel

from app.response.service import response_service
from app.response.verification import verification_service
from app.agent.reassessment import reassessment_engine
from app.audit.logger import audit_logger


router = APIRouter(prefix="/approvals", tags=["Approvals"])


class ApprovalRequest(BaseModel):
    trace_id: str
    approved: bool
    ip_address: str


@router.post("/")
async def process_approval(request: ApprovalRequest):
    if not request.approved:
        response_result = {
            "trace_id": request.trace_id,
            "action": "BLOCK_IP",
            "status": "APPROVAL_REJECTED"
        }

        verification_result = verification_service.verify(response_result)

        reassessment_result = reassessment_engine.reassess(
            verification_result
        )

        audit_result = audit_logger.log(
            reassessment_result
        )

        return {
            "trace_id": request.trace_id,
            "approval": "REJECTED",
            "response": response_result,
            "verification": verification_result,
            "reassessment": reassessment_result,
            "audit": audit_result
        }

    approval_result = {
        "trace_id": request.trace_id,
        "approval_required": False,
        "action_status": "AUTO_ALLOWED",
        "ip_address": request.ip_address,
        "status": "APPROVED"
    }

    response_result = response_service.execute(approval_result)

    verification_result = verification_service.verify(
        response_result
    )

    reassessment_result = reassessment_engine.reassess(
        verification_result
    )

    audit_result = audit_logger.log(
        reassessment_result
    )

    return {
        "trace_id": request.trace_id,
        "approval": "APPROVED",
        "response": response_result,
        "verification": verification_result,
        "reassessment": reassessment_result,
        "audit": audit_result
    }