"""Thin competition adapter over the frozen ReasonFuse deterministic core."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from reasonfuse.core.contract import RunContract
from reasonfuse.core.detectors import exact_loop, oscillation, retrieval_churn
from reasonfuse.core.engine import ReasonFuseEngine
from reasonfuse.core.fingerprint import tool_fingerprint
from reasonfuse.core.outcome import OutcomeVerifier
from reasonfuse.core.progress import result_signals
from reasonfuse.core.state import ReasonFuseState


@dataclass
class CompetitionAdapter:
    """Expose stable competition contracts without copying core logic."""

    engine: ReasonFuseEngine

    @classmethod
    def fresh(cls, *, contract: RunContract | None = None) -> "CompetitionAdapter":
        return cls(ReasonFuseEngine(contract=contract))

    def trajectory_guard(self, tool_name: str, arguments: Any) -> dict[str, Any]:
        decision = self.engine.before_dispatch(tool_name, arguments)
        return {
            "decision": "ALLOW" if decision.allow else "BLOCK",
            "reason": decision.reason,
            "fingerprint": tool_fingerprint(tool_name, arguments),
            "trajectory_state": self.engine.state.trajectory_state,
        }

    def record(self, tool_name: str, arguments: Any, result: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        observation = self.engine.record(tool_name, arguments, result, **kwargs)
        return {
            "signals": observation.signals,
            "objective_progress": observation.objective_progress,
            "trajectory_state": observation.trajectory_state,
            "progress_state": observation.progress_state,
            "fuse_reason": observation.fuse_reason,
            "executed": observation.executed,
        }

    @staticmethod
    def progress(before: dict[str, Any], after: dict[str, Any],
                 before_todo: dict[str, Any] | None = None,
                 after_todo: dict[str, Any] | None = None) -> dict[str, Any]:
        signals = result_signals(before, after, before_todo, after_todo)
        return {
            "progress_state": "ADVANCING" if signals.objective_progress else "STALLED",
            "objective_progress": signals.objective_progress,
            "signals": {
                "evidence_delta": signals.evidence_delta,
                "world_state_delta": signals.world_state_delta,
                "retrieval_delta": signals.retrieval_delta,
                "todo_delta": signals.todo_delta,
                "postcondition_delta": signals.postcondition_delta,
            },
        }

    @staticmethod
    def detect(fingerprints: list[str], progress: list[bool],
               retrieval_attempts: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        checks = [exact_loop(fingerprints, progress), oscillation(fingerprints, progress)]
        if retrieval_attempts is not None:
            checks.append(retrieval_churn(retrieval_attempts))
        hit = next((item for item in checks if item.tripped), None)
        return {
            "detected": hit is not None,
            "failure_type": hit.reason if hit else None,
            "explanation": hit.explanation if hit else "no deterministic failure pattern",
        }

    def contract_status(self, *, side_effect: bool, verification: bool = False) -> dict[str, Any]:
        state = self.engine.state
        reason = self.engine.contract.before_dispatch(
            steps=state.step_index,
            tool_calls=state.tool_call_count,
            side_effects=state.side_effect_count,
            side_effect=side_effect,
            verification=verification,
            reserve_available=state.verification_reserve_available,
        )
        return {
            "decision": "BLOCK" if reason else "ALLOW",
            "reason": reason,
            "remaining_steps": max(0, self.engine.contract.max_steps - state.step_index),
            "remaining_tool_calls": max(0, self.engine.contract.max_tool_calls - state.tool_call_count),
            "remaining_side_effects": max(0, self.engine.contract.max_side_effects - state.side_effect_count),
            "verification_reserved": state.verification_reserve_available,
        }

    @staticmethod
    def approval(proposed_action: str, risk_class: str, approval_state: str | None) -> dict[str, Any]:
        high_impact = risk_class in {"HIGH", "CRITICAL"}
        if not high_impact:
            return {"decision": "NOT_REQUIRED", "action": proposed_action, "risk_class": risk_class}
        normalized = (approval_state or "PENDING").strip().upper()
        if normalized == "APPROVED":
            return {"decision": "APPROVED", "action": proposed_action, "risk_class": risk_class}
        if normalized == "DENIED":
            return {"decision": "DENIED", "action": proposed_action, "risk_class": risk_class}
        return {"decision": "APPROVAL_REQUIRED", "action": proposed_action, "risk_class": risk_class}

    @staticmethod
    def outcome(action: str, accepted_result: dict[str, Any], observation: dict[str, Any] | None,
                resource: str) -> dict[str, Any]:
        return OutcomeVerifier().verify(action, accepted_result, observation, requested_resource=resource)


def restored_adapter(state: dict[str, Any], contract: RunContract | None = None) -> CompetitionAdapter:
    """Restore a persisted core state while retaining the original contract."""

    core_state = ReasonFuseState.from_dict(state)
    return CompetitionAdapter(ReasonFuseEngine(state=core_state, contract=contract))
