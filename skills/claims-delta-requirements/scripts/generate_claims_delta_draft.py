#!/usr/bin/env python3
"""Generate a first-pass claims requirement draft from a reference and delta brief."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def parse_markdown_sections(text: str, min_level: int = 2, max_level: int = 3) -> tuple[str | None, dict[str, dict]]:
    title = None
    sections: dict[str, dict] = {}
    current_h2: str | None = None
    current_h3: str | None = None

    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            continue

        match = re.match(r"^(#{2,3})\s+(.*)$", line)
        if match:
            level = len(match.group(1))
            heading = match.group(2).strip()
            if level < min_level or level > max_level:
                continue
            if level == 2:
                current_h2 = heading
                current_h3 = None
                sections.setdefault(current_h2, {"body": [], "children": {}})
            else:
                if current_h2 is None:
                    continue
                current_h3 = heading
                sections[current_h2]["children"].setdefault(current_h3, [])
            continue

        if current_h2 is None:
            continue
        if current_h3 is None:
            sections[current_h2]["body"].append(line)
        else:
            sections[current_h2]["children"][current_h3].append(line)

    return title, sections


def bullets(lines: list[str]) -> list[str]:
    items: list[str] = []
    current: str | None = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            if current is not None:
                items.append(current)
            current = stripped[2:].strip()
            continue
        if current is not None and stripped:
            current = f"{current} {stripped}"
    if current is not None:
        items.append(current)
    return items


def bullet_tree(lines: list[str]) -> list[dict]:
    tree: list[dict] = []
    stack: list[tuple[int, list[dict]]] = [(-1, tree)]
    current_node: dict | None = None
    for line in lines:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if stripped.startswith("- "):
            node = {"text": stripped[2:].strip(), "children": []}
            while stack and indent <= stack[-1][0]:
                stack.pop()
            stack[-1][1].append(node)
            stack.append((indent, node["children"]))
            current_node = node
            continue
        if current_node is not None:
            current_node["text"] = f"{current_node['text']} {stripped}"
    return tree


def render_bullet_tree(nodes: list[dict], indent: int = 0) -> list[str]:
    lines: list[str] = []
    pad = "  " * indent
    for node in nodes:
        lines.append(f"{pad}- {node['text']}")
        lines.extend(render_bullet_tree(node["children"], indent + 1))
    return lines


def tree_node(text: str, children: list[dict] | None = None) -> dict:
    return {"text": text, "children": children or []}


def key_values(lines: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for item in bullets(lines):
        if ":" not in item:
            continue
        key, value = item.split(":", 1)
        values[normalize(key)] = value.strip()
    return values


def keyed_bullets(lines: list[str]) -> dict[str, list[str]]:
    values: dict[str, list[str]] = {}
    current_key: str | None = None
    for item in bullets(lines):
        if ":" in item:
            key, value = item.split(":", 1)
            current_key = normalize(key)
            values.setdefault(current_key, [])
            if value.strip():
                values[current_key].append(value.strip())
            continue
        if current_key is not None:
            values.setdefault(current_key, []).append(item)
    return values


def request_value(request: dict[str, str], key: str, default: str = "[TBD]") -> str:
    return request.get(normalize(key), default)


def match_reference_section(query: str, ref_sections: dict[str, str]) -> tuple[str | None, str | None]:
    if not query:
        return None, None
    nq = normalize(query)
    for heading, body in ref_sections.items():
        nh = normalize(heading)
        if nq == nh or nq in nh or nh in nq:
            return heading, body
    return None, None


def list_block(items: list[str], indent: str = "- ") -> list[str]:
    return [f"{indent}{item}" for item in items] if items else [f"{indent}[TBD]"]


def nested_block(label: str, items: list[str]) -> list[str]:
    if not items:
        return [f"- {label}", "  - [TBD]"]
    lines = [f"- {label}"]
    lines.extend([f"  - {item}" for item in items])
    return lines


def split_first(items: list[str]) -> tuple[str | None, list[str]]:
    if not items:
        return None, []
    return items[0], items[1:]


def render_reference_copy(label: str, query_items: list[str], ref_sections: dict[str, str]) -> list[str]:
    lines = [f"## {label}"]
    if not query_items:
        lines.extend(["- No carry-forward section was specified.", ""])
        return lines
    copied = False
    for item in query_items:
        heading, body = match_reference_section(item, ref_sections)
        if body is None:
            continue
        copied = True
        lines.append(f"### Carried Forward From Reference: {heading}")
        body = body.strip()
        lines.append(body if body else "[Reference section is empty]")
        lines.append("")
    if not copied:
        lines.extend(["- No matching reference sections were found to copy forward.", ""])
    return lines


def primary_action(request: dict[str, str], fallback: str) -> str:
    return request_value(request, "Claim Type / Benefit / Action", fallback)


def is_contractual_definitions_step(request: dict[str, str]) -> bool:
    title = request_value(request, "Requirement Title", "").lower()
    action = primary_action(request, "").lower()
    return "contractual definitions" in title or "contractual definitions" in action


def user_story_lines(request: dict[str, str], delta_sections: dict[str, list[str]]) -> list[str]:
    action = primary_action(request, "the target claim action")
    domain = request_value(request, "Claim Domain / Product", "the claims user")
    role_notes = delta_sections.get("security access changes", [])
    workflow = delta_sections.get("workflow routing changes", [])
    business = delta_sections.get("business logic changes", [])

    if is_contractual_definitions_step(request):
        benefit_set = request_value(request, "Claim Type / Benefit / Action", action)
        lines = [
            f"As a {domain}, I want the system to determine whether contractual definitions are met for **{benefit_set}** so that I can move the claim forward only when the benefit rules are satisfied.",
            "As SmartServe, I want to evaluate the relevant benefit buckets against the contract rules and persist the met / not-met outcome with audit history.",
        ]
    else:
        lines = [
            f"As a {domain}, I want to perform **{action}** so that I can review the current state and act on failures quickly.",
            f"As SmartServe, I want to present the current status for **{action}** and persist the result with audit history.",
        ]
    if role_notes:
        lines.append(f"Access is limited according to the brief: {role_notes[0]}")
    if workflow:
        lines.append(f"Failure handling must follow the new route: {workflow[0]}")
    if business:
        lines.append(f"The core business rule is: {business[0]}")
    return lines


def acceptance_criteria_lines(request: dict[str, str], delta_sections: dict[str, list[str]]) -> list[str]:
    action = primary_action(request, "the target claim action")
    if is_contractual_definitions_step(request):
        benefit_set = request_value(request, "Claim Type / Benefit / Action", action)
        criteria = [
            f"The system evaluates whether contractual definitions are met for **{benefit_set}**.",
            "The system checks the relevant benefit bucket(s) and contract rules for the claim.",
            "The result is recorded as met or not met and is traceable to evidence.",
            "If contractual definitions are met, the case can progress to the next assessment step.",
            "If contractual definitions are not met, the case remains blocked or routes to the agreed clarification path.",
            "The output does not retain later approval-step language from the baseline.",
        ]
    else:
        criteria = [
            f"The user can perform **{action}** only when the role gate allows it.",
            "The system shows the current status and any error code associated with the record.",
            "The result reflects the actual state and is traceable to evidence.",
            "A failed record routes to the agreed follow-up path.",
            "The result is persisted to the claim record with audit history.",
            "The output does not retain assessment-only behavior from the baseline.",
        ]
    return criteria


def reference_sections(reference_text: str) -> dict[str, str]:
    _, sections = parse_markdown_sections(reference_text, min_level=2, max_level=2)
    result: dict[str, str] = {}
    for heading, payload in sections.items():
        result[heading] = "\n".join(payload["body"]).strip()
    return result


def build_variance_only(
    reference_title: str | None,
    reference_path: Path,
    brief_title: str,
    request: dict[str, str],
    closest_ref: dict[str, str],
    delta_sections: dict[str, list[str]],
    unchanged: list[str],
    testing_hotspots: list[str],
    open_questions: list[str],
    output_preference: dict[str, str],
    reviewer_checks: list[str],
    ref_sections: dict[str, str],
) -> str:
    preserved_sections = closest_ref.get("which sections should be preserved unchanged", [])
    safe_sections = output_preference.get("sections safe to carry forward with minimal edits", [])
    lines: list[str] = [
        f"# {brief_title} - Draft",
        "",
        "## Draft Metadata",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| **Generated From** | {reference_title or reference_path.name} |",
        f"| **Reference Path** | {reference_path} |",
        f"| **Requirement Archetype** | {request_value(request, 'Requirement Archetype', 'variance-only requirement')} |",
        f"| **Jira / Tracking** | {request_value(request, 'Jira / Tracking Reference')} |",
        "",
        "## Overview",
        "",
        f"This draft captures the variance against **{reference_title or reference_path.name}** for **{request.get('claim type / benefit / action', brief_title)}**.",
        "",
        "Key deltas:",
    ]
    lines.extend(list_block(delta_sections.get("business logic changes", [])))
    lines.append("")
    lines.append("## Trigger")
    lines.append("")
    trigger_items = delta_sections.get("workflow routing changes", []) + delta_sections.get("data field changes", [])
    lines.extend(list_block(trigger_items))
    lines.append("")
    lines.append("## Basic Flow (with reference to alternative flows)")
    lines.append("")
    lines.append(f"Baseline behavior follows **{reference_title or reference_path.name}** except for the following changes:")
    lines.extend(list_block(
        delta_sections.get("business logic changes", [])
        + delta_sections.get("workflow routing changes", [])
        + delta_sections.get("ui output changes", [])
    ))
    lines.append("")
    lines.append("## Business Acceptance Criteria")
    lines.append("")
    lines.extend(list_block(
        delta_sections.get("business logic changes", [])
        + delta_sections.get("data field changes", [])
        + delta_sections.get("ui output changes", [])
    ))
    lines.append("")
    lines.extend(render_reference_copy("Process Flow", ["Process Flow"], ref_sections))
    lines.append("## Solution - Mock UI")
    lines.append("")
    ui_items = delta_sections.get("ui output changes", [])
    if ui_items:
        lines.extend(list_block(ui_items))
    else:
        lines.append("- As per reference implementation.")
    lines.append("")
    lines.append("## Field Details - Data Attributes")
    lines.append("")
    field_items = delta_sections.get("data field changes", [])
    lines.extend(list_block(field_items))
    lines.append("")
    lines.append("## Specific Dev Tasks")
    lines.append("")
    lines.extend(list_block(
        delta_sections.get("business logic changes", [])
        + delta_sections.get("workflow routing changes", [])
        + delta_sections.get("dependency integration changes", [])
        + delta_sections.get("security access changes", [])
    ))
    lines.append("")
    lines.append("## Testing Considerations")
    lines.append("")
    lines.extend(list_block(testing_hotspots))
    lines.append("")
    lines.append("## Unchanged Baseline Assumptions")
    lines.append("")
    lines.extend(list_block(unchanged))
    lines.append("")
    lines.append("## Carry-Forward Guidance")
    lines.append("")
    lines.append("Sections identified for minimal change:")
    lines.extend(list_block(preserved_sections or safe_sections))
    lines.append("")
    lines.append("## Known Gaps / Questions")
    lines.append("")
    lines.extend(list_block(open_questions))
    lines.append("")
    lines.append("## Reviewer Checks")
    lines.append("")
    lines.extend(list_block(reviewer_checks))
    lines.append("")
    return "\n".join(lines)


def build_claim_step(
    reference_title: str | None,
    reference_path: Path,
    brief_title: str,
    request: dict[str, str],
    delta_sections: dict[str, list[str]],
    delta_trees: dict[str, list[dict]],
    unchanged: list[str],
    testing_hotspots: list[str],
    open_questions: list[str],
    reviewer_checks: list[str],
    ref_sections: dict[str, str],
) -> str:
    step_title = request_value(request, "Requirement Title", brief_title)
    step_action = primary_action(request, step_title)
    business_logic = delta_sections.get("business logic changes", [])
    workflow = delta_sections.get("workflow routing changes", [])
    data_fields = delta_sections.get("data field changes", [])
    ui = delta_sections.get("ui output changes", [])
    deps = delta_sections.get("dependency integration changes", [])
    security = delta_sections.get("security access changes", [])
    business_tree = delta_trees.get("business logic changes", [])
    workflow_tree = delta_trees.get("workflow routing changes", [])
    data_tree = delta_trees.get("data field changes", [])
    ui_tree = delta_trees.get("ui output changes", [])
    deps_tree = delta_trees.get("dependency integration changes", [])
    security_tree = delta_trees.get("security access changes", [])
    testing = testing_hotspots or ["[TBD]"]
    unchanged_shell = unchanged or ["Use the reference artifact only for structural shape."]
    lines = [
        f"# {brief_title} - Draft",
        "",
        "## Draft Metadata",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| **Generated From** | {reference_title or reference_path.name} |",
        f"| **Requirement Archetype** | {request_value(request, 'Requirement Archetype', 'claim-step requirement')} |",
        f"| **Claim Domain / Product** | {request_value(request, 'Claim Domain / Product')} |",
        f"| **Claim Type / Benefit / Action** | {step_action} |",
        f"| **Jira / Tracking** | {request_value(request, 'Jira / Tracking Reference')} |",
        "",
    ]
    lines.extend([
        "## Overview",
        "",
        f"This requirement rewrites **{reference_title or reference_path.name}** for **{step_title}**.",
        "Use the baseline only as the document shell.",
        "The draft should read like the direct decision step for the new benefit set, not the later approval path.",
    ])
    if is_contractual_definitions_step(request):
        lines.extend(render_bullet_tree(business_tree or [tree_node("[TBD]")]))
    else:
        lines.extend(list_block(business_logic))
    lines.append("")
    if is_contractual_definitions_step(request):
        lead_line, bucket_items = split_first(business_logic)
        trigger_intro = "Trigger the step when the claim reaches the contractual-definition assessment gate for the selected benefit set."
        precondition_lines = [
            "Relevant claim record exists.",
            "Policy / contract data for the selected benefit set is available.",
            "Supporting evidence or rider information is available for review.",
            "User has the correct LBC / claims-assessment role.",
        ]
        success_lines = [
            "Contractual-definition outcome determined as met or not met.",
            "Outcome persisted to the claim record with audit history.",
            "If met, the case progresses to the next assessment step.",
            "If not met, the case remains blocked or routes to the agreed clarification path.",
        ]
        process_lines = [
            "Start from the baseline process only as a shell.",
            "Replace later approval logic with contractual-definition logic.",
        ]
        dependency_lines = deps or ["Policy / contract service lookup is required.", "Supporting evidence or rider logic must be available to the decisioning step."]
        security_lines = security or ["Only authorized CC/CS roles should be able to finalize the step outcome."]
    else:
        trigger_intro = f"Trigger the step when **{step_title}** is initiated."
        precondition_lines = [
            "Relevant claim record exists.",
            "User has the correct LBC role.",
            "Supporting source data is available.",
            "The document should keep the established claims requirement format.",
        ]
        success_lines = [
            "Outcome is visible, traceable, and stored with audit history.",
            "Required downstream routing or next-step handoff is completed.",
        ]
        process_lines = [
            "Start from the baseline process only as a shell.",
            "Replace assessment logic with the target action logic.",
        ]
        dependency_lines = deps or ["Supporting source data is available."]
        security_lines = security or ["Restrict access to approved LBC roles."]

    lines.extend([
        "## Trigger",
        "",
        trigger_intro,
        "The trigger and routing must follow the target assessment path, not the later approval path.",
    ])
    if is_contractual_definitions_step(request):
        lines.extend(render_bullet_tree([tree_node("Routing and handoff", workflow_tree or [tree_node("[TBD]")])]))
        lines.extend(render_bullet_tree([tree_node("Evidence / fields", data_tree or [tree_node("[TBD]")])]))
    else:
        lines.extend(list_block(workflow + data_fields))
    lines.append("")
    lines.extend([
        "## Pre-conditions",
        "",
        "Carry forward only the minimum baseline preconditions that still apply.",
        "Add the step-specific conditions from the brief and remove later-step prerequisites.",
    ])
    lines.extend(list_block(precondition_lines))
    lines.append("")
    lines.extend([
        "## Basic Flow (with reference to alternative flows)",
        "",
        "### User Story",
        "",
    ])
    lines.extend(list_block(user_story_lines(request, delta_sections)))
    lines.extend([
        "",
        "### Basic Flow",
        "",
        "The flow below is drafted from the delta brief rather than copied from the baseline.",
    ])
    if is_contractual_definitions_step(request):
        lines.extend(render_bullet_tree([
            tree_node("Decision logic", business_tree or [tree_node("[TBD]")]),
            tree_node(
                "Follow-on actions",
                (workflow_tree or []) + [
                    tree_node("Persist the result to the claim record."),
                    tree_node("Route unresolved cases to the agreed follow-up path."),
                ] if (workflow_tree or []) else [
                    tree_node("Persist the result to the claim record."),
                    tree_node("Route unresolved cases to the agreed follow-up path."),
                ],
            ),
        ]))
    else:
        lines.extend(list_block(
            business_logic
            + workflow
            + [
                "Persist the result to the claim record.",
                "Route unresolved cases to the agreed follow-up path.",
            ]
        ))
    lines.append("")
    lines.extend([
        "## Successful Post Conditions",
        "",
        "The step outcome is visible, traceable, and stored with audit history.",
    ])
    lines.extend(list_block(success_lines))
    lines.append("")
    lines.extend([
        "## Dependencies",
        "",
        "Keep only the dependencies relevant to the new action.",
    ])
    lines.extend(list_block(dependency_lines))
    lines.append("")
    lines.extend([
        "## Business Acceptance Criteria",
        "",
        "State the actual acceptance criteria for the claim-assessment step.",
    ])
    lines.extend(list_block(acceptance_criteria_lines(request, delta_sections)))
    lines.append("")
    lines.extend([
        "## Exception Handling",
        "",
        "Use exception handling only where the step needs it.",
    ])
    lines.extend(list_block(
        [
            "If required evidence is unavailable, keep the case pended and escalate.",
            "If definitions cannot be resolved, route to the agreed clarification path.",
        ]
    ))
    lines.append("")
    lines.extend([
        "## Process Flow",
        "",
        "The process flow below is drafted from the target requirement, not the baseline later-step language.",
    ])
    lines.extend(list_block(process_lines))
    lines.append("")
    lines.extend([
        "## Solution - Mock UI",
        "",
        "Show only the UI elements needed for the contractual-definition step.",
    ])
    lines.extend(render_bullet_tree(ui_tree or [tree_node("Payment status display and processed flag.")]))
    lines.append("")
    lines.extend([
        "## Field Details - Data Attributes",
        "",
        "Keep only the fields required for the target action.",
    ])
    lines.extend(render_bullet_tree(data_tree or [tree_node("Payment status"), tree_node("Error code"), tree_node("Processed flag")]))
    lines.append("")
    lines.extend([
        "## Impacted Interfaces",
        "",
        "List only the systems touched by the new step.",
    ])
    lines.extend(list_block(deps or ["Epsilon", "Audit / case store"]))
    lines.append("")
    lines.extend([
        "## Specific Dev Tasks",
        "",
        "Rewrite the implementation work around the new action.",
    ])
    if is_contractual_definitions_step(request):
        lines.extend(render_bullet_tree([
            tree_node("Contractual-definition logic", business_tree or [tree_node("[TBD]")]),
            tree_node("Routing and dependencies", (workflow_tree or []) + (deps_tree or []) if (workflow_tree or deps_tree) else [tree_node("[TBD]")]),
            tree_node("Access controls", security_tree or [tree_node("[TBD]")]),
        ]))
        lines.append("- Remove later approval-step behavior from this step.")
    else:
        lines.extend(list_block(
            business_logic + workflow + deps + security + ["Remove assessment-only behavior from this step."]
        ))
    lines.append("")
    lines.extend([
        "## Testing Considerations and Hot Spots",
        "",
        "Focus tests on the behavior that changed.",
    ])
    if is_contractual_definitions_step(request):
        lines.extend(render_bullet_tree([tree_node("Benefit bucket coverage", [tree_node(item) for item in (testing or ["[TBD]"])])]))
    else:
        lines.extend(list_block(testing))
    lines.append("")
    lines.extend([
        "## Impacted Comms",
        "",
        "Keep only comms that are explicitly called out by the brief.",
    ])
    lines.extend(list_block(["[TBD]"]))
    lines.append("")
    lines.extend([
        "## Calculations",
        "",
        "Only include calculations if the brief introduces them.",
    ])
    lines.extend(list_block(["No calculation specified for this step."]))
    lines.append("")
    lines.extend([
        "## Security Considerations (Access & Routing)",
        "",
        "Use the access and routing rules from the brief, not the baseline role model.",
    ])
    lines.extend(list_block(security_lines))
    lines.append("")
    lines.append("## Unchanged Baseline Assumptions")
    lines.append("")
    lines.extend(list_block(unchanged_shell))
    lines.append("")
    lines.append("## Known Gaps / Questions")
    lines.append("")
    lines.extend(list_block(open_questions))
    lines.append("")
    lines.append("## Reviewer Checks")
    lines.append("")
    lines.extend(list_block(reviewer_checks))
    lines.append("")
    return "\n".join(lines)


def build_report(
    reference_title: str | None,
    reference_path: Path,
    brief_title: str,
    request: dict[str, str],
    delta_sections: dict[str, list[str]],
    unchanged: list[str],
    testing_hotspots: list[str],
    open_questions: list[str],
    reviewer_checks: list[str],
    ref_sections: dict[str, str],
) -> str:
    sections = [
        "1. Business Context",
        "2. Functional Requirements",
        "3. Technical Requirements",
        "4. Data Requirements",
        "5. Metrics & Calculations",
        "6. Business Rules",
        "7. Report Layout",
        "8. Acceptance Criteria",
        "9. Test Scenarios",
        "10. Integration & Dependencies",
    ]
    lines = [
        f"# {brief_title} - Draft",
        "",
        "## Draft Metadata",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| **Generated From** | {reference_title or reference_path.name} |",
        f"| **Requirement Archetype** | {request_value(request, 'Requirement Archetype', 'report or analytics requirement')} |",
        f"| **Jira / Tracking** | {request_value(request, 'Jira / Tracking Reference')} |",
        "",
    ]
    for section in sections:
        lines.append(f"## {section}")
        lines.append("")
        heading, body = match_reference_section(section, ref_sections)
        if body:
            lines.append(f"_Baseline reference: {heading}_")
            lines.append("")
            lines.append(body)
            lines.append("")
        if section == "2. Functional Requirements":
            lines.extend(list_block(delta_sections.get("business logic changes", []) + delta_sections.get("workflow routing changes", []) + delta_sections.get("data field changes", [])))
        elif section == "5. Metrics & Calculations":
            lines.extend(list_block(delta_sections.get("data field changes", []) + delta_sections.get("ui output changes", [])))
        elif section == "7. Report Layout":
            lines.extend(list_block(delta_sections.get("ui output changes", [])))
        elif section == "9. Test Scenarios":
            lines.extend(list_block(testing_hotspots))
        elif section == "10. Integration & Dependencies":
            lines.extend(list_block(delta_sections.get("dependency integration changes", [])))
        else:
            lines.append("- Review against the delta brief and update only if the change affects this section.")
        lines.append("")
    lines.append("## Unchanged Baseline Assumptions")
    lines.append("")
    lines.extend(list_block(unchanged))
    lines.append("")
    lines.append("## Known Gaps / Questions")
    lines.append("")
    lines.extend(list_block(open_questions))
    lines.append("")
    lines.append("## Reviewer Checks")
    lines.append("")
    lines.extend(list_block(reviewer_checks))
    lines.append("")
    return "\n".join(lines)


def bullets_from_kv_list(value: str) -> list[str]:
    if not value:
        return []
    parts = [part.strip() for part in value.split(";")]
    return [part for part in parts if part]


def parse_brief(path: Path) -> dict:
    title, sections = parse_markdown_sections(path.read_text())
    request = {key: " ".join(values) for key, values in keyed_bullets(sections.get("1. Request Summary", {}).get("body", [])).items()}
    closest_ref = keyed_bullets(sections.get("2. Closest Reference Artifact", {}).get("body", []))
    output_preference = keyed_bullets(sections.get("7. Output Preference", {}).get("body", []))
    delta_raw = sections.get("3. Delta to Apply", {}).get("children", {})
    delta_sections = {normalize(name): bullets(lines) for name, lines in delta_raw.items()}
    delta_trees = {normalize(name): bullet_tree(lines) for name, lines in delta_raw.items()}

    return {
        "title": title or path.stem,
        "request": request,
        "closest_ref": closest_ref,
        "delta_sections": delta_sections,
        "delta_trees": delta_trees,
        "unchanged": bullets(sections.get("4. Unchanged Baseline Assumptions", {}).get("body", [])),
        "testing_hotspots": bullets(sections.get("5. Testing Hot Spots Introduced by the Delta", {}).get("body", [])),
        "open_questions": bullets(sections.get("6. Known Gaps / Questions", {}).get("body", [])),
        "output_preference": output_preference,
        "reviewer_checks": bullets(sections.get("8. Reviewer Checks", {}).get("body", [])),
    }


def build_draft(reference_path: Path, brief_path: Path) -> str:
    brief = parse_brief(brief_path)
    reference_text = reference_path.read_text()
    reference_title, _ = parse_markdown_sections(reference_text, min_level=2, max_level=2)
    ref_sections = reference_sections(reference_text)
    archetype = brief["request"].get("requirement archetype", "").lower()
    title = brief["request"].get("requirement title", brief["title"])

    if "variance" in archetype:
        return build_variance_only(
            reference_title,
            reference_path,
            title,
            brief["request"],
            brief["closest_ref"],
            brief["delta_sections"],
            brief["unchanged"],
            brief["testing_hotspots"],
            brief["open_questions"],
            brief["output_preference"],
            brief["reviewer_checks"],
            ref_sections,
        )
    if "report" in archetype or "analytic" in archetype:
        return build_report(
            reference_title,
            reference_path,
            title,
            brief["request"],
            brief["delta_sections"],
            brief["unchanged"],
            brief["testing_hotspots"],
            brief["open_questions"],
            brief["reviewer_checks"],
            ref_sections,
        )
    return build_claim_step(
        reference_title,
        reference_path,
        title,
        brief["request"],
        brief["delta_sections"],
        brief["delta_trees"],
        brief["unchanged"],
        brief["testing_hotspots"],
        brief["open_questions"],
        brief["reviewer_checks"],
        ref_sections,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=Path, help="Signed-off reference requirement.")
    parser.add_argument("--brief", required=True, type=Path, help="Claims delta brief.")
    parser.add_argument("--output", required=True, type=Path, help="Output path for the generated draft.")
    args = parser.parse_args()

    draft = build_draft(args.reference, args.brief)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(draft)
    print(f"Wrote draft to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
