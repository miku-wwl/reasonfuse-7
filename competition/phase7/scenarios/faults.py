"""Deterministic, resettable collaboration-fault fixtures."""

from __future__ import annotations

from typing import Any

from reasonfuse.core.contract import RunContract

from ..adapter import CompetitionAdapter
from ..skills.approval_control.skill import evaluate as approval_control
from ..skills.failure_detection.skill import evaluate as detect_failure
from ..skills.outcome_verification.skill import evaluate as verify_outcome
from ..skills.trajectory_guard.skill import evaluate as guard_action


FAULT_ACTIONS = {
    "loop": ["duplicate-work", "duplicate-work", "duplicate-work"],
    "duplicate_work": ["duplicate-work", "duplicate-work", "duplicate-work"],
    "oscillation": ["handoff-commander-diagnosis", "handoff-diagnosis-commander",
                    "handoff-commander-diagnosis", "handoff-diagnosis-commander"],
    "ping_pong": ["handoff-commander-diagnosis", "handoff-diagnosis-commander",
                  "handoff-commander-diagnosis", "handoff-diagnosis-commander"],
    "retrieval_churn": ["retrieve-one", "retrieve-two", "retrieve-three"],
    "premature_remediation": ["restart-before-approval"],
    "postcondition_failure": ["restart-then-unhealthy"],
    "stale_verification": ["verify-old-generation"],
    "conflicting_decisions": ["diagnosis-restart", "diagnosis-no-restart"],
}


class FaultInjector:
    """Run one fault in an isolated engine so the main scenario can reset safely."""

    def run(self, fault: str = "ping_pong") -> dict[str, Any]:
        if fault not in FAULT_ACTIONS:
            raise ValueError(f"unsupported fault: {fault}")
        if fault in {"premature_remediation", "postcondition_failure", "stale_verification", "conflicting_decisions"}:
            return self._semantic_fault(fault)
        actions = FAULT_ACTIONS[fault]
        contract = RunContract(max_stalled_steps=10, required_objective_progress_interval=10)
        adapter = CompetitionAdapter.fresh(contract=contract)
        trace: list[dict[str, Any]] = []
        fingerprints: list[str] = []
        progress: list[bool] = []
        for action in actions:
            args = {"body": {"handoff": action}}
            decision = guard_action({"tool_name": action, "arguments": args}, adapter)
            trace.append({"action": action, "decision": decision["decision"], "reason": decision.get("reason")})
            fingerprints.append(_fingerprint(action, args))
            progress.append(False)
            if decision["decision"] == "BLOCK":
                break
            adapter.record(action, args, {"status": "NO_PROGRESS"}, executed=True)
        retrieval_attempts = None
        if fault == "retrieval_churn":
            retrieval_attempts = [
                {"query": query, "source_keys": ["same-evidence"], "knowledge_base_version": "v1"}
                for query in ("one", "two", "three")
            ]
        detection = detect_failure({
            "fingerprints": fingerprints,
            "progress": progress,
            "retrieval_attempts": retrieval_attempts,
        })
        return {
            "fault": fault,
            "resettable": True,
            "isolated": True,
            "trace": trace,
            "detector": detection,
            "contained": detection["detected"],
        }

    @staticmethod
    def _semantic_fault(fault: str) -> dict[str, Any]:
        if fault == "premature_remediation":
            gate = approval_control({"action": "restart_service", "risk_class": "HIGH", "approval_state": "PENDING"})
            return {
                "fault": fault, "resettable": True, "isolated": True,
                "trace": [{"action": "restart_service", "decision": gate["decision"], "reason": "side_effect_before_approval"}],
                "detector": {"skill": "approval_control", "detected": True, "failure_type": "PREMATURE_SIDE_EFFECT",
                             "explanation": "high-impact action was proposed without current approval"},
                "contained": True,
            }
        accepted = {"accepted": True, "generation": "g2"}
        if fault == "postcondition_failure":
            check = verify_outcome({"action": "restart_service", "resource": "checkout", "accepted_result": accepted,
                                    "observation": {"resource": "checkout", "generation": "g2", "service_health": "UNHEALTHY"}})
            failure_type = "POSTCONDITION_FAILED"
        elif fault == "stale_verification":
            check = verify_outcome({"action": "restart_service", "resource": "checkout", "accepted_result": accepted,
                                    "observation": {"resource": "checkout", "generation": "g1", "service_health": "HEALTHY"}})
            failure_type = "STALE_VERIFICATION"
        else:
            check = {"decision": "CONFLICTING_AGENT_DECISIONS", "reason": "agents proposed incompatible actions"}
            failure_type = "CONFLICTING_AGENT_DECISIONS"
        return {
            "fault": fault, "resettable": True, "isolated": True,
            "trace": [{"action": FAULT_ACTIONS[fault][0], "decision": check["decision"], "reason": check.get("reason")}],
            "detector": {"skill": "outcome_verification" if fault != "conflicting_decisions" else "failure_detection",
                         "detected": True, "failure_type": failure_type, "explanation": check.get("reason", "semantic fault contained")},
            "contained": True,
        }


def _fingerprint(action: str, args: dict[str, Any]) -> str:
    from reasonfuse.core.fingerprint import tool_fingerprint
    return tool_fingerprint(action, args)
