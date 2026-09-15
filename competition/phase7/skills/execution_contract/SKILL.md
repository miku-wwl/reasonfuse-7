# Execution Contract

## Purpose

Report whether a proposed action fits the bounded ReasonFuse run contract.

## When to Trigger

Trigger before dispatch when the orchestrator needs remaining step, tool-call,
side-effect, or verification-reserve allowance.

## When NOT to Trigger

Do not use it to classify failure patterns, request human approval, or decide
whether the final business outcome is healthy.

## Inputs

Persisted counters, contract limits, action class, and verification status.

## Outputs

`ALLOW` or `BLOCK`, reason, remaining allowances, and reserve status.

## Preconditions

Contract limits must satisfy the frozen `RunContract` validation rules.

## Deterministic Logic

The adapter delegates slot and side-effect accounting to
`RunContract.before_dispatch`, including the reserved verification read.

## Failure Modes

Malformed contracts or counters are blocked. A side effect is blocked when its
required action-plus-verification slots do not fit.

## Example

See `examples/example.json`.

## Self-Test Coverage

Twenty cases cover boundaries for steps, tools, side effects, verification
reserve, custom versions, and invalid limits.

## Integration in the Main Scenario

The Skill checks the remediation proposal and reserves capacity for the fresh
service-status read.

## Dependencies

Frozen `reasonfuse.core.contract`, `engine`, and `state`.

## Limitations

This is a pre-dispatch budget decision; it does not execute tools or observe
the external world.
