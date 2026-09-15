"""Deterministic incident plan used by the SP-A demo."""

from __future__ import annotations

from .message_schema import WorkItem


def decompose_intent(intent: str) -> list[WorkItem]:
    if not isinstance(intent, str) or not intent.strip():
        raise ValueError("intent must be a non-empty string")
    task_id = "incident-recovery"
    return [
        WorkItem(task_id, "diagnose", "Collect fresh checkout health and evidence", "Diagnosis Agent"),
        WorkItem(task_id, "stress-test", "Exercise and contain a collaboration fault", "Incident Commander", ("diagnose",)),
        WorkItem(task_id, "remediate", "Propose and execute a bounded restart", "Operations Agent", ("diagnose", "stress-test")),
        WorkItem(task_id, "verify", "Read the fresh postcondition and prove recovery", "Verification Agent", ("remediate",)),
    ]
