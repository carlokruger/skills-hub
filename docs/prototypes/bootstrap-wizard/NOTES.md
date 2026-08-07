# Prototype verdict

## Findings

- The first walkthrough was hard to navigate because it exposed all commands at
  once and provided too little guidance about what each choice meant or which
  action should come next.
- Revision: every stage now recommends one next action, explains why, limits the
  visible choices to those relevant at that gate, and states their consequences.

## Verdict

The revised guided-choice journey was approved in the human walkthrough. Retain
the stage-local recommendation, rationale, limited choice set, and explicit
consequences in the production wizard contract.

Capture what should be retained in the issue resolution:

- Stage order: Approved as inspect, confirm mode, select intent, resolve choices,
  review plan/conflicts, authorize, execute, complete Manual Stages, verify, and
  review result.
- Prompts and defaults: Must explain the recommended choice and its consequence,
  not merely display its current value.
- Preview and confirmation gates: Recipe expansion and every resolved default
  remain visible; plan approval is fingerprint-bound and destructive changes
  receive per-change approval.
- Resume and non-interactive behavior: Resume re-inspects state and invalidates
  stale approval on drift; non-interactive input must express the same complete
  choices and structured resolutions without guessing.
- Automation versus Manual Stage boundary: Automate deterministic local and API
  operations when authority is available; guide only identity-, consent-, or
  provider-authority work and verify resulting evidence.
- Closing summary: Report exactly verified, incomplete, failed, or cancelled,
  with changes, checks, provenance, recovery retention, and next commands.
