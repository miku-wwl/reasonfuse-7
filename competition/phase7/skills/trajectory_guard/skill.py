"""Competition wrapper for pre-dispatch trajectory decisions."""

from __future__ import annotations

from typing import Any

from ...adapter import CompetitionAdapter
from ..common import result

SKILL_NAME = "trajectory_guard"


def evaluate(payload: dict[str, Any], adapter: CompetitionAdapter | None = None) -> dict[str, Any]:
    """Guard one proposed tool call before it can execute."""

    if not isinstance(payload, dict):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_INPUT")
    action = payload.get("tool_name") or payload.get("action")
    if not isinstance(action, str) or not action:
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_ACTION")
    args = payload.get("arguments", payload.get("args", {}))
    adapter = adapter or CompetitionAdapter.fresh()
    return result(SKILL_NAME, **adapter.trajectory_guard(action, args))
