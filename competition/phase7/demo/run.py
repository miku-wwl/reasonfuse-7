"""Run the five-minute-friendly local SP-A demo."""

from __future__ import annotations

import argparse
import json

from ..scenarios.incident_recovery import IncidentRecoveryCoordinator
from .terminal import render_trace


def main() -> int:
    parser = argparse.ArgumentParser(description="ReasonFuse Phase 7 SP-A incident recovery demo")
    parser.add_argument("--fault", default="ping_pong", choices=["ping_pong", "loop", "retrieval_churn"])
    parser.add_argument("--approval", default="APPROVED", choices=["APPROVED", "DENIED"])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    report = IncidentRecoveryCoordinator().run(fault=args.fault, approval_state=args.approval)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("ReasonFuse - SP-A Collaborative Incident Recovery")
        print(f"Outcome: {report['outcome']} | success={report['success']}")
        print(render_trace(report["state"]["trace"]))
        print("\nSkill usage:", report["state"]["skill_usage"])
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
