# ReasonFuse Phase 7 — 1010 Track B / SP-A

This directory is the independent competition adapter around the frozen
`src/reasonfuse/core/` deterministic runtime. It contains six formal Skills,
an explicit trigger router, a deterministic multi-agent incident-recovery
scenario, resettable collaboration faults, a terminal trace, and one P0
acceptance command.

## Run from the repository root

```powershell
uv sync --frozen --python 3.13
python -m competition.phase7.evaluation
python -m competition.phase7.demo.run
```

The acceptance command checks:

```text
6 Skill packages
20 self-tests per Skill (120 total)
100% self-test pass rate
trigger hit rate >= 90%
all six Skills used in one SP-A E2E
fault injection and deterministic containment
approval-gated remediation
fresh outcome verification
package resource and schema presence
```

The demo is local-only and needs no Azure account or secret. Useful alternate
paths are `--fault loop`, `--fault retrieval_churn`, and `--approval DENIED`.
The denied path intentionally exits non-zero because remediation was not
authorized.

## Package contract

Each Skill has `SKILL.md`, `skill.py`, `schema.json`, an example, and a
`self_tests.py` suite with 20 named cases. `evaluation/trigger_dataset.json`
contains 20 positive examples per Skill, 30 irrelevant examples, and 20
cross-Skill examples.

The package does not claim organizer confirmation for a particular external
orchestration framework. Its local orchestration layer is intentionally small
and inspectable until that compatibility question is resolved.
