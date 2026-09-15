"""Competition wrapper for deterministic objective-progress accounting."""

from __future__ import annotations

from typing import Any

from ...adapter import CompetitionAdapter
from ..common import result

SKILL_NAME = "progress_accounting"


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_INPUT")
    before = payload.get("before", {})
    after = payload.get("after", {})
    if not isinstance(before, dict) or not isinstance(after, dict):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_STATE")
    value = CompetitionAdapter.progress(
        before,
        after,
        payload.get("before_todo"),
        payload.get("after_todo"),
    )
    return result(SKILL_NAME, decision="ADVANCING" if value["objective_progress"] else "STALLED", **value)
