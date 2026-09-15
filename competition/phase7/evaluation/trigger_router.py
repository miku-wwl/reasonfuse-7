"""Explicit deterministic intent-to-Skill trigger router."""

from __future__ import annotations

from typing import Any

SKILL_PATTERNS: dict[str, tuple[str, ...]] = {
    "trajectory_guard": ("trajectory guard", "guard action", "validate trajectory", "before dispatch",
                         "may execute", "block proposal", "execution trajectory", "action gate",
                         "safe dispatch", "tool proposal", "trajectory check", "can this tool run",
                         "permission to run", "action fingerprint", "fuse gate", "prevent repeat action",
                         "dispatch guard", "preflight action", "guard this proposed action", "allowed to execute"),
    "progress_accounting": ("objective progress", "progress delta", "world state delta", "evidence delta",
                             "step advanced", "meaningful progress", "progress accounting", "measure progress",
                             "todo not progress", "compare before after", "progress advancement", "stalled progress",
                             "postcondition delta", "progress signal", "state change", "work advanced",
                             "progress check", "progress status", "delta analysis", "progress measurement"),
    "failure_detection": ("detect loop", "detect oscillation", "retrieval churn", "collaboration failure",
                           "runaway collaboration", "repeat pattern", "failure detector", "ping pong",
                           "stalled trajectory", "duplicate work", "fault pattern", "contain failure",
                           "failure type", "oscillation failure", "exact loop", "swarm failure",
                           "no progress failure", "diagnose loop", "collaboration deadlock", "failure analysis"),
    "execution_contract": ("execution budget", "run contract", "remaining tool budget", "max steps",
                            "step limit", "tool call allowance", "side effect budget", "verification reserve",
                            "bounded execution", "contract limit", "execution allowance", "budget status",
                            "dispatch within budget", "budget exhausted", "contract validation", "steps remaining",
                            "tool calls remaining", "resource action budget", "run limits", "bounded run"),
    "approval_control": ("request approval", "risky operation", "high impact", "human confirmation",
                          "approve restart", "approval state", "gate side effect", "permission for remediation",
                          "approve remediation", "denied action", "approval required", "operator confirmation",
                          "safety confirmation", "side effect approval", "authorization to act",
                          "confirm production change", "review risky tool", "approval control", "human-in-the-loop",
                          "confirm action"),
    "outcome_verification": ("verify outcome", "postcondition", "confirm recovery", "fresh verification",
                             "real world result", "health after restart", "outcome status", "verification read",
                             "service healthy", "did remediation work", "check recovery", "outcome verifier",
                             "generation check", "stale verification", "prove success", "result verified",
                             "postcondition failed", "fresh read", "is checkout healthy", "completion proof"),
}


def route_intent(intent: str) -> dict[str, Any]:
    if not isinstance(intent, str) or not intent.strip():
        return {"skill": None, "score": 0, "matched": [], "reason": "EMPTY_INTENT"}
    normalized = " ".join(intent.lower().split())
    scores = {skill: [pattern for pattern in patterns if pattern in normalized]
              for skill, patterns in SKILL_PATTERNS.items()}
    best_score = max((len(matches) for matches in scores.values()), default=0)
    if best_score == 0:
        return {"skill": None, "score": 0, "matched": [], "reason": "NO_MATCH"}
    winners = [skill for skill, matches in scores.items() if len(matches) == best_score]
    winner = winners[0]
    return {
        "skill": winner,
        "score": best_score,
        "matched": scores[winner],
        "ambiguous": len(winners) > 1,
        "candidates": winners,
    }
