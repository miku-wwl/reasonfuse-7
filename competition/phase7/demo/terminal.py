"""Small terminal renderer for collaboration and ReasonFuse decisions."""

from __future__ import annotations

from typing import Any, Iterable


def render_trace(trace: Iterable[dict[str, Any]]) -> str:
    lines = ["SEQ | AGENT                | EVENT                  | SKILL                 | DECISION"]
    lines.append("----+----------------------+------------------------+-----------------------+---------")
    for item in trace:
        lines.append("{sequence:>3} | {agent_role:<20} | {event:<22} | {skill:<19} | {decision}".format(
            sequence=item.get("sequence", ""),
            agent_role=str(item.get("agent_role", ""))[:20],
            event=str(item.get("event", ""))[:22],
            skill=str(item.get("skill", "-"))[:21],
            decision=item.get("decision", item.get("outcome", "-")),
        ))
    return "\n".join(lines)
