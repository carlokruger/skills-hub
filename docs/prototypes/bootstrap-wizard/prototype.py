#!/usr/bin/env python3
"""Throwaway TUI for testing the bootstrap-wizard journey and automation boundary."""

import os

from journey import STAGES, Journey, advance, apply_action, new_journey


BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def guidance(state: Journey) -> tuple[str, str, list[tuple[str, str]]]:
    """Return the recommended action, rationale, and context-relevant choices."""
    if state.stage == 0:
        return (
            "Press [n] to review the run-mode recommendation.",
            "Inspection is read-only. Nothing has been selected or changed yet.",
            [("n", "continue to the detected-state explanation")],
        )
    if state.stage == 1 and state.mode == "unconfirmed":
        return (
            f"Press [m] to confirm the recommended {state.recommendation} mode.",
            "Initialize is only for an effectively empty repository; adopt preserves and integrates existing content. The mode is not saved as project intent.",
            [("m", f"use {state.recommendation} for this run"), ("b", "return to inspection if the recommendation looks wrong")],
        )
    if state.stage == 2 and state.recipe == "none":
        return (
            "Press [s] to preview the Next.js web app recipe.",
            "A recipe is only a visible starting proposal. You will review every Workload, Capability, and default before anything is saved.",
            [("s", "preview the proposed selections"), ("b", "revisit the run mode")],
        )
    if state.stage == 4 and state.conflicts:
        return (
            "Press [c] to simulate reviewing and resolving this conflict.",
            "Real conflicts show preserve, merge, replace, or change-intent choices with a diff and recovery plan; no global force option exists.",
            [("c", "review and resolve the listed conflict"), ("b", "change intent before resolving it")],
        )
    if state.stage == 5 and state.authorization == "none":
        return (
            "Press [a] to authorize this exact reviewed plan.",
            "Approval is bound to the plan fingerprint. Repository drift or a changed plan voids it.",
            [("a", "approve the reviewed plan"), ("b", "return to plan review")],
        )
    if state.stage == 7 and state.manual_stage != "none" and state.evidence == "none":
        return (
            "Press [e] after completing the provider step, or [d] to test resume after drift.",
            "The bootstrapper guides work requiring your identity or authority, stores no secret, and verifies the resulting provider state before continuing.",
            [("e", "simulate verified provider evidence"), ("d", "simulate repository changes while paused")],
        )
    return (
        "Press [n] to continue to the next review gate.",
        "You can always go back before execution. The prototype never touches a repository.",
        [("n", "continue"), ("b", "go back"), ("d", "simulate state drift")],
    )


def render(state: Journey) -> None:
    os.system("clear")
    print(f"{BOLD}PROJECT STANDARDS WIZARD — THROWAWAY PROTOTYPE{RESET}")
    print(f"{DIM}Scenario {state.scenario} · stage {state.stage + 1}/{len(STAGES)}{RESET}\n")
    fields = (
        ("Stage", STAGES[state.stage]), ("Purpose", state.message), ("Status", state.status),
        ("Mode", f"{state.mode} (recommended: {state.recommendation})"), ("Recipe", state.recipe),
        ("Workloads", ", ".join(state.workloads) or "none"),
        ("Capabilities", ", ".join(state.capabilities) or "none"),
        ("Conflicts", "; ".join(state.conflicts) or "none"), ("Plan", state.plan_fingerprint),
        ("Authorization", state.authorization), ("Manual stage", state.manual_stage),
        ("Evidence", state.evidence), ("Detected state", state.state_fingerprint), ("Result", state.result),
    )
    for label, value in fields:
        print(f"{BOLD}{label:15}{RESET} {value}")
    recommendation, reason, choices = guidance(state)
    print(f"\n{BOLD}What to do now{RESET}")
    print(recommendation)
    print(f"{DIM}{reason}{RESET}")
    print(f"\n{BOLD}Choices at this stage{RESET}")
    for key, consequence in choices:
        print(f"  {BOLD}[{key}]{RESET} {consequence}")
    print(f"\n{BOLD}Automation boundary{RESET}")
    if state.stage == 7:
        print("GUIDE: open provider/CLI path, explain the exact human action, capture a non-secret reference, verify resulting state")
    else:
        print("AUTOMATE: inspect, render, diff, backup, mutate declared targets, call authenticated APIs, and verify")
    print(f"\n{DIM}Scenario shortcuts: [1] new repo  [2] adopt repo  [3] resume manual stage  [q] quit{RESET}")


def main() -> None:
    state = new_journey("new")
    actions = {"b": "back", "m": "confirm-mode", "s": "select", "c": "resolve", "a": "authorize", "e": "evidence", "d": "drift"}
    while True:
        render(state)
        choice = input("\nChoice: ").strip().lower()
        if choice == "q":
            return
        if choice in {"1", "2", "3"}:
            state = new_journey({"1": "new", "2": "adopt", "3": "resume"}[choice])
        elif choice == "n":
            state = advance(state)
        elif choice in actions:
            state = apply_action(state, actions[choice])


if __name__ == "__main__":
    main()
