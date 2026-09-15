# Approval Control

## Purpose

Gate a high-impact side effect using an explicit platform/native approval
state.

## When to Trigger

Trigger when an agent proposes a risky remediation or another high-impact
operation.

## When NOT to Trigger

Do not require approval for read-only diagnostics or use this Skill as a
replacement for the host platform's authorization and approval primitives.

## Inputs

Action, risk class, and the externally supplied approval state.

## Outputs

`NOT_REQUIRED`, `APPROVAL_REQUIRED`, `APPROVED`, or `DENIED`.

## Preconditions

The action and risk class must be explicit.

## Deterministic Logic

Low and medium-risk reads need no approval. High and critical actions require a
current `APPROVED` state; pending, stale, and unknown states remain gated.

## Failure Modes

Malformed actions or risk classes are blocked. A denial never becomes an
approval through normalization.

## Example

See `examples/example.json`.

## Self-Test Coverage

Twenty cases cover low/high/critical risk, approval, denial, stale state, and
input validation.

## Integration in the Main Scenario

The operations proposal is held at `APPROVAL_REQUIRED` until the operator
returns `APPROVED`.

## Dependencies

`CompetitionAdapter.approval`; the real competition host may replace the
approval-state provider without changing the Skill contract.

## Limitations

The local demo models approval state; it does not impersonate a production
identity provider or human approval UI.
