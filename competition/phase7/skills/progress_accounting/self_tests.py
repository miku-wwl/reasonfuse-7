"""Twenty deterministic Progress Accounting self-tests."""

from __future__ import annotations

from typing import Callable

from ...adapter import CompetitionAdapter
from ..common import passed
from .skill import evaluate


def _run(case_id: str, check: Callable[[], None]) -> dict[str, object]:
    try:
        check()
        return passed(case_id)
    except Exception as exc:  # pragma: no cover
        return {"case_id": case_id, "passed": False, "detail": f"{type(exc).__name__}: {exc}"}


def _progress(before: dict, after: dict, **kwargs: dict) -> dict:
    return evaluate({"before": before, "after": after, **kwargs})


def run_self_tests() -> list[dict[str, object]]:
    cases: list[tuple[str, Callable[[], None]]] = [
        ("PA-01-new-evidence", lambda: _expect_progress({}, {"evidence_keys": ["A"]}, True)),
        ("PA-02-duplicate-evidence", lambda: _expect_progress({"evidence_keys": ["A"]}, {"evidence_keys": ["A"]}, False)),
        ("PA-03-world-change", lambda: _expect_progress({"world_state": {"service_health": "UNHEALTHY"}}, {"world_state": {"service_health": "HEALTHY"}}, True)),
        ("PA-04-world-unchanged", lambda: _expect_progress({"world_state": {"service_health": "HEALTHY"}}, {"world_state": {"service_health": "HEALTHY"}}, False)),
        ("PA-05-new-retrieval", lambda: _expect_progress({}, {"retrieval": {"source_keys": ["A"], "knowledge_base_version": "v1"}}, True)),
        ("PA-06-same-retrieval", lambda: _expect_progress({"retrieval": {"source_keys": ["A"]}}, {"retrieval": {"source_keys": ["A"]}}, False)),
        ("PA-07-todo-only-not-objective", lambda: _expect_todo_only()),
        ("PA-08-postcondition-is-not-fabricated", lambda: _expect_progress({}, {"postcondition": {"status": "verified"}}, False)),
        ("PA-09-mixed-delta", lambda: _expect_progress({"evidence_keys": ["A"]}, {"evidence_keys": ["A", "B"], "world_state": {"service_health": "HEALTHY"}}, True)),
        ("PA-10-empty-observation", lambda: _expect_progress({"evidence_keys": ["A"]}, {}, False)),
        ("PA-11-noisy-world-fields", lambda: _expect_progress({"world_state": {"service_health": "HEALTHY", "request_id": "1"}}, {"world_state": {"service_health": "HEALTHY", "request_id": "2"}}, False)),
        ("PA-12-world-array-order-is-stable", lambda: _expect_progress({"world_state": {"dependency_health": ["a", "b"]}}, {"world_state": {"dependency_health": ["a", "b"]}}, False)),
        ("PA-13-retrieval-order-is-stable", lambda: _expect_progress({"retrieval": {"source_keys": ["A", "B"]}}, {"retrieval": {"source_keys": ["B", "A"]}}, False)),
        ("PA-14-knowledge-version-change", lambda: _expect_progress({"retrieval": {"source_keys": ["A"], "knowledge_base_version": "v1"}}, {"retrieval": {"source_keys": ["A"], "knowledge_base_version": "v2"}}, True)),
        ("PA-15-world-field-addition", lambda: _expect_progress({"world_state": {"service_health": "HEALTHY"}}, {"world_state": {"service_health": "HEALTHY", "generation": "g2"}}, True)),
        ("PA-16-null-snapshots-default", lambda: _expect_progress({}, {}, False)),
        ("PA-17-retrieval-new-source", lambda: _expect_progress({"retrieval": {"source_keys": ["A"]}}, {"retrieval": {"source_keys": ["A", "B"]}}, True)),
        ("PA-18-todo-delta-is-reported", lambda: _expect_todo_signal()),
        ("PA-19-invalid-before-blocks", lambda: _expect(evaluate({"before": [], "after": {}}), "BLOCK")),
        ("PA-20-invalid-after-blocks", lambda: _expect(evaluate({"before": {}, "after": []}), "BLOCK")),
    ]
    return [_run(case_id, check) for case_id, check in cases]


def _expect_progress(before: dict, after: dict, expected: bool) -> None:
    assert _progress(before, after)["objective_progress"] is expected


def _expect_todo_only() -> None:
    value = _progress({}, {}, before_todo={"status": "OPEN"}, after_todo={"status": "DONE"})
    assert value["signals"]["todo_delta"] is True
    assert value["objective_progress"] is False


def _expect_todo_signal() -> None:
    value = _progress({"evidence_keys": ["A"]}, {"evidence_keys": ["A"]}, before_todo={"x": 1}, after_todo={"x": 2})
    assert value["decision"] == "STALLED"
    assert value["signals"]["todo_delta"] is True


def _expect(value: dict[str, object], decision: str) -> None:
    assert value["decision"] == decision, value
