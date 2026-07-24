---
name: wayfinder-relay
description: Checkpoint and resume a Wayfinder effort across fresh Codex tasks. Use after a Wayfinder ticket is resolved when the user wants a repo-root handoff and exact `/new` continuation, or in a fresh task to load the latest Wayfinder handoff, refresh the frontier, claim the next ticket, resolve exactly one ticket, and checkpoint again.
---

# Wayfinder Relay

Bridge Wayfinder tasks through durable repository artifacts. Operate in checkpoint mode before `/new` and resume mode after `/new`.

Do not attempt to execute `/new`. It is client-level session control, not an agent tool or shell command.

## Invariants

- Read and follow `../wayfinder/SKILL.md` for map, frontier, claim, and resolution rules.
- Read and follow `../handoff/SKILL.md` before creating a checkpoint.
- Resolve at most one Wayfinder ticket per Codex task. Preserve Wayfinder's one-ticket session boundary.
- Treat the live tracker and map as source of truth. Treat a handoff's frontier pointer as a restart hint that may have gone stale.
- Refer to maps and tickets by linked names, not bare ids or filenames in human-facing text.
- Recheck current state before claiming because another task may have moved the frontier.
- Never claim or open the next ticket while checkpointing.
- Reference existing decisions and artifacts; do not duplicate them in a handoff.

## Select a mode

- Use **checkpoint mode** when the current task has just resolved a Wayfinder ticket or the user explicitly asks to stop and hand off.
- Use **resume mode** in a fresh task, when the user says to continue, or when no ticket is active in the current conversation.
- Honor an explicit `checkpoint`, `resume`, map, ticket, or handoff argument.
- If more than one active map or handoff is plausible and repository evidence cannot disambiguate them safely, ask the user to choose.

## Checkpoint mode

1. Find the repository root and load the active map at low resolution.
2. Inspect the current ticket and confirm its state:
   - If resolved, verify that the resolution is recorded, the ticket is closed, the map has a context pointer, and any newly visible frontier or fog changes are represented.
   - Finish missing tracker bookkeeping when the decision is already established. Do not invent or answer an unresolved human decision.
   - If the user stops before resolution, leave the ticket open and make that same ticket the restart point.
3. Refresh the frontier without claiming anything. If the current ticket remains open, use it as the restart point; otherwise identify the first open, unblocked, unclaimed child in tracker order.
4. Follow `../handoff/SKILL.md` and write a timestamped handoff under the repository root's `.handoff/` folder.
5. Keep the handoff pointer-heavy. Include:
   - the repository root and active map;
   - the ticket resolved or paused in this task;
   - the exact restart ticket by linked name, including whether it is currently unclaimed;
   - relevant working-tree state and verification results;
   - the skills named by the map, plus `wayfinder-relay` and `wayfinder`;
   - the one-ticket-per-task invariant;
   - the exact continuation prompt: `Use $wayfinder-relay to resume from <handoff-path>.`
6. End with a compact transition block:

```text
/new
$wayfinder-relay resume <handoff-path>
```

Do not begin the restart ticket in checkpoint mode.

## Resume mode

1. Locate the checkpoint:
   - Use an explicit handoff path when provided.
   - Otherwise choose the newest relevant Wayfinder handoff under the repository root's `.handoff/` folder.
   - If no handoff exists, locate the active Wayfinder map directly and continue from its live frontier.
2. Load the handoff, then load the map and this repository's tracker instructions. Do not load every ticket body.
3. Refresh current ticket and dependency state:
   - Resume an explicitly paused open ticket when it is still the valid restart point.
   - Otherwise choose the first open, unblocked, unclaimed frontier ticket in tracker order.
   - If the recorded ticket was claimed or closed elsewhere, skip it and recompute from live state.
4. Claim the chosen ticket before opening its full body.
5. Follow `../wayfinder/SKILL.md` and every skill named by the map. For HITL tickets, preserve the required one-question-at-a-time exchange and never answer for the human.
6. Resolve exactly one ticket. After recording the resolution and updating the map, automatically run checkpoint mode. Do not wait for another invocation and do not claim a second ticket.

Treat short user replies to HITL questions as continuation of this relay until the selected ticket is resolved and checkpointed.

## End states

- If the map has another frontier ticket, checkpoint it without claiming it.
- If tickets remain but none are takeable, checkpoint the blocked state and name the blocking change needed.
- If no tickets or in-scope fog remain and the destination is clear, record map completion according to the tracker, checkpoint the implementation handoff, and recommend only the next workflow already supported by the map's destination or Notes.
