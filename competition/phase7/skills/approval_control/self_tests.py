"""Twenty deterministic Approval Control self-tests."""

from __future__ import annotations

from typing import Callable

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
        ("AC-01-low-not-required", lambda: _expect("LOW", None, "NOT_REQUIRED")),
        ("AC-02-medium-not-required", lambda: _expect("MEDIUM", "PENDING", "NOT_REQUIRED")),
        ("AC-03-high-pending-required", lambda: _expect("HIGH", "PENDING", "APPROVAL_REQUIRED")),
        ("AC-04-high-missing-required", lambda: _expect("HIGH", None, "APPROVAL_REQUIRED")),
        ("AC-05-high-approved", lambda: _expect("HIGH", "APPROVED", "APPROVED")),
        ("AC-06-high-denied", lambda: _expect("HIGH", "DENIED", "DENIED")),
        ("AC-07-critical-approved", lambda: _expect("CRITICAL", "APPROVED", "APPROVED")),
        ("AC-08-critical-stale-required", lambda: _expect("CRITICAL", "STALE", "APPROVAL_REQUIRED")),
        ("AC-09-lowercase-risk-normalized", lambda: _expect(" high ", "approved", "APPROVED")),
        ("AC-10-lowercase-denial-normalized", lambda: _expect("HIGH", " denied ", "DENIED")),
        ("AC-11-unknown-state-required", lambda: _expect("HIGH", "MAYBE", "APPROVAL_REQUIRED")),
        ("AC-12-empty-action-blocks", lambda: _expect_action("")),
        ("AC-13-missing-action-blocks", lambda: _expect_payload({"risk_class": "HIGH"})),
        ("AC-14-invalid-payload-blocks", lambda: _expect_payload([])),
        ("AC-15-nonstring-risk-blocks", lambda: _expect_payload({"action": "x", "risk_class": 1})),
        ("AC-16-tool-name-alias", lambda: _expect_payload({"tool_name": "restart_service", "risk_class": "HIGH"}, "APPROVAL_REQUIRED")),
        ("AC-17-high-is-case-insensitive", lambda: _expect("HIGH", "approved", "APPROVED")),
        ("AC-18-read-approval-is-ignored", lambda: _expect("LOW", "DENIED", "NOT_REQUIRED")),
        ("AC-19-approval-is-action-specific", lambda: _action_preserved()),
        ("AC-20-no-implicit-approval", lambda: _expect("CRITICAL", "true", "APPROVAL_REQUIRED")),
    ]
    return [_run(case_id, check) for case_id, check in cases]


def _expect(risk: str, state: str | None, decision: str) -> None:
    value = evaluate({"action": "restart_service", "risk_class": risk, "approval_state": state})
    assert value["decision"] == decision, value


def _expect_action(action: str) -> None:
    assert evaluate({"action": action, "risk_class": "HIGH"})["decision"] == "BLOCK"


def _expect_payload(payload: object, decision: str = "BLOCK") -> None:
    assert evaluate(payload)["decision"] == decision


def _action_preserved() -> None:
    value = evaluate({"action": "rotate_key", "risk_class": "HIGH"})
    assert value["action"] == "rotate_key"
