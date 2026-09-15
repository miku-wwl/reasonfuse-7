# Trajectory Guard

## Purpose

Decide whether a proposed tool action may be dispatched on the current
ReasonFuse trajectory.

## When to Trigger

Trigger before every proposed tool or side-effect dispatch when the
orchestrator asks whether the action is safe to execute.

## When NOT to Trigger

Do not use it for business diagnosis, progress reporting, human approval, or
fresh postcondition verification after an accepted side effect.

## Inputs

`tool_name` and JSON `arguments`, plus the adapter's bounded runtime state.

## Outputs

`ALLOW` or `BLOCK`, an optional reason, the trajectory state, and a canonical
tool fingerprint.

## Preconditions

The action name must be non-empty and arguments must be JSON-compatible.

## Deterministic Logic

The wrapper delegates to `ReasonFuseEngine.before_dispatch`; it does not copy
the core detector or budget logic.

## Failure Modes

Malformed actions are blocked. Contained trajectories, exhausted budgets, and
detected loops are blocked with the core fuse reason.

## Example

```json
{"tool_name":"restart_service","arguments":{"service_name":"checkout"}}
```

## Self-Test Coverage

Twenty boundary cases cover first dispatch, containment, budgets, disabled
mode, argument normalization, and reserved verification.

## Integration in the Main Scenario

The Skill guards diagnosis reads, the remediation proposal, and the fresh
verification read.

## Dependencies

Frozen `reasonfuse.core.engine`, `contract`, `fingerprint`, and `state`.

## Limitations

It makes a deterministic dispatch decision; it is not an authorization system
and cannot prove that a tool actually ran.
