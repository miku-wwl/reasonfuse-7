# Outcome Verification

## Purpose

Determine whether an accepted side effect produced its intended fresh
postcondition in the simulated or real world.

## When to Trigger

Trigger after an accepted side effect when a fresh read for the same resource
is available.

## When NOT to Trigger

Do not declare success from an accepted request alone, a stale read, a read for
another resource, or an unverified agent claim.

## Inputs

Action, requested resource, accepted result, and fresh observation.

## Outputs

`OUTCOME_VERIFIED`, `POSTCONDITION_FAILED`, or `OUTCOME_UNKNOWN`, with reason
and resource.

## Preconditions

The action must have an accepted result and a resource-specific observation.

## Deterministic Logic

The wrapper delegates to the frozen `OutcomeVerifier` and its postcondition
registry, including generation and freshness checks.

## Failure Modes

Missing, stale, malformed, unhealthy, or mismatched observations never become
verified success.

## Example

See `examples/example.json`.

## Self-Test Coverage

Twenty cases cover verified, failed, unknown, stale, generation, and malformed
observations.

## Integration in the Main Scenario

The Verification Agent performs the fresh checkout status read and publishes
the final outcome.

## Dependencies

Frozen `reasonfuse.core.outcome` through `CompetitionAdapter`.

## Limitations

The local scenario verifies its resettable fixture; cloud or production
verification requires a real observation provider.
