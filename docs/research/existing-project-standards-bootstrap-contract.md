# Existing project-standards bootstrap contract

Research note for the Wayfinder investigation **Distill the existing standards
bootstrap contract**. This note examines only primary local sources in
`skills-hub` and its related `dev-env-export` repository. It describes the
observable contract a future project-standards bootstrapper must consciously
preserve, replace, or retire; it does not propose an implementation.

## Executive conclusion

The current bootstrapper is not a project generator. It is a conservative
standards overlay with two outputs:

1. a profile-rendered `constitution.md` that states the intended engineering
   policy; and
2. a small set of agent-direction and lint/format artifacts merged or copied
   into an existing repository.

Its strongest contract is safety around pre-existing files: normal operation
does not overwrite them, repeated identical application is a no-op, and forceful
replacement backs up file and symlink targets. Its weakest contract is
completion: success can include skipped or unapplied configuration, it does not
install dependencies or create most promised test/build/CI machinery, and its
tests cover only a narrow Markdown/agent-direction slice.

The successor should therefore preserve the policy vocabulary and conservative
ownership boundary, replace the partial/ambiguous completion model with an
explicit plan-and-result contract, and retire only those details that are
deliberately superseded (notably template sediment and machine-specific version
defaults).

## Policies that constitute the baseline

### Preserve as policy, while allowing explicit exceptions

- **TypeScript-first, Python-by-justification.** Application and service repos
  default to TypeScript strict mode; Python is intended mainly for scripting,
  automation, or materially better library support. Markdown-only repos are a
  first-class exception rather than being forced through an application
  profile. This stance is stated in the baseline and repeated in the generated
  constitution
  ([`PROJECT-STANDARDS.md` lines 15-35](https://github.com/ironicbuddha/dev-env-export/blob/main/PROJECT-STANDARDS.md#L15-L35),
  [`constitution.md` lines 29-42](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/project-standards/constitution.md#L29-L42)).

- **One reproducible project toolchain.** A repo should commit one package
  manager and lockfile per package boundary, pin runtime versions, and define
  repo-local quality commands; machine-global quality tools are explicitly not
  the source of truth
  ([`PROJECT-STANDARDS.md` lines 37-55](https://github.com/ironicbuddha/dev-env-export/blob/main/PROJECT-STANDARDS.md#L37-L55)).

- **Testing proportional to risk and interface.** Unit tests cover business
  logic, integration tests cover storage/auth/third-party boundaries, end-to-end
  tests cover critical flows, and contract tests cover public interfaces. The
  default application/service coverage target is 80%, but high-risk paths need
  direct tests regardless of aggregate coverage
  ([`PROJECT-STANDARDS.md` lines 57-97](https://github.com/ironicbuddha/dev-env-export/blob/main/PROJECT-STANDARDS.md#L57-L97),
  [`constitution.md` lines 44-54](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/project-standards/constitution.md#L44-L54)).

- **Delivery is an owned, recoverable system.** Local setup must be repeatable;
  deploys, builds, environment configuration, and migrations must be versioned;
  deployable systems require a non-production environment and a rollback or
  recovery path. Vercel is the default for Next.js frontends and AWS for backend
  workloads, subject to documented deviation
  ([`PROJECT-STANDARDS.md` lines 99-130](https://github.com/ironicbuddha/dev-env-export/blob/main/PROJECT-STANDARDS.md#L99-L130)).

- **Security is day-one policy.** Secrets belong in 1Password or platform secret
  stores, never Git; input/config boundaries are validated; auth is documented;
  production access is least-privilege; logs exclude secrets; and dependency or
  platform vulnerability scanning is enabled
  ([`PROJECT-STANDARDS.md` lines 132-152](https://github.com/ironicbuddha/dev-env-export/blob/main/PROJECT-STANDARDS.md#L132-L152)).

- **Operability and documentation are part of the contract.** Running systems
  should have structured logs, health/readiness checks where relevant, error
  tracking, traceable identifiers, and visible failure reporting. Repos should
  document setup, test, deploy, secrets/environment flow, and meaningful
  architectural decisions
  ([`PROJECT-STANDARDS.md` lines 154-179](https://github.com/ironicbuddha/dev-env-export/blob/main/PROJECT-STANDARDS.md#L154-L179)).

- **Quality gates vary by repository shape.** Application/service merge gates
  include lint, format checking, tests, build, typecheck where applicable, and
  high-severity security status. Markdown-only repos require only `lint` and
  `format:check` until executable code appears
  ([`PROJECT-STANDARDS.md` lines 181-199](https://github.com/ironicbuddha/dev-env-export/blob/main/PROJECT-STANDARDS.md#L181-L199)).

- **Deviation is allowed but explicit.** The generated contract asks a repo to
  record what differs, why, and the compensating control. This is a useful
  escape hatch that keeps standards opinionated without pretending every profile
  fits every project
  ([`constitution.md` lines 163-175](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/project-standards/constitution.md#L163-L175)).

### Preserve the intent, but make versions and platforms updateable inputs

The current defaults encode Node `24.18.0` LTS, Next.js `16.2.10`, `pnpm` for
TypeScript/Markdown, `uv` for Python, Vercel for Next.js, and AWS for backend
workloads
([`templates/project-standards/README.md` lines 5-13](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/project-standards/README.md#L5-L13)).
Those choices are policy snapshots, not timeless bootstrap mechanics. A future
bootstrapper should preserve the principle of explicit, pinned, profile-owned
defaults while sourcing the actual versions from one maintainable catalogue.

## Artifacts and observable behavior

### Profile contract

The command requires both `--repo` and one of six profiles: `next`, `vite`,
`ts-service`, `python`, `markdown`, or `mixed`. It also accepts `--dry-run`,
`--force`, and `--constitution-only`
([`13-apply-project-standards.sh` lines 27-61](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L27-L61),
[`13-apply-project-standards.sh` lines 561-608](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L561-L608)).
The Skill Hub invocation contract mirrors five of those profiles but omits
`markdown` from its description and profile list, an existing documentation
drift a successor must correct rather than preserve
([`apply-project-standards/SKILL.md` lines 1-3](../../skills/apply-project-standards/SKILL.md#L1-L3),
[`apply-project-standards/SKILL.md` lines 32-42](../../skills/apply-project-standards/SKILL.md#L32-L42)).

Each profile renders the same constitution template with concrete project type,
language, frontend/backend shape, package manager, deployment target, data
sensitivity, runtime versions, version `0.1.0`, and the current date
([`13-apply-project-standards.sh` lines 171-244](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L171-L244),
[`13-apply-project-standards.sh` lines 246-303](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L246-L303)).
All profile addenda remain in the output and the operator must delete the ones
that do not apply
([`constitution.md` lines 108-161](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/project-standards/constitution.md#L108-L161)).

### Artifact matrix

| Profile | Policy/agent artifacts | Quality artifacts and merge behavior |
| --- | --- | --- |
| All | Rendered `constitution.md`; unless constitution-only, a concise `AGENTS.md` and relative `CLAUDE.md -> AGENTS.md` link ([script lines 621-641](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L621-L641)) | Profile-specific rows below |
| `next`, `vite`, `ts-service` | Common artifacts | Prettier config/ignore, Markdownlint, ESLint, Stylelint; missing scripts and devDependencies from `package.quality.json` are merged into an existing `package.json` ([script lines 469-478](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L469-L478), [`package.quality.json`](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/code-quality/package.quality.json)) |
| `markdown` | Common artifacts | Prettier config/ignore and Markdownlint; creates the Markdown `package.json` if absent or merges its scripts/dependencies if present ([script lines 480-494](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L480-L494), [`package.markdown.json`](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/code-quality/package.markdown.json)) |
| `python` | Common artifacts | Markdownlint; creates or extends `pyproject.toml` with Ruff configuration; writes a Ruff `Makefile`, falling back to `Makefile.python` when a foreign Makefile exists ([script lines 410-467](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L410-L467)) |
| `mixed` | Common artifacts | Applies both the TypeScript and Python baselines ([script lines 627-641](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L627-L641)) |

The agent starter deliberately stays short, points agents to `constitution.md`,
requires narrow tested changes and preservation of unrelated work, protects
secrets, and asks before external-authority or scope-expanding actions
([`agent-direction/AGENTS.md`](https://github.com/ironicbuddha/dev-env-export/blob/main/agent-direction/AGENTS.md)).
Specialised agent workflows are intentionally kept in Skill Hub rather than
copied into every repository
([`carlo-baseline-refresh-plan.md` lines 158-164](https://github.com/ironicbuddha/dev-env-export/blob/main/docs/plans/carlo-baseline-refresh-plan.md#L158-L164)).

### Safety and ownership guarantees to preserve

- Target input must be an existing directory. If it is inside a Git working
  tree, the applicator resolves it to the repository top level; otherwise it
  uses the directory itself
  ([`13-apply-project-standards.sh` lines 81-96](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L81-L96)).

- Default writes are non-overwriting. An identical file or correct symlink is
  retained; any other existing destination is skipped with a warning. `--force`
  moves an existing file, directory, or symlink to a timestamped sibling backup
  before replacement
  ([`13-apply-project-standards.sh` lines 98-169](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L98-L169)).

- Package JSON merging is additive by default: existing script and dependency
  keys win, and only missing keys are supplied. With `--force`, template keys
  win
  ([`13-apply-project-standards.sh` lines 340-408](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L340-L408)).

- Dry-run records intended writes/merges without mutating destinations. The
  normal output separates applied, skipped, and warning items, then prints manual
  next steps
  ([`13-apply-project-standards.sh` lines 513-559](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L513-L559)).

- Relative `CLAUDE.md -> AGENTS.md` is the canonical projection, with a plain
  copy documented for tools/filesystems that do not support symlinks
  ([`README.md` lines 387-398](https://github.com/ironicbuddha/dev-env-export/blob/main/README.md#L387-L398)).
  This was an intentional 2026-07-24 simplification from two copied long-form
  policies to one concise source of truth, captured in commit
  [`c91cbf7`](https://github.com/ironicbuddha/dev-env-export/commit/c91cbf70d98d2eee04399fcbc3a5bec905742ea3).

- The contract test locks three behaviors: initial agent-direction creation,
  idempotent preservation of the relative link, and refusal to replace a foreign
  `CLAUDE.md` without force
  ([`project_standards_contract_test.sh` lines 25-49](https://github.com/ironicbuddha/dev-env-export/blob/main/tests/project_standards_contract_test.sh#L25-L49)).

## Known shortcomings the successor must resolve explicitly

These are observable limitations, not necessarily bugs. Each needs a deliberate
preserve/replace/retire decision.

1. **“Applied” does not mean the baseline is operational.** The script neither
   installs dependencies nor creates `test`, `build`, `typecheck`, CI,
   deployment, secret-template, or observability artifacts. Its own next-step
   summary tells the operator to install tooling and add missing scripts, while
   the starter README separately requires CI and a non-secret environment
   template
   ([script lines 545-558](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L545-L558),
   [`templates/project-standards/README.md` lines 20-44](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/project-standards/README.md#L20-L44)).
   Replace the ambiguous success concept with an explicit distinction between
   generated, merged, skipped, verified, and still-required work.

2. **Warnings and skipped essentials still exit successfully.** Missing
   `package.json`, missing `jq`, foreign config files, and absent agent-direction
   source files are recorded as skips/warnings, but there is no incomplete exit
   state or machine-readable result
   ([script lines 340-355](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L340-L355),
   [script lines 496-511](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L496-L511),
   [script lines 513-559](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L513-L559)).
   A future contract should say which omissions are acceptable, which make the
   run incomplete, and how automation consumes the result.

3. **Force is too coarse and inconsistently recoverable.** `--force` authorizes
   every file replacement and every package-script/dependency collision at once.
   File targets are backed up, but `package.json` is rewritten from a temporary
   result without first creating a backup
   ([script lines 103-135](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L103-L135),
   [script lines 360-407](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L360-L407)).
   Preserve recoverability, but replace global force with explicit per-artifact
   conflict choices or another ownership-aware mechanism.

4. **Profile rendering is only partially profile-specific.** The script fills
   profile metadata but leaves every addendum in place and assigns all profiles
   the same moderate data sensitivity. Manual trimming and completion remain
   mandatory
   ([script lines 171-244](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L171-L244),
   [`constitution.md` lines 15-27](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/project-standards/constitution.md#L15-L27)).
   Replace this with either truly selected sections or an explicit, validated
   interactive tailoring phase; do not silently claim a fully tailored output.

5. **Policy and artifact behaviour drift.** The Skill Hub skill omits the
   supported `markdown` profile. The Python starter guidance mentions Prettier
   for meaningful docs, while the Python applicator installs Markdownlint only.
   The Vite renderer records deployment as `other`, while the wider baseline
   names Vercel or S3/CDN as usual choices
   ([`apply-project-standards/SKILL.md` lines 32-42](../../skills/apply-project-standards/SKILL.md#L32-L42),
   [`templates/code-quality/README.md` lines 17-27](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/code-quality/README.md#L17-L27),
   [script lines 195-203](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L195-L203),
   [`PROJECT-STANDARDS.md` lines 233-245](https://github.com/ironicbuddha/dev-env-export/blob/main/PROJECT-STANDARDS.md#L233-L245)).
   Replace duplicated profile declarations with a single source of truth.

6. **The tests define only a sliver of the contract.** The sole focused test
   exercises Markdown application and `CLAUDE.md` conflict behavior. It does not
   cover all profile matrices, rendered values, `--dry-run`, `--force` and
   backups, `--constitution-only`, additive/forced JSON merges, Python merging,
   missing prerequisites, output/exit semantics, or Git-root resolution
   ([`project_standards_contract_test.sh`](https://github.com/ironicbuddha/dev-env-export/blob/main/tests/project_standards_contract_test.sh)).
   Preserve the three locked behaviors, but replace the test surface with
   contract coverage for every promised mode and safety boundary.

7. **Target resolution can surprise monorepo users.** Passing any subdirectory
   of a Git repository silently redirects all writes to the Git top level
   ([script lines 81-96](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L81-L96)).
   A successor must explicitly choose whether standards are root-only, package-
   scoped, or both, and must preview the resolved target before mutation.

8. **Template freshness has no provenance inside generated repos.** The output
   records a static constitution version and current dates, but no source commit,
   profile schema version, managed-artifact manifest, or safe upgrade path
   ([`constitution.md` lines 171-175](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/project-standards/constitution.md#L171-L175),
   [script lines 285-303](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L285-L303)).
   If future runs are expected to update an established repo, replace blind
   copy/merge semantics with provenance and ownership. If upgrades remain out of
   scope, state that explicitly and retire any implication of lifecycle
   management.

9. **Generated policy contains deliberate placeholders and sediment.** The
   release flow remains unrendered; all irrelevant addenda remain; and a rerun on
   a later date produces a different candidate constitution but skips the
   existing one unless forced
   ([`constitution.md` lines 56-65](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/project-standards/constitution.md#L56-L65),
   [`constitution.md` lines 108-175](https://github.com/ironicbuddha/dev-env-export/blob/main/templates/project-standards/constitution.md#L108-L175),
   [script lines 306-338](https://github.com/ironicbuddha/dev-env-export/blob/main/scripts/13-apply-project-standards.sh#L306-L338)).
   Retire unused sections and unresolved placeholders from final output, or make
   an explicit draft state part of the contract.

## Preserve, replace, retire decision ledger

### Preserve

- Six recognizable project shapes, including Markdown-only and mixed repos.
- A short repo-local delivery contract covering quality, testing, delivery,
  security, operations, documentation, exceptions, and versioning.
- Repo-local quality tools and explicit runtime/package-manager choices.
- Non-overwriting default behavior, idempotent identical reruns, dry-run preview,
  and recoverable conflict handling.
- One canonical `AGENTS.md` with a relative Claude projection and a copy fallback.
- Deliberate separation between universal agent guidance and specialised Skill
  Hub workflows.

### Replace

- Duplicated profile declarations with one versioned profile catalogue.
- Best-effort success with explicit result states and verification.
- Global `--force` with granular, ownership-aware conflict resolution and backup
  parity for structured-file merges.
- Unpruned, placeholder-bearing constitutions with genuinely tailored or clearly
  draft output.
- Manual dependency/config follow-through with a declared boundary: either
  perform and verify it, or emit a complete machine-readable handoff.
- Narrow Markdown-only testing with full profile, conflict, rerun, and failure
  contract coverage.

### Explicitly retire unless the destination says otherwise

- Hard-coded point versions as bootstrap logic; retain them only as updateable
  catalogue data.
- Copying long-form or specialised agent workflows into every repo.
- The implication that one application fully establishes testing, CI,
  deployment, security, and operations when it currently scaffolds only policy
  plus lint/format foundations.
- Silent Git-root redirection and silent successful partial application.

## Constraint for the next planning ticket

Before designing interfaces or implementation, decide whether the future
bootstrapper's destination is:

- a **safe scaffold** that produces a policy draft plus a precise remaining-work
  manifest; or
- a **verified baseline installer** that is responsible for dependencies,
  executable commands, CI, and post-application checks.

The current tool occupies the first category but its language often implies the
second. Resolving that ambiguity is the highest-leverage contract decision.
