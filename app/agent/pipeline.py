from typing import Any

from app.agent.planner import planner
from app.agent.evidence_selector import evidence_selector
from app.evidence.collector import evidence_collector
from app.agent.correlation_engine import correlation_engine
from app.agent.scoring_engine import scoring_engine
from app.agent.decision_engine import decision_engine
from app.policy.risk_policy import risk_policy_gate
from app.policy.approval_policy import approval_policy
from app.response.service import response_service
from app.response.verification import verification_service
from app.agent.reassessment import reassessment_engine
from app.audit.logger import audit_logger


def run_investigation(alert: dict[str, Any]) -> dict[str, Any]:
    plan = planner.create_plan(alert)

    selected_evidence = evidence_selector.select(plan)

    collected_evidence = evidence_collector.collect(
        selected_evidence
    )

    correlation = correlation_engine.correlate(
        collected_evidence
    )

    scoring = scoring_engine.calculate_score(
        alert,
        correlation
    )

    decision = decision_engine.decide(scoring)

    policy = risk_policy_gate.evaluate(decision)

    approval = approval_policy.evaluate(policy)

    response = response_service.execute(approval)

    verification = verification_service.verify(response)

    reassessment = reassessment_engine.reassess(
        verification
    )

    audit = audit_logger.log(reassessment)

    return {
        "alert": alert,
        "plan": plan,
        "selected_evidence": selected_evidence,
        "collected_evidence": collected_evidence,
        "correlation": correlation,
        "scoring": scoring,
        "decision": decision,
        "policy": policy,
        "approval": approval,
        "response": response,
        "verification": verification,
        "reassessment": reassessment,
        "audit": audit
    }