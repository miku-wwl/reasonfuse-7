"""Competition wrapper for deterministic collaboration-failure detectors."""

from __future__ import annotations

from typing import Any

from ...adapter import CompetitionAdapter
from ..common import result

SKILL_NAME = "failure_detection"


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_INPUT")
    fingerprints = payload.get("fingerprints", [])
    progress = payload.get("progress", [])
    retrieval_attempts = payload.get("retrieval_attempts")
    if not isinstance(fingerprints, list) or not isinstance(progress, list):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_TRAJECTORY")
    if retrieval_attempts is not None and not isinstance(retrieval_attempts, list):
        return result(SKILL_NAME, decision="BLOCK", reason="INVALID_RETRIEVAL_HISTORY")
    value = CompetitionAdapter.detect(fingerprints, progress, retrieval_attempts)
    return result(SKILL_NAME, decision="DETECTED" if value["detected"] else "CLEAR", **value)
