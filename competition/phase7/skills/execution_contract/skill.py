"""Competition wrapper for bounded execution accounting."""

from __future__ import annotations

from typing import Any

from reasonfuse.core.contract import RunContract
from reasonfuse.core.engine import ReasonFuseEngine
from reasonfuse.core.state import ReasonFuseState

from ...adapter import CompetitionAdapter
from ..common import result

SKILL_NAME = "execution_contract"


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_INPUT")
    try:
        contract = RunContract.from_dict(payload.get("contract", {}))
        raw_state = payload.get("state", {})
        if not isinstance(raw_state, dict):
            return result(SKILL_NAME, decision="BLOCK", reason="INVALID_STATE")
        for name in ("step_index", "tool_call_count", "side_effect_count"):
            value = raw_state.get(name, 0)
            if type(value) is not int or value < 0:
                return result(SKILL_NAME, decision="BLOCK", reason=f"INVALID_STATE_COUNTER: {name}")
        reserve = raw_state.get("verification_reserve_available", False)
        if type(reserve) is not bool:
            return result(SKILL_NAME, decision="BLOCK", reason="INVALID_STATE_BOOLEAN")
        state = ReasonFuseState(
            step_index=raw_state.get("step_index", 0),
            tool_call_count=raw_state.get("tool_call_count", 0),
            side_effect_count=raw_state.get("side_effect_count", 0),
            verification_reserve_available=reserve,
        )
        adapter = CompetitionAdapter(ReasonFuseEngine(state=state, contract=contract))
        value = adapter.contract_status(
            side_effect=bool(payload.get("side_effect", False)),
            verification=bool(payload.get("verification", False)),
        )
        return result(SKILL_NAME, **value)
    except (TypeError, ValueError, KeyError) as exc:
        return result(SKILL_NAME, decision="BLOCK", reason=f"INVALID_CONTRACT: {exc}")
