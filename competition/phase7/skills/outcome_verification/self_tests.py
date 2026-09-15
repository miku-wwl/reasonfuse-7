"""Twenty deterministic Outcome Verification self-tests."""

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
        ("OV-01-healthy-verified", lambda: _expect("HEALTHY", "OUTCOME_VERIFIED")),
        ("OV-02-unhealthy-failed", lambda: _expect("UNHEALTHY", "POSTCONDITION_FAILED")),
        ("OV-03-degraded-failed", lambda: _expect("DEGRADED", "POSTCONDITION_FAILED")),
        ("OV-04-missing-observation-unknown", lambda: _expect_observation(None, "OUTCOME_UNKNOWN")),
        ("OV-05-wrong-resource-unknown", lambda: _expect_observation({"resource": "payments", "service_health": "HEALTHY"}, "OUTCOME_UNKNOWN")),
        ("OV-06-stale-status-unknown", lambda: _expect_observation({"resource": "orders", "service_health": "HEALTHY", "status": "stale"}, "OUTCOME_UNKNOWN")),
        ("OV-07-timeout-unknown", lambda: _expect_observation({"resource": "orders", "status": "timeout"}, "OUTCOME_UNKNOWN")),
        ("OV-08-unavailable-unknown", lambda: _expect_observation({"resource": "orders", "status": "unavailable"}, "OUTCOME_UNKNOWN")),
        ("OV-09-malformed-unknown", lambda: _expect_observation({"resource": "orders", "service_health": []}, "OUTCOME_UNKNOWN")),
        ("OV-10-missing-health-unknown", lambda: _expect_observation({"resource": "orders"}, "OUTCOME_UNKNOWN")),
        ("OV-11-generation-match-verified", lambda: _expect_generation("g2", "g2", "OUTCOME_VERIFIED")),
        ("OV-12-generation-mismatch-unknown", lambda: _expect_generation("g2", "g1", "OUTCOME_UNKNOWN")),
        ("OV-13-generation-missing-unknown", lambda: _expect_generation("g2", None, "OUTCOME_UNKNOWN")),
        ("OV-14-rejected-action-unknown", lambda: _expect_accepted(False, "OUTCOME_UNKNOWN")),
        ("OV-15-accepted-202-needs-read", lambda: _expect_observation(None, "OUTCOME_UNKNOWN", accepted={"accepted": True, "status_code": 202})),
        ("OV-16-accepted-202-healthy", lambda: _expect_observation({"resource": "orders", "service_health": "HEALTHY"}, "OUTCOME_VERIFIED", accepted={"accepted": True, "status_code": 202})),
        ("OV-17-missing-action-blocks", lambda: _expect_payload({"resource": "orders", "accepted_result": {}, "observation": {}})),
        ("OV-18-missing-resource-blocks", lambda: _expect_payload({"action": "restart_service", "accepted_result": {}, "observation": {}})),
        ("OV-19-invalid-accepted-result-blocks", lambda: _expect_payload({"action": "restart_service", "resource": "orders", "accepted_result": [], "observation": {}})),
        ("OV-20-extra-noisy-fields-ignored", lambda: _expect_observation({"resource": "orders", "service_health": "HEALTHY", "request_id": "r1", "timestamp_utc": "now"}, "OUTCOME_VERIFIED")),
    ]
    return [_run(case_id, check) for case_id, check in cases]


def _payload(observation: dict | None, accepted: dict | None = None, generation: str | None = None) -> dict:
    accepted = accepted or {"accepted": True}
    if generation is not None:
        accepted = {**accepted, "generation": generation}
    return {"action": "restart_service", "resource": "orders", "accepted_result": accepted, "observation": observation}


def _expect(health: str, decision: str) -> None:
    assert evaluate(_payload({"resource": "orders", "service_health": health}))["decision"] == decision


def _expect_observation(observation: dict | None, decision: str, accepted: dict | None = None) -> None:
    assert evaluate(_payload(observation, accepted))["decision"] == decision


def _expect_generation(accepted_generation: str, observed_generation: str | None, decision: str) -> None:
    observation = {"resource": "orders", "generation": observed_generation, "service_health": "HEALTHY"}
    assert evaluate(_payload(observation, generation=accepted_generation))["decision"] == decision


def _expect_accepted(accepted: bool, decision: str) -> None:
    assert evaluate(_payload({"resource": "orders", "service_health": "HEALTHY"}, {"accepted": accepted}))["decision"] == decision


def _expect_payload(payload: dict) -> None:
    assert evaluate(payload)["decision"] == "BLOCK"
