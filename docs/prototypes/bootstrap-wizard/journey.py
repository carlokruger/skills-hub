"""Pure state machine for the throwaway bootstrap-wizard journey prototype."""

from dataclasses import dataclass, replace


STAGES = (
    "Inspect target",
    "Confirm run mode",
    "Select intent",
    "Resolve policy choices",
    "Review plan and conflicts",
    "Authorize changes",
    "Execute repository changes",
    "Complete manual stages",
    "Verify baseline",
    "Review result",
)


@dataclass(frozen=True)
class Journey:
    scenario: str
    stage: int = 0
    status: str = "planning"
    mode: str = "unconfirmed"
    recommendation: str = "adopt"
    recipe: str = "none"
    workloads: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    authorization: str = "none"
    manual_stage: str = "none"
    evidence: str = "none"
    state_fingerprint: str = "state-a"
    plan_fingerprint: str = "none"
    result: str = "not reached"
    message: str = "Inspect the selected root; inspection is read-only."


def new_journey(scenario: str) -> Journey:
    if scenario == "new":
        return Journey(scenario=scenario, recommendation="initialize")
    if scenario == "adopt":
        return Journey(
            scenario=scenario,
            conflicts=("AGENTS.md has contradictory policy",),
        )
    return Journey(
        scenario="resume",
        stage=7,
        status="incomplete",
        mode="adopt",
        recipe="Next.js web app",
        workloads=("web: next-web @ .",),
        capabilities=("github-repository", "github-actions-ci", "vercel-deployment:web"),
        authorization="approved for plan-a",
        manual_stage="Authorize Vercel account and link project",
        state_fingerprint="state-a",
        plan_fingerprint="plan-a",
        result="incomplete — manual authority required",
        message="Resume by re-inspecting state before accepting evidence.",
    )


def advance(state: Journey) -> Journey:
    if state.stage == 1 and state.mode == "unconfirmed":
        return replace(state, message="Confirm the recommended mode before continuing.")
    if state.stage == 4 and state.conflicts:
        return replace(state, message="Resolve every conflict before authorization.")
    if state.stage == 5 and state.authorization == "none":
        return replace(state, message="Authorize the exact fingerprinted plan before execution.")
    if state.stage == 7 and state.manual_stage != "none" and state.evidence == "none":
        return replace(state, status="incomplete", result="incomplete — manual authority required", message="Pause safely; show resume and abandon/recover commands.")
    if state.stage == 8 and state.state_fingerprint != "state-a":
        return replace(state, status="planning", stage=0, authorization="void", result="not reached", message="Detected drift invalidated the reviewed plan; replan.")
    next_stage = min(state.stage + 1, len(STAGES) - 1)
    updates = {"stage": next_stage, "message": _stage_message(next_stage)}
    if next_stage == 4:
        updates["plan_fingerprint"] = "plan-a"
    if next_stage == 6:
        updates["status"] = "executing"
    if next_stage == 8:
        updates["status"] = "verifying"
    if next_stage == 9:
        updates.update(status="verified", result="verified", message="Show changes, checks, provenance, recovery retention, and exact next commands.")
    return replace(state, **updates)


def apply_action(state: Journey, action: str) -> Journey:
    if action == "back":
        return replace(state, stage=max(0, state.stage - 1), message="Moved back without mutating the target.")
    if action == "confirm-mode":
        return replace(state, mode=state.recommendation, message=f"Human confirmed {state.recommendation}; it remains run-local.")
    if action == "select":
        return replace(state, recipe="Next.js web app", workloads=("web: next-web @ .",), capabilities=("tdd:web", "github-repository", "github-actions-ci"), message="Recipe expanded visibly; durable configuration stores only resolved intent.")
    if action == "resolve":
        return replace(state, conflicts=(), message="Conflict resolved for this plan; review the resulting diff and ownership boundary.")
    if action == "authorize":
        if state.plan_fingerprint == "none":
            return replace(state, message="No reviewed plan exists to authorize.")
        return replace(state, authorization=f"approved for {state.plan_fingerprint}", message="Authorization applies only to this exact plan.")
    if action == "evidence":
        return replace(state, evidence="verified by provider state", status="planning", result="not reached", message="Captured no secret; verify provider state and continue.")
    if action == "drift":
        return replace(state, state_fingerprint="state-b", message="Simulated repository drift; the next verification/resume check must invalidate stale authorization.")
    return state


def _stage_message(stage: int) -> str:
    return (
        "Show detected facts and why the mode is recommended.",
        "Human confirms Initialization Run or Adoption Run.",
        "Offer a recipe, then show every Workload and Capability it proposes.",
        "Materialize every default and collect required rationale.",
        "Show targets, ownership, diffs, verification, recovery, and conflicts.",
        "Require plan-wide confirmation plus per-change destructive approval.",
        "Automate deterministic local and API operations; stop on drift or failure.",
        "Guide only work requiring human authority; capture and verify evidence.",
        "Run every selected check and promote configuration plus provenance together.",
        "Report verified, incomplete, failed, or cancelled — never warning-success.",
    )[stage]
