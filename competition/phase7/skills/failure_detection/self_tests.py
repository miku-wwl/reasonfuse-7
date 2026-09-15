"""Twenty deterministic Failure Detection self-tests."""

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


def run_self_tests() -> list[dict[str, object]]:
    cases: list[tuple[str, Callable[[], None]]] = [
        ("FD-01-empty-clear", lambda: _expect([], [], "CLEAR")),
        ("FD-02-exact-loop-below-threshold", lambda: _expect(["a", "a"], [False, False], "CLEAR")),
        ("FD-03-exact-loop-at-threshold", lambda: _expect(["a", "a", "a"], [False, False, False], "DETECTED")),
        ("FD-04-exact-loop-progress-breaks", lambda: _expect(["a", "a", "a"], [False, True, False], "CLEAR")),
        ("FD-05-different-actions-clear", lambda: _expect(["a", "b", "c"], [False, False, False], "CLEAR")),
        ("FD-06-oscillation-below-window", lambda: _expect(["a", "b", "a"], [False, False, False], "CLEAR")),
        ("FD-07-oscillation-detected", lambda: _expect(["a", "b", "a", "b"], [False] * 4, "DETECTED")),
        ("FD-08-oscillation-progress-breaks", lambda: _expect(["a", "b", "a", "b"], [False, False, True, False], "CLEAR")),
        ("FD-09-same-action-not-oscillation", lambda: _expect(["a", "a", "a", "a"], [False] * 4, "DETECTED")),
        ("FD-10-retrieval-below-threshold", lambda: _retrieval(["one", "two"], False)),
        ("FD-11-retrieval-churn-detected", lambda: _retrieval(["one", "two", "three"], True)),
        ("FD-12-retrieval-new-evidence-clear", lambda: _retrieval_changed(["A"], ["A", "B"])),
        ("FD-13-retrieval-version-clear", lambda: _retrieval_version()),
        ("FD-14-query-order-does-not-matter", lambda: _retrieval_order()),
        ("FD-15-invalid-fingerprints-block", lambda: _invalid("fingerprints")),
        ("FD-16-invalid-progress-block", lambda: _invalid("progress")),
        ("FD-17-invalid-retrieval-block", lambda: _invalid("retrieval_attempts")),
        ("FD-18-ping-pong-label", lambda: _failure_type(["a", "b", "a", "b"], "OSCILLATING")),
        ("FD-19-duplicate-work-label", lambda: _failure_type(["duplicate", "duplicate", "duplicate"], "EXACT_LOOP")),
        ("FD-20-progress-history-length-mismatch-safe", lambda: _expect(["a", "a", "a"], [False], "CLEAR")),
    ]
    return [_run(case_id, check) for case_id, check in cases]


def _expect(fingerprints: list[str], progress: list[bool], decision: str) -> None:
    assert evaluate({"fingerprints": fingerprints, "progress": progress})["decision"] == decision


def _failure_type(fingerprints: list[str], failure_type: str) -> None:
    value = evaluate({"fingerprints": fingerprints, "progress": [False] * len(fingerprints)})
    assert value["failure_type"] == failure_type, value


def _retrieval(queries: list[str], expected: bool) -> None:
    attempts = [{"query": query, "source_keys": ["A"], "knowledge_base_version": "v1"} for query in queries]
    value = evaluate({"fingerprints": [], "progress": [], "retrieval_attempts": attempts})
    assert value["detected"] is expected, value


def _retrieval_changed(before: list[str], after: list[str]) -> None:
    attempts = [
        {"query": "one", "source_keys": before, "knowledge_base_version": "v1"},
        {"query": "two", "source_keys": after, "knowledge_base_version": "v1"},
        {"query": "three", "source_keys": after, "knowledge_base_version": "v1"},
    ]
    assert evaluate({"fingerprints": [], "progress": [], "retrieval_attempts": attempts})["decision"] == "CLEAR"


def _retrieval_version() -> None:
    attempts = [{"query": str(i), "source_keys": ["A"], "knowledge_base_version": f"v{i}"} for i in range(3)]
    assert evaluate({"fingerprints": [], "progress": [], "retrieval_attempts": attempts})["decision"] == "CLEAR"


def _retrieval_order() -> None:
    attempts = [
        {"query": "one", "source_keys": ["A", "B"]},
        {"query": "two", "source_keys": ["B", "A"]},
        {"query": "three", "source_keys": ["A", "B"]},
    ]
    assert evaluate({"fingerprints": [], "progress": [], "retrieval_attempts": attempts})["decision"] == "DETECTED"


def _invalid(kind: str) -> None:
    payload = {"fingerprints": [], "progress": []}
    payload[kind] = "bad"
    assert evaluate(payload)["decision"] == "BLOCK"
