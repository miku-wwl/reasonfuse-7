"""Shared result helpers for the six thin Skill adapters."""

from __future__ import annotations

from typing import Any


def result(skill: str, *, decision: str, **data: Any) -> dict[str, Any]:
    return {"skill": skill, "decision": decision, **data}


def passed(case_id: str, detail: str = "") -> dict[str, Any]:
    return {"case_id": case_id, "passed": True, "detail": detail}
