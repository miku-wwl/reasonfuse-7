# Failure Detection

## Purpose

Identify deterministic loop, oscillation, retrieval-churn, and stalled
collaboration patterns.

## When to Trigger

Trigger when the orchestrator reviews a recent action trajectory or asks for a
collaboration-failure classification.

## When NOT to Trigger

Do not use it to judge business correctness, approve side effects, or infer a
failure from one unsuccessful observation.

## Inputs

Recent action fingerprints, objective-progress booleans, and optional retrieval
attempt identities.

## Outputs

`DETECTED` or `CLEAR`, a deterministic failure type, and an explanation.

## Preconditions

Fingerprint and progress histories must be bounded JSON arrays.

## Deterministic Logic

The adapter delegates to the frozen exact-loop, oscillation, and retrieval-churn
detectors.

## Failure Modes

Malformed histories are blocked. Useful rechecks and changed retrieval evidence
must not be mislabeled as failure.

## Example

See `examples/example.json` for a ping-pong handoff.

## Self-Test Coverage

Twenty cases cover detector thresholds, false positives, retrieval versions,
and collaboration-shaped trajectories.

## Integration in the Main Scenario

The fault-injection stage routes its ping-pong trace through this Skill before
the healthy remediation path continues.

## Dependencies

Frozen `reasonfuse.core.detectors` through `CompetitionAdapter`.

## Limitations

The Skill detects patterns from supplied history; it does not inspect private
agent reasoning or predict future failures.
