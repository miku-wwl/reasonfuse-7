# ReasonFuse Phase 7 — 1010 Track B / SP-A Verification Plan

> **Phase:** 7  
> **Target:** 1010 Digital Human Festival / Global AI Agent Competition — Track B  
> **Recommended direction:** SP-A — Collaborative Orchestration Hub Skill Package  
> **Companion document:** `ReasonFuse_Phase7_1010_SP-A_Construction_Plan.md`  
> **Verification scope:** Skill completeness → self-tests → trigger evaluation → orchestration → collaboration faults → end-to-end closed loop → packaging → demo evidence → final claim audit  
> **Core rule:** **Verify the competition distribution without reopening the frozen ReasonFuse core unless a real correctness blocker is proven.**

---

# 0. Purpose

This document defines **how Phase 7 is accepted**.

The Phase 7 Construction Plan answers:

> What needs to be built for the 1010 Track B / SP-A competition version?

This document answers:

> What evidence proves that the Phase 7 competition version actually satisfies the supplied Track B / SP-A requirements?

The verification plan is intentionally stricter than a simple demo checklist.

A Phase 7 submission should prove all of the following:

```text
the six Skills exist
the six Skills are genuinely distinct
the six Skills are actually used
each Skill has ≥20 self-tests
all required self-tests pass
trigger hit rate is ≥90%
the main pipeline is end-to-end demoable
the orchestration is genuinely multi-agent
task decomposition exists
long-horizon planning exists
collaboration exists
fault injection exists
ReasonFuse actually intervenes
monitoring makes the intervention visible
the package is installable / packagable
the final story matches the evidence
```

## Current checkout profile — 2026-09-15

The current implementation under verification is the local package at
`competition/phase7/`. It is a thin adapter over the unchanged
`src/reasonfuse/core/` implementation and is executed from the repository
checkout with:

```powershell
pwsh -File scripts/run_phase7.ps1 -Mode verify
python -m competition.phase7.evaluation
python -m competition.phase7.demo.run
```

The latest local evidence is:

```text
6 / 6 Skill packages present
120 / 120 Skill self-tests PASS
overall trigger hit rate 98.33%
30 / 30 negative trigger examples correctly produced no route
7 / 7 deterministic fault fixtures contained
main E2E OUTCOME_VERIFIED
root test suite 37 / 37 PASS
```

This is local checkout evidence. It does not prove a clean independent
installation, organizer acceptance of the orchestration framework, a live
cloud/production run, swarm emergence, or official competition submission.
Those claims remain `NOT VERIFIED` or `BLOCKED` below.

---

# 1. Source-Derived Acceptance Baseline

The supplied Track B materials establish the following competition requirements.

## Track B overall

The solution must:

```text
assemble ≥6 effective Skills
use one unified scenario
be installable
be testable
be demoable
form an end-to-end closed loop
```

Core acceptance includes:

```text
Skill Count             ≥6 effective Skills
Self-test Coverage      100% pass rate
Trigger Hit Rate        ≥90%
Main Pipeline           ≥1 end-to-end demoable pipeline
Delivery Format         installable / packagable
```

---

## SP-A specific

The supplied SP-A brief asks for a collaborative orchestration hub capable of:

```text
intent understanding
task decomposition
long-horizon planning
multi-agent dispatch and coordination
adversarial gameplay simulation
swarm emergence observation
collaborative stress testing / fault injection
runtime visualization / monitoring
```

The supplied SP-A main pipeline is:

```text
Intent Input
    ↓
Task Decomposition / Planning
    ↓
Multi-Agent Division of Labor & Collaboration
    ↓
Result Completion
    ↓
Monitoring
```

The supplied materials also state:

```text
≥6 effective Skills
shared trigger-word system
shared communication / message schema
SKILL.md + supporting scripts
≥20 self-test cases per Skill
```

This verification plan treats those items as P0 unless later official organizer instructions supersede them.

---

# 2. Verification Vocabulary

Every verification item must use one of these statuses.

## PASS

The required behavior was executed and the evidence supports the claim.

## FAIL

The behavior was executed but violated the expected requirement.

## NOT VERIFIED

The behavior was not executed or the evidence is insufficient.

## BLOCKED

Verification could not proceed because of an external dependency or unresolved organizer requirement.

Examples:

```text
framework eligibility unclear
competition platform unavailable
credentials missing
runtime dependency unavailable
```

## OPTIONAL NOT RUN

Only valid for explicitly P0.5 polish items.

Do not convert:

```text
BLOCKED
NOT VERIFIED
OPTIONAL NOT RUN
```

into PASS in README, slides, video narration, or submission text.

---

# 3. Evidence Strength Levels

Use four evidence levels.

## E0 — Document / Code Presence

Example:

```text
SKILL.md exists
trigger examples are documented
```

This proves packaging presence only.

---

## E1 — Isolated Skill Execution

Example:

```text
Trajectory Guard adapter invokes the actual ReasonFuse core
and returns ALLOW/BLOCK correctly
```

This proves the Skill works independently.

---

## E2 — Integrated Collaboration Evidence

Example:

```text
the Skill is invoked inside the SP-A multi-agent scenario
with collaboration/task identifiers preserved
```

This proves integration.

---

## E3 — End-to-End Competition Evidence

Example:

```text
intent
→ task decomposition
→ multi-agent collaboration
→ injected failure
→ ReasonFuse intervention
→ approval
→ world-state change
→ fresh verification
→ monitored verified outcome
```

This is the strongest Phase 7 proof.

---

# 4. Phase 7 Verification Gates

Use these gates:

```text
P7-V0   Phase 6 Handoff / Core Freeze
P7-V1   Competition Package Structure
P7-V2   Six-Skill Contract Verification
P7-V3   Per-Skill Self-Test Verification
P7-V4   Trigger-System Verification
P7-V5   Shared Message Schema Verification
P7-V6   Planning / Task-Decomposition Verification
P7-V7   Multi-Agent Collaboration Verification
P7-V8   Collaborative Fault-Injection Verification
P7-V9   ReasonFuse Intervention Verification
P7-V10  Approval + Outcome Verification
P7-V11  Runtime Visualization / Monitoring Verification
P7-V12  Main E2E Closed-Loop Verification
P7-V13  Installability / Packaging Verification
P7-V14  Acceptance Harness Verification
P7-V15  Demo / Competition Story Verification
P7-V16  Final Claim Audit
P7-V17  Final Freeze / Submission Gate
```

P0 completion requires:

```text
P7-V0 through P7-V17
```

except clearly marked P0.5 sub-items.

Important distinction for this checkout:

```text
LOCAL_P0_ACCEPTANCE = PASS
FORMAL_P7-V0..V17_SUBMISSION_GATE = NOT VERIFIED
```

The local acceptance harness intentionally covers the executable package,
self-tests, trigger set, fault matrix, and one deterministic E2E. It does not
close the external-framework, clean-install, independent-viewer, official
submission, or final-archive gates.

---

# 5. P7-V0 — Phase 6 Handoff / Core Freeze

## Goal

Prove Phase 7 starts from a stable ReasonFuse baseline and does not silently rewrite the Microsoft submission.

## Required record

Capture the source-core SHA separately from the Phase 7 implementation SHA.
Do not label the current Phase 7 working tree as frozen until the implementation
has been reviewed, committed, and the final acceptance run has been repeated.

For the current checkout:

```text
source/core baseline: e5ba1cb79e5dbad5afd91cf4af49271fd596df7a
Phase 7 implementation: local uncommitted working tree
branch: main
core source diff: none
pre-existing plan edit: preserved and not overwritten
```

Recommended branch relationship:

```text
phase6-submitted
    ↓
phase7-1010
```

---

## Core regression baseline

Run the existing core verification suite before Phase 7 adapter work.

Expected:

```text
core unit / boundary tests PASS
local wiring PASS
history audit PASS
compileall PASS
git diff --check PASS
benchmark/15-scenarios.md: manual checklist only; execution NOT VERIFIED
```

Current evidence is `36 / 36` core tests PASS and `37 / 37` root tests PASS
when the Phase 7 acceptance test is included. The local `15-scenarios.md`
file is not an automated run and must not be reported as `15 scenarios PASS`.

## PASS

Phase 7 begins from a known-good core baseline.

## FAIL

Do not continue Phase 7 packaging if the core baseline is already broken.

---

# 6. P7-V1 — Competition Package Structure

## Goal

Prove the formal competition package exists and is complete.

Minimum expected logical structure:

```text
competition/phase7/
    skills/
        trajectory_guard/
        progress_accounting/
        failure_detection/
        execution_contract/
        approval_control/
        outcome_verification/

    orchestration/
    scenarios/
    evaluation/
    tests/
    demo/
```

Exact filesystem naming is not itself an official requirement.

The verification requirement is functional completeness.

---

## Required checks

Verify:

```text
6 Skill directories/packages exist
6 SKILL.md files exist
6 callable wrappers/adapters exist
6 input/output contracts exist
supporting implementation and self-test modules exist
examples exist
test folders exist
```

Current checkout mapping:

```text
competition/phase7/skills/<skill>/SKILL.md
competition/phase7/skills/<skill>/skill.py
competition/phase7/skills/<skill>/schema.json
competition/phase7/skills/<skill>/examples/example.json
competition/phase7/skills/<skill>/self_tests.py
competition/phase7/evaluation/acceptance.py
```

The current package check is the `package` section of
`python -m competition.phase7.evaluation`. It checks six directories, six
schemas, six examples, and required files; it does not claim a separately
published archive.

## PASS

All six formal Skills are present and inspectable.

---

# 7. P7-V2 — Six-Skill Contract Verification

The six formal Skills are:

```text
1. Trajectory Guard
2. Progress Accounting
3. Failure Detection
4. Execution Contract
5. Approval Control
6. Outcome Verification
```

Each Skill must satisfy the same contract categories.

---

## Required Skill contract

For each Skill verify:

```text
Purpose
When to Trigger
When NOT to Trigger
Inputs
Outputs
Preconditions
Deterministic Logic
Failure Modes
Example
Self-Test Coverage
Main Scenario Integration
Dependencies
Limitations
```

---

## Non-duplication check

The six Skills must be meaningfully distinct.

Fail examples:

```text
Trajectory Guard and Failure Detection expose the same behavior
Execution Contract is just renamed Trajectory Guard
Approval Control contains no approval-specific logic
Outcome Verification is only a status formatter
```

---

## Core-reuse check

Each wrapper should delegate to existing ReasonFuse logic where that logic already exists.

Preferred:

```text
Skill wrapper
    ↓
ReasonFuse core
```

Fail pattern:

```text
duplicate independent implementation
    ↓
same algorithm copied six times
```

## PASS

The six Skills are distinct, documented, and backed by real implementation.

Current implementation note: Trajectory Guard, Progress Accounting, Failure
Detection, Execution Contract, and Outcome Verification delegate to the frozen
core through `competition/phase7/adapter.py`. Approval Control is the thin
competition-facing approval-state adapter because the local package has no
native human-approval provider. That local approval model must not be presented
as production or platform-native approval evidence.

---

# 8. P7-V3 — Per-Skill Self-Test Verification

The supplied Track B materials require:

```text
≥20 self-test cases per Skill
```

Minimum Phase 7 requirement:

```text
6 Skills × 20 tests
= 120 self-tests minimum
```

---

## Test-count gate

For each Skill verify:

```text
Trajectory Guard       ≥20
Progress Accounting    ≥20
Failure Detection      ≥20
Execution Contract     ≥20
Approval Control       ≥20
Outcome Verification   ≥20
```

---

## Required test quality

Tests must not be 20 cosmetic duplicates.

Each Skill's tests should cover:

```text
happy path
negative path
boundary path
invalid input
ambiguous input
stateful edge cases where applicable
main-scenario use
```

---

## Recommended coverage themes

### Trajectory Guard

```text
valid first action
contained run
blocked follow-up
fingerprint normalization
same action / different semantically equivalent input
new action
unknown tool
```

### Progress Accounting

```text
new evidence
duplicate evidence
world-state change
no world-state change
retrieval identity change
retrieval duplicate
todo-only delta
postcondition delta
mixed signals
```

### Failure Detection

```text
exact loop
false exact-loop candidate
oscillation
false oscillation
retrieval churn
useful recheck
generic no-progress
threshold boundaries
```

### Execution Contract

```text
step limit
tool-call limit
stall limit
oscillation limit
retrieval-churn limit
side-effect limit
verification reserve
N-1 / N / N+1 boundaries
```

### Approval Control

```text
read-only no approval
high-impact approval required
approved
denied
stale approval
reused approval rejected
single execution
```

### Outcome Verification

```text
verified
failed
unknown
stale generation
wrong resource
missing observation
accepted but unverified
fresh success
```

---

## Official acceptance gate

Required result:

```text
100% self-test pass rate
```

If even one required self-test fails:

```text
Phase 7 P0 = FAIL
```

Do not hide or exclude failing tests to reach 100%.

Current execution path:

```powershell
python -m competition.phase7.evaluation
```

The acceptance harness executes `run_self_tests()` for each Skill and currently
records `120 / 120 PASS` (`20 / 20` for each Skill). The six small
`tests/test_skill.py` files assert those named cases; the acceptance harness is
the authoritative aggregate count.

---

# 9. P7-V4 — Trigger-System Verification

The supplied Track B acceptance criterion requires:

```text
Trigger Hit Rate ≥90%
```

Phase 7 must therefore verify the routing system explicitly.

---

## Trigger evaluation dataset

Recommended minimum internal dataset:

```text
positive examples per Skill        ≥20
negative / irrelevant examples     ≥20 total
cross-Skill ambiguous examples     ≥20 total
```

These dataset sizes are engineering choices, not official numbers from the supplied brief.

---

## Required categories

For every Skill include:

```text
clear positive
paraphrased positive
short command
long natural-language request
near-neighbor Skill confusion
irrelevant request
```

---

## Metrics

Compute:

```text
overall trigger hit rate
per-Skill hit rate
wrong-Skill routing count
no-trigger correctness
confusion matrix / confusion summary
```

Official gate:

```text
overall trigger hit rate ≥90%
```

Recommended internal target:

```text
≥95%
```

The 95% target is internal margin only.

---

## Trigger correctness rule

A trigger counts as correct only if:

```text
expected Skill selected
```

For a multi-Skill request:

```text
expected Skill set selected
```

if the router officially supports multi-Skill routing.

Document the evaluation policy before measuring.

Do not change the scoring rule after seeing results.

Current frozen local dataset and result:

```text
positive examples: 20 per Skill / 120 total
negative examples: 30
cross-Skill examples: 20
overall hit rate: 98.33%
negative no-trigger correctness: 30 / 30
approval_control recall: 18 / 20 (90%)
```

The current router uses deterministic normalized phrase matching and reports
the two approval-control misses in its confusion summary. This is a local
engineering evaluation, not an organizer-provided benchmark.

---

# 10. P7-V5 — Shared Message Schema Verification

SP-A requires a shared communication/message schema.

Recommended envelope fields:

```text
collaboration_id
task_id
subtask_id
agent_role
intent
objective
evidence_refs
proposed_action
expected_postcondition
status
handoff_to
```

---

## Required checks

Verify that:

```text
every participating agent can emit the schema
every participating agent can consume the schema
required IDs survive handoff
invalid schema is rejected
missing required fields are handled
unknown extra fields do not silently corrupt state
```

---

## Privacy / reasoning rule

Do not require:

```text
private chain-of-thought
hidden internal reasoning
```

inside the shared message schema.

Use:

```text
decisions
evidence
plans
actions
status
```

## PASS

Messages are interoperable across agents and traceable through one collaboration.

Current local status: the runtime trace emitted by
`competition/phase7/orchestration/message_schema.py` carries
`collaboration_id`, `task_id`, `subtask_id`, and `agent_role`; the handoff event
also carries `handoff_from` and `handoff_to`. This proves trace identity at E2
level. Formal producer/consumer validation and rejection of malformed
`CollaborationMessage` instances are not yet executed, so the full shared
message-schema gate remains `NOT VERIFIED`.

---

# 11. P7-V6 — Planning / Task-Decomposition Verification

SP-A requires:

```text
intent decomposition
long-horizon planning
```

Phase 7 must prove both exist.

---

## Fixed main goal

Recommended:

```text
Restore checkout/payment service health safely.
```

---

## Required planning output

A valid plan should contain a multi-step structure such as:

```text
1. establish current health
2. collect diagnostic evidence
3. isolate likely failure domain
4. choose remediation
5. request approval if needed
6. execute remediation
7. perform fresh verification
8. close incident
```

Exact steps may vary.

---

## Verification checks

Confirm:

```text
input intent is parsed
multiple subtasks are created
subtasks have dependencies/order where needed
roles are assigned
plan persists across collaboration
plan can be updated when new evidence arrives
replan does not erase completed evidence
```

---

## Negative test

Provide an intentionally ambiguous or incomplete goal.

Expected:

```text
planner clarifies / safely bounds scope
```

or produces a conservative plan.

It must not immediately jump to a high-impact action.

Current local status: `decompose_intent()` creates four ordered work items with
dependencies (`diagnose → stress-test → remediate → verify`) and assigns the
four role responsibilities. Dynamic re-plan, persistence after an evidence
update, and the ambiguous-goal negative test are not implemented in the local
coordinator and remain `NOT VERIFIED`.

---

# 12. P7-V7 — Multi-Agent Collaboration Verification

SP-A requires real multi-agent division of labor and collaboration.

Recommended roles:

```text
Incident Commander
Diagnosis Agent
Operations Agent
Verification Agent
```

Optional:

```text
Knowledge Agent
```

---

## Distinct-role gate

Each role must have a distinct responsibility.

Fail example:

```text
four agents all call the same tools
with different names only
```

---

## Collaboration proof

The main scenario must show at least:

```text
one task assignment
one handoff
one evidence-sharing event
one action proposal from a different role
one verification handoff
```

---

## Collaboration identity

Every action should be attributable to:

```text
collaboration_id
task_id
subtask_id
agent_role
```

---

## Result aggregation

The final result must combine outputs from multiple roles.

A single agent doing all real work while others emit decorative text does not satisfy the intended collaboration standard.

---

# 13. P7-V8 — Collaborative Fault-Injection Verification

SP-A explicitly mentions:

```text
adversarial gameplay simulation
collaborative stress testing / fault injection
```

Phase 7 must include deterministic collaboration faults.

Minimum recommended P0 set:

```text
C-ADV-001  Ping-Pong Handoff
C-ADV-002  Duplicate Retrieval Swarm
C-ADV-003  Premature Remediation
```

---

## C-ADV-001 — Ping-Pong Handoff

Trajectory:

```text
Diagnosis
→ Operations
→ Diagnosis
→ Operations
```

with no meaningful new evidence.

Expected:

```text
oscillation / no-progress recognized
ReasonFuse bounds or contains the collaboration
```

Evidence:

```text
handoff trace
progress state
failure type
containment decision
```

---

## C-ADV-002 — Duplicate Retrieval Swarm

Multiple agents issue differently worded retrievals that normalize to the same evidence.

Expected:

```text
new surface wording
but no new normalized evidence
→ retrieval churn / duplicate-work signal
```

Evidence:

```text
retrieval identities
agent roles
new-evidence count
ReasonFuse decision
```

---

## C-ADV-003 — Premature Remediation

Operations Agent proposes a high-impact remediation before sufficient diagnostic evidence.

Expected:

```text
planner/policy defers
and/or approval required
ReasonFuse does not mark the proposal itself as objective progress
```

---

## P0 gate

At least one collaboration-specific fault must appear in the final demo.

All three recommended faults should pass in the full verification suite.

Current local fault matrix extends this to seven resettable fixtures:

```text
loop                  EXACT_LOOP                 contained
ping_pong             OSCILLATING                contained
retrieval_churn       RETRIEVAL_CHURN            contained
premature_remediation PREMATURE_SIDE_EFFECT     approval-gated
postcondition_failure POSTCONDITION_FAILED      contained
stale_verification    STALE_VERIFICATION         contained
conflicting_decisions CONFLICTING_AGENT_DECISIONS contained
```

The matrix is executed by `python -m competition.phase7.evaluation`. The
retrieval fixture proves deterministic churn containment, but it does not yet
prove multiple independent retrieval agents or emergent swarm behavior; that
stronger claim remains `NOT VERIFIED`.

---

# 14. P7-V9 — ReasonFuse Intervention Verification

The competition must demonstrate that ReasonFuse is not decorative.

For at least one injected failure:

```text
ReasonFuse must materially change what happens next.
```

Valid interventions include:

```text
BLOCK a proposal
trip containment
stop repeated collaboration
reserve verification budget
require approval
mark no-progress
prevent false success
```

---

## Required evidence

Capture:

```text
before trajectory
detector/progress state
ReasonFuse decision
blocked/allowed action
after trajectory
```

---

## Fail condition

If removing ReasonFuse produces the same execution path:

```text
intervention evidence = insufficient
```

This does not mean every demo must be an OFF/ON benchmark, but the causal effect must be clear.

Current local evidence: the ping-pong fixture reaches a core
`OSCILLATING` block before the fourth handoff, and the duplicate-work fixture
reaches an `EXACT_LOOP` block before the third duplicate action. The same run
also demonstrates the verification reserve and approval gate. A controlled
ReasonFuse-OFF comparison has not been run, so a formal causal OFF/ON
comparison remains `NOT VERIFIED`; the allowed wording is “deterministic local
intervention observed.”

---

# 15. P7-V10 — Approval + Outcome Verification

This gate reuses the strongest Phase 6 proof but inside the multi-agent scenario.

Required flow:

```text
Operations Agent proposes restart_service
        ↓
Approval Control
        ↓
APPROVAL_REQUIRED
        ↓
human/platform approval
        ↓
side effect executes
        ↓
accepted
        ↓
NOT SUCCESS YET
        ↓
Verification Agent performs fresh read
        ↓
Outcome Verification
        ↓
OUTCOME_VERIFIED / POSTCONDITION_FAILED / OUTCOME_UNKNOWN
```

---

## Required P0 branches

### Success

```text
accepted
→ fresh observation
→ OUTCOME_VERIFIED
```

### Failure or Unknown

At least one of:

```text
POSTCONDITION_FAILED
OUTCOME_UNKNOWN
```

must be demonstrated in the verification suite.

---

## Important rule

The Verification Agent must not simply trust the Operations Agent's own statement.

Fresh evidence must determine the outcome.

Current local evidence covers both branches. The main run records
`APPROVAL_REQUIRED`, then consumes an explicitly supplied `APPROVED` state,
accepts a `202` restart, performs a fresh `g2` checkout read, and publishes
`OUTCOME_VERIFIED`. Skill self-tests cover `POSTCONDITION_FAILED` and
`OUTCOME_UNKNOWN`; `--approval DENIED` demonstrates a non-success branch. The
approval value is a local enum supplied to the demo, not evidence of a native
human-approval provider.

---

# 16. P7-V11 — Runtime Visualization / Monitoring Verification

SP-A asks for runtime visualization and monitoring.

P0 does not require a large dashboard.

A compact trace is sufficient if it is clear.

Recommended judge-facing columns:

```text
Time
Agent
Subtask
Action
ReasonFuse Skill
Decision
Progress
Outcome
```

---

## Required visibility

A judge should be able to see:

```text
who acted
what subtask was active
what was proposed
which ReasonFuse Skill intervened
why it intervened
whether the run was progressing
what the final outcome was
```

---

## Required collaboration-aware fields

```text
collaboration_id
task_id
subtask_id
agent_role
handoff_from
handoff_to
```

where applicable.

---

## Security rule

Monitoring must not expose:

```text
secrets
credentials
private chain-of-thought
hidden system prompts
sensitive user content
```

Current local evidence: `python -m competition.phase7.demo.run` renders a
17-event terminal trace. It uses a deterministic `sequence` column instead of
wall-clock time and includes agent, subtask, Skill, decision, progress, and
outcome fields where applicable. The trace carries the collaboration/task
identifiers and the local Phase 7 scan reports `PHASE7_SECRET_SCAN_NONE`.

---

# 17. P7-V12 — Main E2E Closed-Loop Verification

This is the central Phase 7 gate.

Run the complete SP-A scenario.

---

## Expected main pipeline

```text
Intent Input
        ↓
Task Decomposition
        ↓
Long-Horizon Plan
        ↓
Role Assignment
        ↓
Multi-Agent Collaboration
        ↓
ReasonFuse Skill Invocations
        ↓
Injected Collaboration Failure
        ↓
ReasonFuse Intervention
        ↓
Remediation Proposal
        ↓
Approval
        ↓
Tool / World-State Change
        ↓
Fresh Verification
        ↓
Verified Result
        ↓
Runtime Monitoring
```

---

## Six-Skill usage gate

All six Skills must be used meaningfully in the main E2E or in a tightly linked E2E suite.

Preferred:

```text
all six appear in the primary main run
```

If one Skill is not naturally exercised in the main happy path, the competition demo may include a short branch.

Do not claim “six integrated Skills” if half of them never execute.

Current local E2E evidence from `python -m competition.phase7.evaluation`:

```text
trajectory_guard       3 invocations
progress_accounting    2 invocations
failure_detection      1 invocation
execution_contract     1 invocation
approval_control       2 invocations
outcome_verification   1 invocation
```

The local coordinator is deterministic role-agent orchestration, not an
external framework run with independently scheduled LLM agents. The stronger
“official multi-agent framework accepted and genuinely live” claim remains
`BLOCKED` / `NOT VERIFIED`.

---

## E2E result record

Capture:

```text
user intent
generated plan
agent role assignments
message exchanges
Skill triggers
ReasonFuse decisions
fault injection
approval state
world-state change
fresh verification
final outcome
monitoring trace
```

---

# 18. P7-V13 — Installability / Packaging Verification

Track B requires an installable / packagable deliverable.

Verification must be performed from a clean environment.

---

## Clean-install test

Use a clean:

```text
virtual environment
container
or fresh machine/workspace
```

Do not rely on developer-local hidden state.

---

## Required install path

The documented path should look like:

```text
clone
→ install dependencies
→ configure minimal environment
→ run Phase 7 self-tests
→ run trigger evaluation
→ run main demo
```

---

## Verify absence of hidden dependencies

The package must not require:

```text
developer-specific absolute paths
uncommitted files
private local JSON
private tokens baked into code
manual edits not documented
machine-specific caches
```

---

## PASS

A clean environment can reach:

```text
self-tests
trigger evaluation
main demo
```

using the documented setup path.

Current local status: the documented checkout path is:

```powershell
uv sync --frozen --python 3.13
python -m competition.phase7.evaluation
python -m competition.phase7.demo.run
```

That path passed in the current workspace and requires no Azure account or
secret. It is not yet a clean-clone/package-archive test, and no independently
published wheel, container, or archive has been validated. Therefore
`P7-V13 clean install` is `NOT VERIFIED`; `documented local setup` is `PASS`.

---

# 19. P7-V14 — Unified Acceptance Harness Verification

Create one top-level verification command or small command set.

Conceptually:

```text
pwsh -File scripts/run_phase7.ps1 -Mode verify
```

It should report:

```text
6/6 Skills discovered
Skill docs present
test count per Skill
self-test pass rate
trigger hit rate
schema validation
main E2E result
package resource/schema parse smoke
```

Current implementation command: `python -m competition.phase7.evaluation`
(also exposed by `scripts/run_phase7.ps1`). It reports package presence, the
per-Skill self-test count and pass rate, trigger metrics, fault matrix, and
main E2E status. Its schema check parses six JSON schemas; it is not a full
JSON-Schema validator or a clean-install test.

---

## Required final summary example

```text
PHASE7_ACCEPTANCE

Skills:               6 / 6
Self-tests:           120 / 120 PASS
Self-test pass rate:  100%
Trigger hit rate:     98.33%
Message trace IDs:    PASS (formal schema NOT VERIFIED)
Multi-agent E2E:      PASS (local deterministic)
Fault injection:      PASS
Outcome verification: PASS
Package setup:        PASS (checkout)
Clean install:        NOT VERIFIED

RESULT: LOCAL_P0_ACCEPTANCE
```

The current local summary is `6 / 6` Skills, `120 / 120` self-tests PASS,
`98.33%` overall trigger hit rate, `7 / 7` fault fixtures contained, and
`OUTCOME_VERIFIED` for the main E2E. Package-install and framework-eligibility
fields must not be changed to PASS without the missing evidence.

---

# 20. P7-V15 — Demo / Competition Story Verification

A technically correct project can still fail if the demo is confusing.

Verify the final demo against the SP-A story.

---

## Demo must clearly show

```text
1. intent
2. decomposition
3. multi-agent collaboration
4. ReasonFuse reliability intervention
5. fault injection
6. approval / side effect
7. fresh outcome verification
8. monitoring
9. six Skills
10. acceptance metrics
```

---

## Demo comprehension test

Give the demo to someone who has not read the repository.

After watching, they should be able to answer:

```text
What is the problem?
Why are multiple agents needed?
What can go wrong in collaboration?
What does ReasonFuse do?
Which six Skills exist?
How is failure detected?
How is risky execution gated?
How is success verified?
What was actually tested?
```

If they cannot answer these, the demo story is not ready.

Current local demo check:

```powershell
python -m competition.phase7.demo.run
python -m competition.phase7.demo.run --fault loop
python -m competition.phase7.demo.run --approval DENIED
```

The approved default and loop variants complete with
`OUTCOME_VERIFIED`; the denied variant exits non-zero by design because the
side effect is not authorized. The terminal output visibly shows the intent,
plan, roles, fault, Skill decisions, approval, verification, and monitoring.
An independent viewer comprehension test and a final recorded competition
video have not been performed: `NOT VERIFIED`.

---

# 21. P7-V16 — Final Claim Audit

Build a claim-to-evidence matrix.

Current local audit snapshot:

| Claim | Required Evidence | Status | Allowed Wording |
|---|---|---|---|
| 6 effective Skills | package + E2E use | PASS (local) | “6 integrated Skills in the local package” |
| ≥20 tests per Skill | counted tests | PASS (local) | “20 named self-tests per Skill” |
| 100% pass rate | acceptance harness | PASS (local) | “120/120 local self-tests pass” |
| trigger hit rate ≥90% | frozen evaluation dataset | PASS (local) | “98.33% on the local dataset” |
| role collaboration | E2E trace | PASS (local) | “deterministic role-agent orchestration” |
| external multi-agent framework | live framework run + eligibility | NOT VERIFIED / BLOCKED | do not claim official framework acceptance |
| fault injection | deterministic scenario | PASS (local) | “fault-injected local collaboration trace” |
| shared message schema | producer/consumer validation | NOT VERIFIED | do not claim full schema interoperability |
| clean install / published package | clean clone or archive run | NOT VERIFIED | “documented local checkout setup” only |
| swarm emergence | dedicated evidence | NOT VERIFIED | do not claim full swarm emergence |
| framework compatibility | organizer confirmation | BLOCKED | do not claim official approval yet |
| official submission/video | final package and viewer review | NOT VERIFIED | do not claim submitted or judge-reviewed |

---

## Special warning — framework compatibility

The supplied SP-A brief gives open-source framework examples such as:

```text
AgentVerse
AutoGen
etc.
```

The supplied material does **not** clearly establish that Microsoft Agent Framework is accepted as an equivalent.

Therefore final verification must include:

```text
organizer compatibility confirmed
```

or the submission must use an accepted orchestration framework.

Until confirmed:

```text
Framework Eligibility = BLOCKED / OPEN QUESTION
```

This is not a ReasonFuse correctness failure.

---

# 22. P7-V17 — Final Freeze / Submission Gate

Before submission:

```text
no new features
no new agent roles
no new Skill category
no architecture redesign
```

Run the final acceptance suite once.

Current freeze status is not yet ready for submission. The executable local
P0 gates pass, but the checklist below must keep the unresolved items visible
until the Phase 7 implementation is reviewed and committed, a clean install
is tested, framework eligibility is resolved, and the final submission
artifacts are independently checked.

Current status summary:

```text
[PASS]           core regression and no core diff
[PASS]           6 Skill package presence and local contracts
[PASS]           120 / 120 self-tests
[PASS]           local trigger evaluation and fault matrix
[PASS]           deterministic local main E2E
[NOT VERIFIED]   formal message producer/consumer compatibility
[NOT VERIFIED]   dynamic replanning and ambiguous-intent handling
[NOT VERIFIED]   clean-clone or published-archive installation
[BLOCKED]        official orchestration-framework eligibility
[NOT VERIFIED]   final archive, video, and official submission review
```

---

## Final P0 checklist

### Core

```text
[ ] Phase 6 baseline preserved
[ ] ReasonFuse core regression PASS
[ ] no unreviewed core redesign
```

### Skills

```text
[ ] 6 / 6 formal Skills present
[ ] 6 / 6 SKILL.md present
[ ] all supporting implementations present
[ ] all input/output contracts present
[ ] all examples present
```

### Self-tests

```text
[ ] each Skill has ≥20 tests
[ ] total ≥120 tests
[ ] 100% required self-tests PASS
```

### Trigger system

```text
[ ] evaluation dataset frozen before final measurement
[ ] overall hit rate ≥90%
[ ] per-Skill results recorded
[ ] confusion summary recorded
```

### SP-A orchestration

```text
[ ] intent parsing PASS
[ ] task decomposition PASS
[ ] long-horizon plan PASS
[ ] role assignment PASS
[ ] genuine multi-agent collaboration PASS
[ ] shared message schema PASS
```

### Reliability

```text
[ ] collaboration fault injection PASS
[ ] ReasonFuse intervention PASS
[ ] bounded execution PASS
[ ] approval flow PASS
[ ] fresh outcome verification PASS
```

### Monitoring

```text
[ ] collaboration trace visible
[ ] ReasonFuse decisions visible
[ ] task/agent identifiers visible
[ ] no secrets / hidden reasoning exposed
```

### E2E

```text
[ ] one complete main pipeline PASS
[ ] all six Skills used meaningfully
[ ] final result verified
```

### Packaging

```text
[ ] clean install PASS
[ ] documented setup PASS
[ ] test command PASS
[ ] trigger-eval command PASS
[ ] demo command PASS
```

### Submission

```text
[ ] framework eligibility resolved
[ ] claims match evidence
[ ] no unsupported swarm / production claims
[ ] no secrets
[ ] final commit SHA recorded
[ ] final archive/package generated
[ ] final demo video checked
```

---

# 23. P0.5 Verification

Only after all P0 items pass.

Optional verification:

```text
advanced relationship graph
swarm-emergence visualization
second business scenario
additional agent role
live cloud deployment
Foundry IQ integration
APIM sticky canary
advanced adversarial simulation
performance profiling
```

P0.5 failure must not invalidate P0.

---

# 24. Recommended Evidence Layout

Recommended local/public evidence structure:

```text
evidence/
└── phase7/
    ├── baseline/
    ├── skills/
    │   ├── trajectory_guard/
    │   ├── progress_accounting/
    │   ├── failure_detection/
    │   ├── execution_contract/
    │   ├── approval_control/
    │   └── outcome_verification/
    │
    ├── triggers/
    │   ├── dataset.json
    │   ├── metrics.json
    │   └── confusion-summary.md
    │
    ├── orchestration/
    │   ├── plan.md
    │   ├── message-schema.md
    │   └── collaboration-trace.md
    │
    ├── faults/
    │   ├── C-ADV-001.md
    │   ├── C-ADV-002.md
    │   └── C-ADV-003.md
    │
    ├── e2e/
    │   └── main-spa-run.md
    │
    ├── packaging/
    │   └── clean-install.md
    │
    └── demo/
        └── final-demo-check.md
```

Public evidence must be sanitized.

Current checkout evidence is command output and source inspection; no immutable
`evidence/phase7/` run bundle, archive hash, video, or official submission
record has been created yet. A future final run should save the acceptance JSON,
terminal trace, fault matrix, commit SHA, and clean-install output into the
layout above before changing the corresponding status to `PASS`.

---

# 25. Standard Phase 7 Evidence Record

Use this template:

```markdown
## P7-RUN-<ID> — <title>

- Timestamp:
- Commit SHA:
- Environment:
- Competition track:
- Framework:
- Scenario:
- collaboration_id:
- User intent:
- Plan:
- Active agents:
- Skills triggered:
- Trigger result:
- Fault injected:
- ReasonFuse intervention:
- Approval state:
- World-state change:
- Verification observation:
- Final outcome:
- Monitoring evidence:
- Result: PASS / FAIL / NOT VERIFIED / BLOCKED
- Evidence artifacts:
- Limitations:
```

Recommended IDs:

```text
P7-SKILL-001   Trajectory Guard
P7-SKILL-002   Progress Accounting
P7-SKILL-003   Failure Detection
P7-SKILL-004   Execution Contract
P7-SKILL-005   Approval Control
P7-SKILL-006   Outcome Verification

P7-TRIG-001    Trigger evaluation
P7-ORCH-001    Planning + collaboration
P7-ADV-001     Ping-pong handoff
P7-ADV-002     Duplicate retrieval swarm
P7-ADV-003     Premature remediation
P7-E2E-001     Main SP-A closed loop
P7-PKG-001     Clean install
P7-DEMO-001    Final demo rehearsal
```

---

# 26. Failure Triage

When verification fails, classify first.

## A — Competition Requirement Ambiguity

Example:

```text
orchestration framework eligibility unclear
submission format unclear
```

Action:

```text
clarify with organizer
do not rewrite ReasonFuse
```

---

## B — Skill Packaging Defect

Example:

```text
missing SKILL.md
schema inconsistent
adapter path broken
```

Action:

```text
fix Phase 7 packaging
```

---

## C — Trigger Routing Defect

Example:

```text
wrong Skill selected
ambiguous requests misrouted
overall hit rate <90%
```

Action:

```text
fix trigger router / descriptions / examples
rerun frozen evaluation set
```

Do not delete difficult test examples merely to inflate the score.

---

## D — Orchestration Defect

Example:

```text
handoff state lost
task IDs inconsistent
planner skips dependency
agents duplicate work because shared state is broken
```

Action:

```text
fix Phase 7 orchestration layer
```

---

## E — Demo World / Fault Fixture Defect

Example:

```text
fault does not reset
world state nondeterministic
stale/fresh generation cannot be distinguished
```

Action:

```text
fix scenario fixture
```

---

## F — ReasonFuse Core Correctness Defect

Example:

```text
contained trajectory still dispatches
stale verification becomes OUTCOME_VERIFIED
execution contract does not enforce declared bounds
```

Only category F justifies touching the frozen ReasonFuse core.

Required response:

```text
minimal fix
→ core regression
→ affected 15 scenarios
→ affected Skill tests
→ affected Phase 7 E2E
```

---

# 27. Anti-Gaming Rules

Phase 7 verification must not game the competition metrics.

Do not:

```text
write 20 nearly identical tests
remove hard trigger examples after measuring
count documentation examples as runtime tests
count six aliases of one Skill as six effective Skills
declare success from accepted side effect
use decorative agents that do no real work
fake fault injection with pre-recorded output
claim installability from the developer machine only
```

The goal is to make the submission defensible under judge questioning.

---

# 28. Verification Stop Conditions

Stop construction and prepare submission when:

```text
all P0 gates PASS
```

Do not continue adding:

```text
extra agents
extra Skills
extra dashboards
extra cloud services
extra competition tracks
```

just because time remains.

Use remaining time for:

```text
demo stability
evidence cleanup
presentation polish
README clarity
packaging reliability
```

---

# 29. Definition of Verified Phase 7

Phase 7 is **VERIFIED COMPLETE** only when we can truthfully state:

> The ReasonFuse competition distribution contains at least six effective Skills, each documented and backed by at least twenty self-tests. The required self-tests pass, the trigger system reaches the required hit rate, the Skills operate inside one unified SP-A multi-agent scenario, and the main pipeline demonstrates task decomposition, planning, genuine role collaboration, injected collaboration failure, deterministic ReasonFuse intervention, high-impact action control, fresh outcome verification, runtime monitoring, and a reproducible installable package.

Current status: the first executable/local portion of this statement is
supported by the acceptance run, but the phrase “genuine role collaboration”
is currently limited to the deterministic local role-agent coordinator, and
“reproducible installable package” has only been demonstrated as a checkout
setup. Until the unresolved gates above are closed, the correct label is
`LOCAL_P0_ACCEPTANCE = PASS`, not `VERIFIED COMPLETE`.

---

# 30. Final Verification Thesis

The submission should prove more than:

```text
six Skills exist
```

It should prove:

```text
the six Skills work together
        ↓
inside real multi-agent collaboration
        ↓
under controlled failure
        ↓
ReasonFuse changes the runtime outcome
        ↓
the final result is verified
        ↓
the whole thing is testable and packageable
```

The final Phase 7 standard is:

> **Do not submit six isolated Skill folders. Submit one reliable multi-agent system whose six Skills form a tested, observable, end-to-end control layer.**
