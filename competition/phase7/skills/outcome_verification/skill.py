"""Competition wrapper for fresh postcondition verification."""

from __future__ import annotations

from typing import Any

from ...adapter import CompetitionAdapter
from ..common import result

SKILL_NAME = "outcome_verification"


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_INPUT")
    action = payload.get("action")
    resource = payload.get("resource")
    accepted = payload.get("accepted_result", {})
    observation = payload.get("observation")
    if not isinstance(action, str) or not action or not isinstance(resource, str) or not resource:
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_POSTCONDITION_REQUEST")
    if not isinstance(accepted, dict):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_ACCEPTED_RESULT")
    value = CompetitionAdapter.outcome(action, accepted, observation, resource)
    return result(SKILL_NAME, decision=value["outcome"], **value, resource=resource)
