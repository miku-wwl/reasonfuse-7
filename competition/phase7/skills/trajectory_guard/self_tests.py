"""Twenty deterministic Trajectory Guard self-tests."""

from __future__ import annotations

from typing import Callable

from reasonfuse.core.contract import RunContract
from reasonfuse.core.engine import ReasonFuseEngine
from reasonfuse.core.state import ReasonFuseState

from ...adapter import CompetitionAdapter
from ..common import passed
from .skill import evaluate


def _run(case_id: str, check: Callable[[], None]) -> dict[str, object]:
    try:
        check()
        return passed(case_id)
    except Exception as exc:  # pragma: no cover - reported by acceptance harness
        return {"case_id": case_id, "passed": False, "detail": f"{type(exc).__name__}: {exc}"}


def run_self_tests() -> list[dict[str, object]]:
    cases: list[tuple[str, Callable[[], None]]] = []

    cases.append(("TG-01-first-action-allows", lambda: _expect(evaluate({"tool_name": "diagnose", "arguments": {}}), "ALLOW")))
    cases.append(("TG-02-empty-action-blocks", lambda: _expect(evaluate({"tool_name": "", "arguments": {}}), "BLOCK")))
    cases.append(("TG-03-missing-action-blocks", lambda: _expect(evaluate({}), "BLOCK")))
    cases.append(("TG-04-invalid-payload-blocks", lambda: _expect(evaluate([]), "BLOCK")))
    cases.append(("TG-05-contained-state-blocks", lambda: _expect(evaluate({"tool_name": "diagnose"}, CompetitionAdapter(ReasonFuseEngine(state=ReasonFuseState(contained=True, fuse_reason="NO_PROGRESS")))), "BLOCK")))
    cases.append(("TG-06-containment-reason-preserved", lambda: _expect_reason("NO_PROGRESS")))
    cases.append(("TG-07-different-actions-allow", lambda: _different_actions()))
    cases.append(("TG-08-dict-order-fingerprint-stable", lambda: _same_fingerprint()))
    cases.append(("TG-09-array-order-fingerprint-sensitive", lambda: _different_fingerprint()))
    cases.append(("TG-10-side-effect-budget-blocks", lambda: _expect(evaluate({"tool_name": "restart_service"}, CompetitionAdapter(ReasonFuseEngine(state=ReasonFuseState(side_effect_count=1)))), "BLOCK")))
    cases.append(("TG-11-verification-reserve-allows-read", lambda: _verification_reserve()))
    cases.append(("TG-12-tool-budget-reserves-read", lambda: _expect(evaluate({"tool_name": "restart_service", "arguments": {"service_name": "orders"}}, CompetitionAdapter.fresh(contract=RunContract(max_tool_calls=1))), "BLOCK")))
    cases.append(("TG-13-step-budget-reserves-read", lambda: _expect(evaluate({"tool_name": "restart_service", "arguments": {"service_name": "orders"}}, CompetitionAdapter.fresh(contract=RunContract(max_steps=1))), "BLOCK")))
    cases.append(("TG-14-disabled-mode-allows", lambda: _expect(evaluate({"tool_name": "repeat"}, CompetitionAdapter(ReasonFuseEngine(state=ReasonFuseState(reasonfuse_enabled=False)))), "ALLOW")))
    cases.append(("TG-15-nested-body-accepted", lambda: _expect(evaluate({"tool_name": "restart_service", "arguments": {"body": {"service_name": "orders"}}}), "ALLOW")))
    cases.append(("TG-16-args-alias-accepted", lambda: _expect(evaluate({"action": "diagnose", "args": {}}), "ALLOW")))
    cases.append(("TG-17-unicode-action-accepted", lambda: _expect(evaluate({"tool_name": "诊断", "arguments": {}}), "ALLOW")))
    cases.append(("TG-18-fingerprint-returned", lambda: _has_value(evaluate({"tool_name": "diagnose", "arguments": {}}), "fingerprint")))
    cases.append(("TG-19-blocked-proposal-counts", lambda: _blocked_count()))
    cases.append(("TG-20-core-state-remains-bounded", lambda: _bounded_history()))
    return [_run(case_id, check) for case_id, check in cases]


def _expect(value: dict[str, object], decision: str) -> None:
    assert value["decision"] == decision, value


def _expect_reason(reason: str) -> None:
    adapter = CompetitionAdapter(ReasonFuseEngine(state=ReasonFuseState(contained=True, fuse_reason=reason)))
    assert evaluate({"tool_name": "diagnose"}, adapter)["reason"] == reason


def _different_actions() -> None:
    adapter = CompetitionAdapter.fresh()
    assert evaluate({"tool_name": "a"}, adapter)["decision"] == "ALLOW"
    adapter.record("a", {}, {"evidence_keys": ["a"]}, executed=True)
    assert evaluate({"tool_name": "b"}, adapter)["decision"] == "ALLOW"


def _same_fingerprint() -> None:
    a = evaluate({"tool_name": "x", "arguments": {"b": 2, "a": 1}})
    b = evaluate({"tool_name": "x", "arguments": {"a": 1, "b": 2}})
    assert a["fingerprint"] == b["fingerprint"]


def _different_fingerprint() -> None:
    a = evaluate({"tool_name": "x", "arguments": {"items": [1, 2]}})
    b = evaluate({"tool_name": "x", "arguments": {"items": [2, 1]}})
    assert a["fingerprint"] != b["fingerprint"]


def _verification_reserve() -> None:
    adapter = CompetitionAdapter.fresh()
    adapter.record("restart_service", {"service_name": "orders"}, {"accepted": True, "generation": "g1"}, executed=True, side_effect=True)
    _expect(evaluate({"tool_name": "service_status", "arguments": {"service_name": "orders"}}, adapter), "ALLOW")


def _has_value(value: dict[str, object], key: str) -> None:
    assert isinstance(value.get(key), str) and value[key]


def _blocked_count() -> None:
    state = ReasonFuseState(contained=True, fuse_reason="EXACT_LOOP")
    adapter = CompetitionAdapter(ReasonFuseEngine(state=state))
    _expect(evaluate({"tool_name": "x"}, adapter), "BLOCK")
    assert state.blocked_proposal_count == 1


def _bounded_history() -> None:
    adapter = CompetitionAdapter.fresh()
    for index in range(40):
        adapter.record("read", {"index": index}, {"evidence_keys": [str(index)]}, executed=True)
    assert len(adapter.engine.state.recent_actions) <= 32
