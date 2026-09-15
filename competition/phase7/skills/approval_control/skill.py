"""Platform-native approval decision adapter for high-impact actions."""

from __future__ import annotations

from typing import Any

from ...adapter import CompetitionAdapter
from ..common import result

SKILL_NAME = "approval_control"


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_INPUT")
    action = payload.get("action") or payload.get("tool_name")
    risk_class = payload.get("risk_class", "LOW")
    if not isinstance(action, str) or not action:
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_ACTION")
    if not isinstance(risk_class, str):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_RISK_CLASS")
    value = CompetitionAdapter.approval(action, risk_class.strip().upper(), payload.get("approval_state"))
    return result(SKILL_NAME, **value)
