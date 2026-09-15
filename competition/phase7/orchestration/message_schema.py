"""Shared collaboration messages and deterministic runtime trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class WorkItem:
    task_id: str
    subtask_id: str
    title: str
    owner_role: str
    depends_on: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "subtask_id": self.subtask_id,
            "title": self.title,
            "owner_role": self.owner_role,
            "depends_on": list(self.depends_on),
        }


@dataclass(frozen=True)
class CollaborationMessage:
    collaboration_id: str
    task_id: str
    subtask_id: str
    agent_role: str
    kind: str
    payload: dict[str, Any]
    handoff_from: str | None = None
    handoff_to: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "collaboration_id": self.collaboration_id,
            "task_id": self.task_id,
            "subtask_id": self.subtask_id,
            "agent_role": self.agent_role,
            "kind": self.kind,
            "payload": self.payload,
            "handoff_from": self.handoff_from,
            "handoff_to": self.handoff_to,
        }


@dataclass
class CollaborationState:
    intent: str
    collaboration_id: str = field(default_factory=lambda: f"collab-{uuid4().hex[:8]}")
    status: str = "RECEIVED"
    trace: list[dict[str, Any]] = field(default_factory=list)
    skill_usage: dict[str, int] = field(default_factory=dict)
    shared: dict[str, Any] = field(default_factory=dict)

    def emit(self, event: str, *, task_id: str = "root", subtask_id: str = "root",
             agent_role: str = "Incident Commander", **data: Any) -> dict[str, Any]:
        item = {
            "sequence": len(self.trace) + 1,
            "event": event,
            "collaboration_id": self.collaboration_id,
            "task_id": task_id,
            "subtask_id": subtask_id,
            "agent_role": agent_role,
            **data,
        }
        self.trace.append(item)
        return item

    def use(self, skill: str) -> None:
        self.skill_usage[skill] = self.skill_usage.get(skill, 0) + 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent,
            "collaboration_id": self.collaboration_id,
            "status": self.status,
            "trace": list(self.trace),
            "skill_usage": dict(self.skill_usage),
            "shared": dict(self.shared),
        }
