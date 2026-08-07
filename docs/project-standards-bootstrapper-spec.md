# Project Standards Bootstrapper: Build-Ready Specification

Status: implementation handoff

Owners: `dev-env-export` (engine, catalogue, templates, package policy, and standards payload) and Skill Hub (invocation and distribution skill)

Source: the resolved decisions in [Chart a safe project standards bootstrapper](https://github.com/ironicbuddha/skills-hub/issues/1)

## 1. Purpose

Build a repeatable project-standards bootstrapper that installs and verifies a selected repository baseline. It must initialize genuinely empty repositories and adopt standards into repositories with existing content without guessing ownership, overwriting unrelated work, or claiming success before every selected requirement is verified.

The bootstrapper is a verified-baseline installer, not a file copier or best-effort scaffold. A run succeeds only with the `verified` outcome.

## 2. Goals

- Represent desired repository intent as one Core Baseline, one or more composable Workloads, and optional scoped Capabilities.
- Give interactive and non-interactive callers the same schema, planning model, state machine, safety rules, and terminal outcomes.
- Produce deterministic, reviewable, state-bound plans before mutation.
- Preserve user-owned and unrelated content during Adoption Runs.
- Track current Managed Artifact ownership and verification in committed provenance.
- Make rerunning an unchanged configuration against an unchanged Verified Baseline a true no-op that still re-verifies the contract.
- Automate work when the caller already has authority and pause only when human identity, consent, secrets, billing, licence acceptance, organisation approval, SSO, or browser-only authority is required.
- Generate a substantive Project Delivery Contract, executable verification, and concise Agent Guidance Adapters for every selected repository shape.

## 3. Non-goals

- Machine provisioning or replacement of the machine bootstrap in `dev-env-export`.
- Personal identity, account login, credential creation, licence acceptance, or unrelated environment setup.
- Inferring durable intent from detected tools, repository resemblance, or legacy starter files.
- A compatibility shim, legacy migration mode, or deprecation window for the old starter.
- Generic support for providers whose artifacts and verification are not modelled in the catalogue.
- A global force, overwrite, skip, or best-effort mode.
- Storing secret values, hidden reasoning, candidate-generation logs, or creativity scores.

## 4. Normative domain model

Use the canonical vocabulary in `CONTEXT.md`.

- **Core Baseline**: exactly one mandatory, workload-independent standards layer.
- **Workload**: a stable instance with a unique ID, catalogue kind, exact repository-relative root, and fully resolved Policy Choices.
- **Capability**: an optional stable instance with an ID, catalogue kind, fully resolved Policy Choices, and repository, Workload, or declared cross-Workload scope.
- **Policy Choice**: a typed value owned by exactly one Core Baseline, Workload, or Capability. No choice floats independently.
- **Detected Repository State**: a fresh, read-only snapshot used as planning evidence for one run. It is not durable intent.
- **Planned Change**: one state-bound operation with target, owning layer, reason, precondition, verification, and recovery.
- **Conflict**: a contradiction between detected state and desired intent, or an inability to establish ownership for a required Planned Change. It blocks only the affected change.
- **Managed Artifact**: a whole file, link, or addressable structured fragment owned through provenance.
- **Manual Stage**: a resumable human-authority gate with instructions, expected evidence, and machine verification where possible.
- **Bootstrap Configuration**: the complete desired intent committed at `.project-standards/config.json`.
- **Provenance Manifest**: the current machine-owned ownership and verification ledger committed at `.project-standards/manifest.json`.
- **Verified Baseline**: a selected baseline whose complete installation, configuration, and verification contract passes.
- **Incomplete Result**: any required selected work that is unfinished or unverified, including a pending Manual Stage.
- **Initialization Run** and **Adoption Run**: explicit, run-local operating modes. They are never durable configuration.
- **Project Delivery Contract**: authoritative human-readable policy at `constitution.md`.
- **Agent Guidance Adapter**: concise agent entry point that routes to the Project Delivery Contract and adds only tool-specific operating guidance.
- **Runtime Rationale**: structured evidence for choosing a non-default runtime.
- **Selection Recipe**: wizard-only proposal that disappears when the complete Bootstrap Configuration is emitted.
- **Creative Review Policy**: observable quality contract for judgment-heavy work in a Markdown content Workload.

## 5. Configuration contract

### 5.1 Durable files

`.project-standards/config.json` contains only:

```json
{
  "$schema": "<schema URL>",
  "schemaVersion": "<exact schema version>",
  "catalogueVersion": "<exact catalogue version>",
  "core": {
    "kind": "core",
    "choices": {}
  },
  "workloads": [],
  "capabilities": [],
  "extensions": {}
}
```

Every object has a closed schema and rejects unknown fields. `extensions` is the only namespaced escape hatch. The resolved configuration materializes every accepted default. It must not contain mode, detection results, plans, conflicts, approvals, progress, run state, ownership, verification state, or secrets.

`.project-standards/manifest.json` contains:

- manifest schema version;
- configuration digest;
- catalogue and bootstrapper versions;
- optionally the verifying run ID for audit context;
- one entry per Managed Artifact with stable artifact ID, owning layer instance, target locator, ownership granularity, semantic or byte fingerprint, and last verification state.

The manifest is a current ledger, not an append-only log. It never depends on retained backups and never describes partial ownership.

### 5.2 Validation layers

JSON Schema validates closed structure, types, and required fields. The pinned catalogue additionally validates:

- supported kinds and stable IDs;
- unique Workload IDs and roots;
- Policy Choice values and resolved defaults;
- Capability scopes, cardinality, dependencies, and incompatibilities;
- nested-root composition contracts;
- artifact ownership and declared merge contracts;
- runtime-selection rules and Runtime Rationale requirements.

Two selected layers may target the same artifact only when the catalogue declares an explicit composition or merge contract. There is no implicit precedence. Schema-version changes use explicit migrations; catalogue or configuration versions never upgrade silently.

## 6. First-release selection matrix

### 6.1 Workloads

| Kind | Responsibility | Required shape choices | Intrinsic verification |
| --- | --- | --- | --- |
| `next-web` | One Next.js app, including rendering, Server Actions, route handlers, and small BFF logic | Exact root and package/runtime choices | format, lint, typecheck, tests, build |
| `vite-web` | One Vite frontend app | Exact root and package/runtime choices | format, lint, typecheck, tests, build |
| `node-service` | One independently deployable TypeScript backend unit | `http-service`, `function`, `worker`, or `scheduled-job` | format, lint, typecheck, tests, build/package |
| `typescript-package` | TypeScript library, CLI, or reusable tooling package | Package boundary and runtime choices | format, lint, typecheck, tests, package check |
| `python-workload` | One Python script, library, worker, scheduled job, or service | `script`, `library`, `worker`, `scheduled-job`, or `service`; service-like shapes require Runtime Rationale | format, lint, typecheck where selected, tests, package/build check |
| `markdown-content` | Authored Markdown as a primary deliverable | Content root and factual-validation command | format, lint, links, factual validation |

Every Workload has a unique stable ID and exact root. Duplicate roots are invalid. Nested roots require a catalogue-declared ownership contract. Multiple web Workloads are separate applications. Independently deployable APIs, workers, queues, substantial persistence logic, and non-web consumers are separate service Workloads.

The default frontend/backend composition is a web Workload plus `node-service`. A Python service may replace or accompany it only with a Runtime Rationale containing the default alternative considered, concrete constraint, material benefit, accepted operational trade-offs, and review trigger. Preference alone is invalid.

### 6.2 Capabilities

| Kind | Scope/cardinality | Selection rule |
| --- | --- | --- |
| `tdd` | repository-wide or selected executable Workloads | Preselect for new executable repositories |
| `github-repository` | repository singleton | Preselect; human confirms remote settings |
| `github-actions-ci` | repository singleton | Preselect when GitHub support is accepted; depends on it |
| `vercel-deployment` | Workload | Recommend for Next.js/Vite deployable shapes |
| `aws-deployment` | Workload | Recommend for Node and deployable Python shapes |
| `vercel-services-experimental` | cross-Workload singleton | Explicit opt-in only; qualifying Next.js/FastAPI topology |
| `persistence` | Workload | Explicit selection |
| `authentication` | Workload | Explicit selection |
| `observability` | Workload | Required for production services, workers, and scheduled jobs |
| `public-interface` | Workload | Recommend for HTTP/API shapes; require confirmation |
| `secret-management` | repository-wide or Workload | Required wherever secrets are used |
| `creative-markdown` | Workload | Explicit selection; requires `markdown-content` |

Multiple deployment Capabilities may target one Workload only for distinct named environments or purposes. Two providers claiming the same environment are incompatible. Cross-Workload Capabilities identify Workloads by ID and never infer topology.

### 6.3 Selection Recipes

The wizard may propose recipes for Next.js web app, Vite web app, TypeScript service, Next.js plus Node service, Python automation, and Markdown content repository. A recipe visibly expands to proposed instances and choices, remains fully editable, and is absent from durable configuration. Python backend and experimental Vercel Services are never recipe defaults.

## 7. Package, repository, CI, test, and deployment policies

### 7.1 Package and runtime defaults

- New TypeScript and Markdown package boundaries use pnpm, exactly pinned in `package.json#packageManager` and activated by Corepack.
- Node is exactly pinned in `.nvmrc`; `package.json#engines.node` declares compatibility.
- New Python Workloads use uv, `.python-version`, and committed `uv.lock`.
- Lockfiles are mandatory and CI installs are frozen/immutable.
- Adoption preserves compatible pnpm, npm, Yarn, Bun, or uv arrangements unless package-manager migration is explicitly selected.
- Package-manager and runtime ownership is per package boundary or Workload. Layers sharing a boundary must agree; isolated pnpm and uv roots may coexist.
- Renovate or Dependabot may propose upgrades, but accepted upgrades are explicit configuration migrations.

### 7.2 GitHub and CI defaults

`github-repository` may create or connect a repository only after confirming owner, name, visibility, and remote. It can configure default branch, merge strategy, automatic deletion of merged branches, topics, and a baseline ruleset. The first-release solo default permits direct pushes to `main`; pull requests and required reviews are stricter selectable choices. Compatible existing controls are preserved; weakening them is a Conflict.

`github-actions-ci` composes Workload verification into separate stable-named jobs. It runs for every direct push to `main`, uses frozen installs, least-privilege permissions, concurrency cancellation, timeouts, no secret access for untrusted pull requests, and third-party actions pinned to full commit SHAs. Production deployment waits for all required jobs for the exact commit.

### 7.3 TDD

For scoped executable Workloads, observable behavior changes follow red-green-refactor; bug fixes begin with a reproducing failing test; refactors remain green. Tests target public behavior at the narrowest reliable boundary, with integration tests wherever correctness depends on framework wiring, filesystems, networks, databases, or cross-Workload contracts. Documentation-only changes, formatting, generated artifacts, and explicitly labelled throwaway prototypes are exempt. There is no universal coverage percentage.

### 7.4 Deployment

Vercel and AWS production deployment proceeds from successful GitHub Actions CI for the exact commit. Preview and lower-environment deployments are optional. AWS uses least-privilege OIDC, never long-lived access keys. Each deployment declares artifact identity, environment mapping, smoke check, rollback/recovery, and status reporting.

Experimental Vercel Services is limited to one Vercel project with isolated `frontend/` and `backend/` roots, root `vercel.json`, current `services` schema, and ordered rewrites exposing `/api/**` before the frontend catch-all. Preflight team entitlement and CLI/schema support. Support only the documented FastAPI preset initially; never fall back to `experimentalServices`. Expose Function constraints, including external durable state, bounded requests, 4.5 MB bodies, Python bundles, and usage costs. Preserve native isolated dev commands alongside `vercel dev`, and offer split projects or Vercel frontend plus external Python as supported fallbacks.

## 8. Managed Artifact contract

### 8.1 Core artifacts

- `constitution.md`: wholly managed after creation or explicit adoption; the authoritative Project Delivery Contract.
- `AGENTS.md`: wholly managed when newly created; otherwise only an identifiable managed section is owned.
- `README.md`: only an identifiable managed links section is owned.
- `CLAUDE.md`: created only when selected or already present; routes to `AGENTS.md` and `constitution.md`.
- Nested `AGENTS.md`: only for a subtree with genuinely different commands or constraints; inherits and cannot override the root contract.
- `.project-standards/config.json`: complete committed intent, promoted only on verification.
- `.project-standards/manifest.json`: complete committed provenance, promoted atomically with configuration.

Selected Workloads and Capabilities add package files, lockfiles, tool configurations, CI workflows, deployment configuration, environment examples, and documentation identified by stable catalogue artifact IDs. Ownership must be whole-file or a catalogue-declared structured fragment.

### 8.2 Constitution composition

The Core Baseline supplies invariant policy for code and dependencies, testing expectations, delivery gates, security and secrets, documentation, narrow changes, and preservation of unrelated work. Workloads add runtime tooling, commands, test layers, build rules, and delivery guidance. Capabilities add selected cross-cutting policy. The rendered constitution contains no unused alternatives, addenda, or placeholders.

Agent Guidance Adapters route to the constitution and command/docs locations, require nested guidance, preserve unrelated work, state secret and external-authority boundaries, and link domain/architecture docs when present. They do not duplicate coding or testing policy, and no adapter filename has precedence.

The managed README section links to the constitution, local setup, and verification. Deployable Workloads additionally require environment, deployment, rollback/recovery, and troubleshooting guidance. Public interfaces require interface documentation. Domain and ADR links are included where applicable. Empty placeholders do not satisfy the contract.

### 8.3 Creative Markdown

The `creative-markdown` Capability adds a Workload-scoped Creative Review Policy to `constitution.md` and a managed `docs/standards/creative-review.md`. It applies to ideation, substantive editorial structure, framing, naming, requirements analysis, and synthesis. It excludes extraction, citation handling, lint/format/link fixes, templated updates, typo correction, and other mechanical transformations unless alternatives are requested.

Facts are established first; exploration may change framing and expression but not sourced facts, quotations, citations, confidence, or uncertainty. Internal candidate exploration may be used, but candidate transcripts, scoring, probability estimates, chain-of-thought, and attestations are never required or stored. There is no durable creativity-intensity choice. Validation checks only observable content, links, commands, placeholders, scope, and non-contradiction; it never scores creativity.

## 9. Run modes and inspection

The caller selects an exact root and explicitly confirms `initialize` or `adopt`. Inspection may recommend but never choose or switch the mode.

Initialization is eligible only when the root contains Git administrative metadata, empty directories or conventional placeholders, ignorable OS/editor metadata that remains untouched, and optionally a wholly empty initial commit. Any substantive file or symlink requires Adoption. Unexpected content invalidates an initialization plan and requires replanning.

Operate on the exact selected root; never redirect to a parent Git root. Git initialization requires confirmation. Inspection fingerprints root identity and covers symlinks, submodules, worktrees, nested repositories, case collisions, filesystem boundaries, traversal, normalization ambiguity, special files, and type changes. Targets remain inside the root unless a selected Capability explicitly owns an external target. Symlinks are not followed for mutation by default. Nested repositories, submodules, and unrelated dirty state are separate ownership boundaries.

All existing Adoption content begins user-owned. Compatible content may be adopted explicitly; structured merges require catalogue ownership boundaries; contradictions or ambiguous ownership are Conflicts. Previously applied legacy starter output receives no detection, reconstruction, or special treatment.

## 10. Planning, conflict, and approval contract

Each Planned Change uses exactly one strategy:

- `create`: create an absent target;
- `adopt`: claim compatible existing content without mutation;
- `merge`: change only a catalogue-declared structured fragment;
- `replace`: replace the reviewed target after backup;
- `satisfied`: verified state already fulfils the requirement;
- `defer`: make no change; if required, the result is Incomplete.

The plan records target, owner, reason, precondition fingerprints, semantic/textual diff, verification, reversibility, backup, and recovery. Secret-bearing diffs are redacted without weakening fingerprints. Planning may continue around Conflicts, but execution starts only after every Conflict in the reviewed plan has a structured resolution. Removing or deferring selected scope requires replanning.

One final confirmation authorizes the exact resolved plan. Destructive replacement and destructive merge also require per-change approval. Additive declared merges may use overall approval. Drift or any plan change voids affected authorization. There is no wildcard approval or durable overwrite preference.

## 11. Execution, recovery, and idempotency

Before mutation, create gitignored `.project-standards/runs/<run-id>/` state containing plan, fingerprints, logs, candidate configuration/provenance, progress, immutable backups, and recovery report. Back up immediately before each actual mutation, preserving bytes, type, permissions, and restoration metadata under restrictive permissions. Never log or commit backup contents. Absent and satisfied targets create no backup.

Prepare file changes in temporary storage, validate, and promote atomically where possible. On failure, restore all reversible mutations from that execution in reverse order without Git reset/checkout and without touching unrelated work. Remote writes, package installs, migrations, and human-authority actions are declared potentially non-reversible, scheduled late, separately confirmed, and given recovery instructions. Incomplete restoration yields `incomplete` with exact manual steps.

Successful run directories remain until explicit cleanup. Cleanup refuses active/Incomplete runs and the only recovery path. Only one mutating run may be active. Signals and crashes never promote candidate configuration or provenance. Cancellation before mutation discards the candidate run; during mutation it rolls back immediately or on resume.

A Manual Stage may preserve candidate state while paused. It records exact instructions, resume point, expected evidence, and abandonment/recovery command. Resume re-inspects relevant state and replans on drift.

For the same Bootstrap Configuration and unchanged Verified Baseline, rerun performs no writes, installs, backups, manifest churn, or Manual Stages. It re-verifies and reports requirements as satisfied. Semantic normalization is used only where declared. Managed drift, surrounding user changes, version changes, and intent changes are reported distinctly.

## 12. Interactive journey and captured values

The wizard uses ten guided-choice stages:

| Stage | Human journey | Captured values/evidence |
| --- | --- | --- |
| 1. Inspect | Select exact root; review detected facts and boundaries | root identity and Detected Repository State fingerprints |
| 2. Choose mode | Review recommendation and exact eligibility evidence | explicit `initialize` or `adopt` for this run |
| 3. Select shape | Optionally choose a Selection Recipe; inspect expanded proposal | proposed Workload and Capability instances |
| 4. Resolve intent | Review every visible default, dependency, choice, and rationale | complete Bootstrap Configuration candidate and Runtime Rationale where required |
| 5. Review plan | Inspect ownership, diffs, Conflicts, verification, reversibility, and recovery | state-bound Planned Changes and Conflict resolutions |
| 6. Authorize | Confirm the exact plan; separately approve destructive merge/replace | plan fingerprint and scoped approvals |
| 7. Execute | Allow deterministic local and authenticated API operations | progress, operation evidence, backups, and API results |
| 8. Manual authority | Follow exact URL/CLI instructions only where human authority is required | non-sensitive Secret References and verifiable resulting evidence; never secret values |
| 9. Verify | Review every selected contract check | check results and candidate provenance |
| 10. Finish | Review terminal outcome, changes, checks, recovery retention, and next commands | final report and, only if verified, promoted config/manifest |

Each stage first shows a recommendation, reason, relevant choices, and consequence. Details are progressively disclosed at their review gate. Going back is safe before execution. The wizard may open exact URLs or show CLI paths but must not invent provider journeys or treat acknowledgement as evidence.

## 13. CLI behavior

The implementation may choose the executable name, but it must expose these semantic operations consistently in interactive and automation modes:

- `inspect <root>`: read-only Detected Repository State and mode recommendation.
- `plan <root>`: interactive intent resolution by default; automation accepts an explicit mode and complete config, then emits a fingerprinted plan without mutation.
- `apply <plan>`: execute only the exact approved plan; automation supplies structured fingerprint-bound approvals, never `--yes` or `--force`.
- `resume <run-id>`: re-inspect and continue a paused Manual Stage or recover an interrupted execution.
- `verify <root>`: verify the committed configuration and manifest without changing intent.
- `status <root|run-id>`: show active run, outcome, pending stage, drift, and recovery state.
- `recover <run-id>`: restore reversible mutations or print exact remaining manual recovery.
- `abandon <run-id>`: discard pre-mutation work or recover candidate mutations before abandonment.
- `cleanup <run-id>`: remove retained run material only when safe.

Machine-readable output includes schema version, run ID, mode, plan/configuration digests, terminal outcome, checks, changes, pending Manual Stage, recovery state, and exact next commands. Human output uses the same facts. Exit status distinguishes `verified`, `incomplete`, `failed`, and `cancelled`; only `verified` returns success. Missing authority, credentials, connectivity, or evidence is `incomplete`, not warning-success.

## 14. Verification and acceptance criteria

A run is `verified` only when all of the following hold:

1. Configuration and provenance validate against their pinned schemas and catalogue.
2. Every Planned Change postcondition passes and no Conflict remains unresolved.
3. Every Managed Artifact or fragment has a stable identity, owner, locator, and matching semantic/byte fingerprint.
4. User-owned surrounding and unrelated content is preserved.
5. `constitution.md` contains every selected requirement, no unselected material, and no unresolved placeholder.
6. Agent Guidance Adapters route to the Project Delivery Contract and do not contradict or duplicate it.
7. Managed links resolve to substantive documents and referenced commands exist.
8. Package managers, exact runtime pins, and lockfiles are internally consistent; immutable installation succeeds where selected.
9. Every Workload's format, lint, applicable typecheck, tests/content checks, and build/package checks pass.
10. Every selected Capability passes its deterministic checks and required Manual Stage evidence.
11. Deployment Capabilities establish artifact identity, environment mapping, smoke verification, recovery, and status reporting.
12. No unexplained managed drift, ownership ambiguity, or state drift remains.
13. Candidate `.project-standards/config.json` and `.project-standards/manifest.json` are promoted together only after all checks pass.
14. A repeated run against the unchanged Verified Baseline is a write-free no-op and returns `verified` after re-verification.
15. Failure, cancellation, and interruption tests prove rollback/recovery without changing unrelated work or promoting partial provenance.

First-release acceptance must include fixtures for eligible empty roots; substantive roots; dirty worktrees; symlinks and nested repositories; existing compatible, complementary, contradictory, and ambiguous artifacts; each Workload; valid and invalid Capability compositions; Python Runtime Rationale; structured fragments; drift between plan and apply; interrupted execution; incomplete Manual Stages; secret redaction; and unchanged reruns.

## 15. Migration and cutover

The legacy `scripts/13-apply-project-standards.sh`, Skill Hub `apply-project-standards`, and Skill Hub `agentic-delivery-loop` are archived immediately as part of successor rollout. Remove them from active catalogues, installers, profiles, and current documentation. Git history is the archive; provide no executable shim or deprecation window.

A repository touched by the old starter uses an ordinary Adoption Run. Inspection considers current state only, never historical fingerprints or inferred legacy profiles. Every artifact remains user-owned until the reviewed plan explicitly adopts, merges, or replaces it. Provenance begins only after a Verified Baseline.

## 16. Repository ownership boundary

`dev-env-export` owns:

- bootstrapper engine and CLI;
- configuration, manifest, plan, run-state, and machine-output schemas;
- versioned catalogue, dependency/composition rules, and migrations;
- templates, renderers, managed-fragment contracts, package/runtime policy, provider operations, and verification checks;
- recovery machinery, tests, documentation, and release/cutover work.

Skill Hub owns:

- one thin successor invocation/distribution skill;
- guidance for locating and invoking the `dev-env-export` implementation;
- removal of the two legacy skills from active discovery.

Skill Hub must not duplicate templates, policy payload, catalogue data, schemas, or implementation logic.

## 17. Ordered implementation handoff

Implement as tracer bullets in this order; each ticket must leave its slice executable and tested before the next begins.

1. **Establish schemas, catalogue, and domain validation** — Implement versioned configuration/manifest schemas, stable layer IDs, catalogue validation, Policy Choice resolution, composition rules, and representative fixtures.
2. **Build exact-root inspection and mode eligibility** — Fingerprint the root and relevant filesystem/Git state; detect boundaries and hazards; recommend but require explicit run mode.
3. **Build deterministic planning and ownership-aware diffs** — Produce stable Planned Changes, closed strategies, Conflict records, fragment ownership, redacted review output, and plan fingerprints without mutation.
4. **Build run storage, atomic file execution, and recovery** — Add run locking, restrictive run directories, backups, staged writes, reverse rollback, interruption recovery, cleanup guards, and cancellation semantics.
5. **Render and verify the Core Baseline** — Generate/adopt `constitution.md`, adapters, README links, configuration, provenance, and substantive documentation checks with precise ownership.
6. **Add Workload catalogue slices** — Implement the six Workloads, intrinsic package/runtime/tooling artifacts, exact pins, lockfiles, and executable verification contracts.
7. **Add local policy Capabilities** — Implement TDD, persistence, authentication, observability, public-interface, secret-management, and creative-markdown composition and verification.
8. **Add GitHub repository and CI Capabilities** — Implement authenticated operations, state comparison, least-privilege CI composition, full-SHA actions, stable checks, Manual Stages, and Conflict handling.
9. **Add deployment Capabilities** — Implement Vercel and AWS verified deployment contracts, then the separately gated experimental Vercel Services topology and preflights.
10. **Build the interactive and non-interactive front ends** — Deliver the ten-stage guided wizard, plan/apply separation, structured approvals, resume/status/recover flows, machine-readable parity, and outcome-specific exits.
11. **Prove end-to-end safety and no-op behavior** — Run the complete acceptance fixture matrix, fault injection, drift tests, rollback checks, secret-redaction tests, and byte/semantic no-op assertions.
12. **Cut over distribution and archive legacy entry points** — Publish the thin Skill Hub successor, update active documentation/installers, archive the old script and both named skills, and execute Adoption Run smoke tests against representative legacy-touched repositories.

The handoff is complete when every ticket above has explicit dependencies, acceptance tests derived from section 14, and named ownership in the appropriate repository. Implementation must not reopen a resolved product decision merely to make sequencing convenient; any genuine contradiction must be raised against this specification and its linked decision record.
