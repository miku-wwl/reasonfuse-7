"""Unified multi-agent production-incident recovery scenario."""

from __future__ import annotations

from typing import Any

from reasonfuse.core.contract import RunContract

from ..adapter import CompetitionAdapter
from ..orchestration.message_schema import CollaborationState
from ..orchestration.planner import decompose_intent
from ..orchestration.roles import role_roster
from ..skills.approval_control.skill import evaluate as approval_control
from ..skills.execution_contract.skill import evaluate as execution_contract
from ..skills.failure_detection.skill import evaluate as failure_detection
from ..skills.outcome_verification.skill import evaluate as outcome_verification
from ..skills.progress_accounting.skill import evaluate as progress_accounting
from ..skills.trajectory_guard.skill import evaluate as trajectory_guard
from .faults import FaultInjector


class IncidentRecoveryCoordinator:
    """Execute the inspectable SP-A pipeline against a resettable fixture."""

    def __init__(self, *, contract: RunContract | None = None) -> None:
        self.contract = contract or RunContract()

    def run(self, intent: str = "Restore checkout health safely", *, fault: str = "ping_pong",
            approval_state: str = "APPROVED") -> dict[str, Any]:
        state = CollaborationState(intent=intent)
        adapter = CompetitionAdapter.fresh(contract=self.contract)
        state.emit("INTENT_RECEIVED", payload={"intent": intent})
        plan = decompose_intent(intent)
        state.shared["plan"] = [item.to_dict() for item in plan]
        state.status = "PLANNED"
        state.emit("TASK_DECOMPOSED", payload={"items": state.shared["plan"]})
        state.emit("ROLES_ASSIGNED", payload={"roles": role_roster()})

        diagnosis_args = {"body": {"service_name": "checkout", "query": "checkout health"}}
        diagnosis_guard = trajectory_guard({"tool_name": "diagnostic_read", "arguments": diagnosis_args}, adapter)
        state.use("trajectory_guard")
        state.emit("ACTION_GUARDED", task_id="incident-recovery", subtask_id="diagnose",
                   agent_role="Diagnosis Agent", **diagnosis_guard)
        diagnosis_result = {
            "evidence_keys": ["checkout-health-observation"],
            "world_state": {"service_name": "checkout", "service_health": "UNHEALTHY", "generation": "g1"},
            "status": "DEGRADED",
        }
        before_diagnosis = {"world_state": dict(adapter.engine.state.world_state_snapshot)}
        adapter.record("diagnostic_read", diagnosis_args, diagnosis_result, executed=True)
        progress_result = progress_accounting({"before": before_diagnosis, "after": diagnosis_result})
        state.use("progress_accounting")
        state.emit("DIAGNOSIS_OBSERVED", task_id="incident-recovery", subtask_id="diagnose",
                   agent_role="Diagnosis Agent", **progress_result)
        state.shared["incident"] = diagnosis_result
        state.emit("HANDOFF", task_id="incident-recovery", subtask_id="diagnose",
                   agent_role="Diagnosis Agent", handoff_from="Diagnosis Agent", handoff_to="Incident Commander",
                   payload={"evidence": diagnosis_result["evidence_keys"]})

        fault_result = FaultInjector().run(fault)
        state.use("failure_detection")
        state.emit("FAULT_INJECTED", task_id="incident-recovery", subtask_id="stress-test",
                   agent_role="Incident Commander", **fault_result)
        state.shared["fault"] = fault_result
        state.emit("CONTAINMENT_RESET", task_id="incident-recovery", subtask_id="stress-test",
                   agent_role="Incident Commander", payload={"reason": fault_result["detector"].get("failure_type"), "isolated": True})

        contract_result = execution_contract({
            "contract": self.contract.to_dict(),
            "state": {
                "step_index": adapter.engine.state.step_index,
                "tool_call_count": adapter.engine.state.tool_call_count,
                "side_effect_count": adapter.engine.state.side_effect_count,
                "verification_reserve_available": adapter.engine.state.verification_reserve_available,
            },
            "side_effect": True,
        })
        state.use("execution_contract")
        state.emit("CONTRACT_CHECKED", task_id="incident-recovery", subtask_id="remediate",
                   agent_role="Operations Agent", **contract_result)
        if contract_result["decision"] != "ALLOW":
            return self._finish(state, success=False, outcome="BUDGET_EXHAUSTED")

        approval_pending = approval_control({"action": "restart_service", "risk_class": "HIGH", "approval_state": "PENDING"})
        state.use("approval_control")
        state.emit("APPROVAL_REQUESTED", task_id="incident-recovery", subtask_id="remediate",
                   agent_role="Operations Agent", **approval_pending)
        approval = approval_control({"action": "restart_service", "risk_class": "HIGH", "approval_state": approval_state})
        state.use("approval_control")
        state.emit("APPROVAL_RESOLVED", task_id="incident-recovery", subtask_id="remediate",
                   agent_role="Incident Commander", **approval)
        if approval["decision"] != "APPROVED":
            return self._finish(state, success=False, outcome="APPROVAL_NOT_GRANTED")

        action_args = {"body": {"service_name": "checkout"}}
        action_guard = trajectory_guard({"tool_name": "restart_service", "arguments": action_args}, adapter)
        state.use("trajectory_guard")
        state.emit("ACTION_GUARDED", task_id="incident-recovery", subtask_id="remediate",
                   agent_role="Operations Agent", **action_guard)
        if action_guard["decision"] != "ALLOW":
            return self._finish(state, success=False, outcome=action_guard.get("reason", "BLOCKED"))
        accepted = {"accepted": True, "status_code": 202, "generation": "g2"}
        adapter.record("restart_service", action_args, accepted, executed=True, side_effect=True, approved=True)
        state.emit("SIDE_EFFECT_ACCEPTED", task_id="incident-recovery", subtask_id="remediate",
                   agent_role="Operations Agent", action="restart_service", accepted=True, generation="g2")

        verify_args = {"body": {"service_name": "checkout"}}
        verify_guard = trajectory_guard({"tool_name": "service_status", "arguments": verify_args}, adapter)
        state.use("trajectory_guard")
        state.emit("ACTION_GUARDED", task_id="incident-recovery", subtask_id="verify",
                   agent_role="Verification Agent", **verify_guard)
        observation = {"resource": "checkout", "generation": "g2", "service_health": "HEALTHY",
                       "world_state": {"service_name": "checkout", "service_health": "HEALTHY", "generation": "g2"}}
        before_verification = {"world_state": dict(adapter.engine.state.world_state_snapshot)}
        adapter.record("service_status", verify_args, observation, executed=True)
        progress_after_verify = progress_accounting({"before": before_verification, "after": observation})
        state.use("progress_accounting")
        state.emit("VERIFICATION_OBSERVED", task_id="incident-recovery", subtask_id="verify",
                   agent_role="Verification Agent", **progress_after_verify)
        outcome = outcome_verification({"action": "restart_service", "resource": "checkout",
                                        "accepted_result": accepted, "observation": observation})
        state.use("outcome_verification")
        adapter.engine.set_outcome(outcome)
        state.emit("OUTCOME_PUBLISHED", task_id="incident-recovery", subtask_id="verify",
                   agent_role="Verification Agent", **outcome)
        state.status = "COMPLETE" if outcome["decision"] == "OUTCOME_VERIFIED" else "FAILED"
        state.emit("MONITORING_SNAPSHOT", payload={"status": state.status, "skill_usage": state.skill_usage,
                                                     "core": adapter.engine.state.to_dict()})
        return {
            "success": state.status == "COMPLETE",
            "outcome": outcome["decision"],
            "state": state.to_dict(),
            "core_state": adapter.engine.state.to_dict(),
        }

    @staticmethod
    def _finish(state: CollaborationState, *, success: bool, outcome: str) -> dict[str, Any]:
        state.status = "COMPLETE" if success else "FAILED"
        state.emit("OUTCOME_PUBLISHED", payload={"outcome": outcome})
        return {"success": success, "outcome": outcome, "state": state.to_dict()}
