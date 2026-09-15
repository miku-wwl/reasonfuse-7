"""Twenty deterministic Execution Contract self-tests."""

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
        ("EC-01-default-read-allows", lambda: _expect({}, {}, False, "ALLOW")),
        ("EC-02-step-boundary-allows", lambda: _expect({"max_steps": 2}, {"step_index": 1}, False, "ALLOW")),
        ("EC-03-step-over-boundary-blocks", lambda: _expect({"max_steps": 2}, {"step_index": 2}, False, "BLOCK")),
        ("EC-04-tool-boundary-allows", lambda: _expect({"max_tool_calls": 2}, {"tool_call_count": 1}, False, "ALLOW")),
        ("EC-05-tool-over-boundary-blocks", lambda: _expect({"max_tool_calls": 2}, {"tool_call_count": 2}, False, "BLOCK")),
        ("EC-06-side-effect-reserve-fits", lambda: _expect({"max_tool_calls": 3}, {"tool_call_count": 1}, True, "ALLOW")),
        ("EC-07-side-effect-reserve-does-not-fit", lambda: _expect({"max_tool_calls": 2}, {"tool_call_count": 1}, True, "BLOCK")),
        ("EC-08-side-effect-count-budget", lambda: _expect({"max_side_effects": 1}, {"side_effect_count": 1}, True, "BLOCK")),
        ("EC-09-verification-reserve-fits", lambda: _expect({"max_tool_calls": 1}, {"tool_call_count": 0, "verification_reserve_available": True}, False, "ALLOW", verification=True)),
        ("EC-10-verification-reserve-status", lambda: _has_reserve()),
        ("EC-11-invalid-boolean-limit", lambda: _invalid({"max_steps": True})),
        ("EC-12-invalid-oscillation-limit", lambda: _invalid({"max_oscillation_cycles": 1})),
        ("EC-13-invalid-retrieval-limit", lambda: _invalid({"max_retrieval_churn": 1})),
        ("EC-14-custom-version-preserved", lambda: _version()),
        ("EC-15-large-budget-allows", lambda: _expect({"max_steps": 30, "max_tool_calls": 30}, {"step_index": 10, "tool_call_count": 10}, False, "ALLOW")),
        ("EC-16-remaining-steps-reported", lambda: _remaining("remaining_steps", 3)),
        ("EC-17-remaining-tools-reported", lambda: _remaining("remaining_tool_calls", 4)),
        ("EC-18-remaining-side-effects-reported", lambda: _remaining("remaining_side_effects", 1)),
        ("EC-19-malformed-state-blocks", lambda: _expect_state("bad")),
        ("EC-20-negative-counter-blocks", lambda: _expect_state({"step_index": -1})),
    ]
    return [_run(case_id, check) for case_id, check in cases]


def _expect(contract: dict, state: dict, side_effect: bool, decision: str, **kwargs: bool) -> None:
    value = evaluate({"contract": contract, "state": state, "side_effect": side_effect, **kwargs})
    assert value["decision"] == decision, value


def _invalid(contract: dict) -> None:
    assert evaluate({"contract": contract})["decision"] == "BLOCK"


def _has_reserve() -> None:
    value = evaluate({"state": {"verification_reserve_available": True}})
    assert value["verification_reserved"] is True


def _version() -> None:
    value = evaluate({"contract": {"version": "competition-v1"}})
    assert value["decision"] == "ALLOW"


def _remaining(key: str, expected: int) -> None:
    value = evaluate({"contract": {"max_steps": 4, "max_tool_calls": 5}, "state": {"step_index": 1, "tool_call_count": 1}})
    assert value[key] == expected, value


def _expect_state(state: object) -> None:
    value = evaluate({"state": state})
    assert value["decision"] == "BLOCK"
