"""Evaluate trigger recall, no-trigger precision, and routing confusion."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .trigger_router import route_intent

DATASET_PATH = Path(__file__).with_name("trigger_dataset.json")


def load_dataset() -> dict[str, Any]:
    return json.loads(DATASET_PATH.read_text(encoding="utf-8"))


def evaluate_triggers(dataset: dict[str, Any] | None = None) -> dict[str, Any]:
    dataset = dataset or load_dataset()
    positives = dataset["positives"]
    per_skill: dict[str, Any] = {}
    correct = 0
    total = 0
    confusion: dict[str, int] = {}
    for expected, examples in positives.items():
        hits = 0
        for example in examples:
            routed = route_intent(example)
            total += 1
            if routed.get("skill") == expected:
                hits += 1
                correct += 1
            else:
                key = f"{expected}->{routed.get('skill') or 'NONE'}"
                confusion[key] = confusion.get(key, 0) + 1
        per_skill[expected] = {"correct": hits, "total": len(examples),
                              "recall": hits / len(examples) if examples else 0.0}
    negatives = dataset.get("negatives", [])
    no_trigger = sum(route_intent(example).get("skill") is None for example in negatives)
    return {
        "per_skill": per_skill,
        "overall_hit_rate": correct / total if total else 0.0,
        "positive_count": total,
        "negative_count": len(negatives),
        "negative_no_trigger": no_trigger,
        "negative_precision": no_trigger / len(negatives) if negatives else 0.0,
        "confusion": confusion,
        "cross_skill_count": len(dataset.get("cross_skill", [])),
    }
