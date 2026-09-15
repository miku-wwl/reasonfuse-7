"""Role responsibilities for the unified production-incident scenario."""

ROLE_RESPONSIBILITIES = {
    "Incident Commander": "owns intent, plan, handoffs, and containment decisions",
    "Diagnosis Agent": "collects fresh evidence and tests the incident hypothesis",
    "Operations Agent": "proposes the bounded remediation action",
    "Verification Agent": "performs the fresh postcondition read and reports outcome",
}


def role_roster() -> list[dict[str, str]]:
    return [{"role": role, "responsibility": responsibility}
            for role, responsibility in ROLE_RESPONSIBILITIES.items()]
