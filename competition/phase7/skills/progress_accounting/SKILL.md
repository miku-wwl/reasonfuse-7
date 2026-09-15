# Progress Accounting

## Purpose

Determine whether a collaboration step made meaningful objective progress.

## When to Trigger

Trigger after an observation, tool result, retrieval result, or state update
when the orchestrator needs an objective delta.

## When NOT to Trigger

Do not treat a request ID, counter, todo-only edit, or unchanged duplicate
evidence as objective progress.

## Inputs

Before and after evidence, world state, retrieval identity, postcondition state,
and optional todo snapshots.

## Outputs

`ADVANCING` or `STALLED`, the objective-progress boolean, and each delta signal.

## Preconditions

Both state snapshots must be JSON objects.

## Deterministic Logic

The adapter delegates to the frozen `result_signals` implementation. Evidence,
world-state, retrieval, and postcondition deltas are distinct signals.

## Failure Modes

Malformed snapshots are blocked. A todo-only change never fabricates objective
progress.

## Example

See `examples/example.json` for a healthy world-state transition.

## Self-Test Coverage

Twenty cases cover evidence, world, retrieval, todo, noisy fields, and malformed
inputs.

## Integration in the Main Scenario

Diagnosis, remediation, and verification each emit a progress observation.

## Dependencies

Frozen `reasonfuse.core.progress` through `CompetitionAdapter`.

## Limitations

Progress is an objective delta signal; it does not decide whether a goal is
complete without outcome verification.
