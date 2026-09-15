"""Single-command P0 acceptance harness for the Phase 7 distribution."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from ..scenarios.incident_recovery import IncidentRecoveryCoordinator
from ..scenarios.faults import FaultInjector
from .trigger_eval import evaluate_triggers

SKILL_PACKAGES = {
    "trajectory_guard": "..skills.trajectory_guard",
    "progress_accounting": "..skills.progress_accounting",
    "failure_detection": "..skills.failure_detection",
    "execution_contract": "..skills.execution_contract",
    "approval_control": "..skills.approval_control",
    "outcome_verification": "..skills.outcome_verification",
}


def _load_self_tests(skill: str) -> list[dict[str, Any]]:
    modules = {
        "trajectory_guard": "..skills.trajectory_guard.self_tests",
        "progress_accounting": "..skills.progress_accounting.self_tests",
        "failure_detection": "..skills.failure_detection.self_tests",
        "execution_contract": "..skills.execution_contract.self_tests",
        "approval_control": "..skills.approval_control.self_tests",
        "outcome_verification": "..skills.outcome_verification.self_tests",
    }
    import importlib
    module = importlib.import_module(modules[skill], __package__)
    return module.run_self_tests()


def package_inventory() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[1] / "skills"
    missing: list[str] = []
    schema_count = 0
    example_count = 0
    for skill in SKILL_PACKAGES:
        directory = root / skill
        for filename in ("SKILL.md", "skill.py", "schema.json", "examples/example.json", "self_tests.py"):
            if not (directory / filename).is_file():
                missing.append(f"{skill}/{filename}")
        try:
            json.loads((directory / "schema.json").read_text(encoding="utf-8"))
            schema_count += 1
            json.loads((directory / "examples/example.json").read_text(encoding="utf-8"))
            example_count += 1
        except (OSError, json.JSONDecodeError):
            missing.append(f"{skill}/invalid-json")
    return {"skill_count": len(SKILL_PACKAGES) - len({item.split('/')[0] for item in missing}),
            "expected_skill_count": len(SKILL_PACKAGES), "schemas": schema_count,
            "examples": example_count, "missing": missing}


def run_acceptance() -> dict[str, Any]:
    inventory = package_inventory()
    self_tests: dict[str, Any] = {}
    for skill in SKILL_PACKAGES:
        cases = _load_self_tests(skill)
        self_tests[skill] = {
            "count": len(cases),
            "passed": sum(bool(case.get("passed")) for case in cases),
            "failures": [case for case in cases if not case.get("passed")],
        }
    all_self_tests = all(item["count"] >= 20 and item["passed"] == item["count"]
                         for item in self_tests.values())
    trigger = evaluate_triggers()
    e2e = IncidentRecoveryCoordinator().run()
    fault_names = ("loop", "ping_pong", "retrieval_churn", "premature_remediation",
                   "postcondition_failure", "stale_verification", "conflicting_decisions")
    fault_matrix = {name: FaultInjector().run(name) for name in fault_names}
    trace = e2e.get("state", {}).get("trace", [])
    used = set(e2e.get("state", {}).get("skill_usage", {}))
    required_events = {"TASK_DECOMPOSED", "ROLES_ASSIGNED", "FAULT_INJECTED", "APPROVAL_REQUESTED",
                       "OUTCOME_PUBLISHED", "MONITORING_SNAPSHOT"}
    e2e_gate = bool(e2e.get("success") and e2e.get("outcome") == "OUTCOME_VERIFIED"
                    and used == set(SKILL_PACKAGES)
                    and required_events.issubset({event.get("event") for event in trace})
                    and e2e.get("state", {}).get("shared", {}).get("fault", {}).get("contained"))
    package_gate = inventory["skill_count"] == 6 and not inventory["missing"] and inventory["schemas"] == 6
    trigger_gate = trigger["overall_hit_rate"] >= 0.90
    fault_gate = all(item["contained"] and item["resettable"] and item["isolated"]
                     for item in fault_matrix.values())
    return {
        "package": {**inventory, "pass": package_gate},
        "self_tests": {"per_skill": self_tests, "total": sum(item["count"] for item in self_tests.values()),
                        "passed": sum(item["passed"] for item in self_tests.values()), "pass": all_self_tests},
        "triggers": {**trigger, "pass": trigger_gate},
        "faults": {"pass": fault_gate, "cases": {
            name: {"contained": item["contained"], "detected": item["detector"]["detected"],
                   "failure_type": item["detector"]["failure_type"]}
            for name, item in fault_matrix.items()
        }},
        "main_e2e": {"pass": e2e_gate, "outcome": e2e.get("outcome"), "skill_usage": e2e.get("state", {}).get("skill_usage"),
                     "trace_events": len(trace), "fault": e2e.get("state", {}).get("shared", {}).get("fault", {}).get("detector")},
        "pass": package_gate and all_self_tests and trigger_gate and fault_gate and e2e_gate,
    }


def main() -> int:
    report = run_acceptance()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
