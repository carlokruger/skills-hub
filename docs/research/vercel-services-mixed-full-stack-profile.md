# Vercel Services for the mixed full-stack profile

Research note for the Wayfinder investigation **Evaluate Vercel Services for
the mixed full-stack profile**. This note uses only first-party Vercel
documentation, checked on 2026-08-07. It evaluates whether the project
bootstrapper should support deploying a Next.js frontend and Python backend as
one Vercel project; it does not implement that support.

## Executive conclusion

Vercel Services is a technically strong match for a mixed Next.js/FastAPI
repository: Vercel explicitly documents that pairing, builds the applications
independently, deploys them together, and presents one public routing surface.
The current model uses one root `vercel.json`, a `services` object, ordered
top-level rewrites for public ingress, and optional bindings for private
service-to-service calls ([Services](https://vercel.com/docs/services),
[configuration reference](https://vercel.com/docs/services/config-reference),
[routing](https://vercel.com/docs/services/routing)).

It should be offered as an **opt-in, experimental deployment capability**, not
the mixed profile's default. Vercel's current first-party guide describes
Services as Beta on all plans, while the core documentation carries a
permissions-required marker. The canonical `services` model also only replaced
the earlier `experimentalServices` model in June 2026. That combination is too
young and entitlement-dependent for a bootstrapper to promise as universally
available ([complete guide](https://vercel.com/kb/guide/vercel-services),
[Services](https://vercel.com/docs/services),
[experimental model](https://vercel.com/docs/services/experimental)).

The bootstrapper may generate this target when the user deliberately selects
it, but should preflight actual team access and the installed CLI, surface the
Beta status, pin the generated configuration to the current `services` schema,
and retain a supported fallback: separate Vercel projects, or Vercel for Next.js
with the Python backend deployed elsewhere.

## Capability and repository contract

### Supported shape

Vercel's own example is the required shape: a Next.js frontend and FastAPI
backend in one repository and one Vercel project. Each service has its own root,
dependencies, build, and runtime configuration, but all services share one
deployment. A bootstrapper-friendly layout is therefore:

```text
/
├── frontend/          # Next.js application
├── backend/           # Python application and pyproject.toml/uv.lock
└── vercel.json        # service ownership and public routing
```

The service `root` is required and is relative to `vercel.json`. The optional
`framework` can pin `nextjs` or `fastapi`; otherwise Vercel detects it. Python
ASGI entrypoints can use `module:variable`, such as `main:app`
([configuration reference](https://vercel.com/docs/services/config-reference),
[Python runtime](https://vercel.com/docs/functions/runtimes/python)).

A minimal generated configuration would follow this current model:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "services": {
    "web": { "root": "frontend", "framework": "nextjs" },
    "api": {
      "root": "backend",
      "framework": "fastapi",
      "entrypoint": "main:app"
    }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": { "service": "api" } },
    { "source": "/(.*)", "destination": { "service": "web" } }
  ]
}
```

This is intentionally not the older `experimentalServices`/`routePrefix`
shape. Vercel says the current `services` model replaces it for new projects
([Services](https://vercel.com/docs/services),
[experimental model](https://vercel.com/docs/services/experimental)).

### Configuration ownership and routing

With `services` present, project-wide public URL behavior stays at the top
level. Build/runtime fields such as `functions`, `installCommand`,
`buildCommand`, `devCommand`, `ignoreCommand`, `outputDirectory`, and
`framework` belong inside the relevant service; keeping them at the top level
is invalid because ownership would be ambiguous
([Services](https://vercel.com/docs/services),
[configuration reference](https://vercel.com/docs/services/config-reference)).

Services are private by default. A service receives public traffic only through
an ordered top-level rewrite targeting `{ "service": "name" }`; Vercel uses the
first match, so `/api/(.*)` must precede the frontend catch-all. The backend sees
the original path (`/api/users`, not `/users`), and routing is final: a backend
404/405 does not fall through to the frontend. Generated FastAPI routes must
therefore include the public prefix, or the configuration must deliberately
transform the request path ([routing](https://vercel.com/docs/services/routing)).

Bindings provide private runtime calls between services and inject a
deployment-aware URL into a caller-selected environment variable. They do not
make the target public, do not provide application-level authorization, are
unavailable during builds and middleware, and bypass the public firewall,
deployment protection, middleware, and CDN pipeline. The bootstrapper should
generate a binding only for a real server-side call and must not describe it as
an authentication boundary ([service bindings](https://vercel.com/docs/services/bindings)).

### Local development

`vercel dev` runs all services together and injects binding variables; `vercel
dev -L` does so without authenticating to Vercel Cloud. A generated mixed
profile should expose this as the integration-development command while keeping
framework-native commands for isolated frontend and backend work
([Services](https://vercel.com/docs/services)). Container-backed services also
require a local Docker CLI and daemon
([container images](https://vercel.com/docs/functions/container-images)).

## Python support and constraints

The Python runtime supports ASGI and WSGI applications. Vercel supplies
framework presets for FastAPI, Flask, Django, and other compatible frameworks;
it detects dependencies from `pyproject.toml`, `requirements.txt`, or
`Pipfile`. New applications should expose `app` (typical ASGI/WSGI),
`application` (Django/WSGI), or `handler` (`BaseHTTPRequestHandler`), and may
declare a custom `module:variable` in `[tool.vercel].entrypoint`
([Python runtime](https://vercel.com/docs/functions/runtimes/python)).

Python 3.12 is the default; 3.13 and 3.14 are also available. The version can be
set in `pyproject.toml`, `.python-version`, or `Pipfile.lock`. Dependencies may
use `pyproject.toml` with an optional `uv.lock`, which fits the mixed profile's
existing `uv` preference. Streaming responses are supported
([Python runtime](https://vercel.com/docs/functions/runtimes/python)).

Material runtime constraints are:

- Python has no automatic tree-shaking. Runtime dependencies and included files
  must be kept narrow, with `excludeFiles` used for tests, fixtures, and other
  non-runtime assets. The standard uncompressed Python bundle limit is 500 MB;
  Large Functions can reach 5 GB for eligible Node.js and Python projects, but
  that path remains Beta and requires Fluid compute
  ([Python runtime](https://vercel.com/docs/functions/runtimes/python),
  [function limits](https://vercel.com/docs/functions/limitations)).
- Services inherit Function limits. With Fluid compute, memory is 2 GB/1 vCPU
  on Hobby and up to 4 GB/2 vCPU on Pro/Enterprise. Node.js and Python requests
  default to 300 seconds; Hobby cannot exceed that, Pro/Enterprise generally
  support 800 seconds, and an eligible 1,800-second extension remains Beta.
  Request and response bodies are limited to 4.5 MB
  ([function limits](https://vercel.com/docs/functions/limitations)).
- These are request-driven Functions, not unconstrained persistent servers.
  Work exceeding the duration ceiling needs a different execution model; Vercel
  itself points unlimited-duration work to Workflows. The bootstrapper should
  not select Services for workloads requiring local durable state, an
  indefinitely running process, or payloads above the Function limit
  ([function limits](https://vercel.com/docs/functions/limitations)).
- A custom container is available where framework/runtime detection is
  insufficient, but it still inherits Function limits and pricing. Secure
  Compute and Static IPs are not yet supported for container images
  ([container images](https://vercel.com/docs/functions/container-images)).

The initial bootstrap capability should therefore support the documented
FastAPI preset only. Flask and Django are valid future variants, but generating
one opinionated framework keeps entrypoint, routing, dependency, health-check,
and test conventions verifiable. A custom-container escape hatch should be a
separate explicit choice, not an automatic fallback.

## Pricing and build limits

Services have no separate flat deployment price documented. Each service is
billed like a Vercel Function for Active CPU, provisioned memory, and
invocations under Fluid compute. Calls over a binding add a regionally priced
service request; public requests do not. Returned bytes are billed as Fast
Origin Transfer. Hobby includes 4 Active CPU hours, 360 GB-hours of provisioned
memory, and one million invocations; Pro is usage-priced by region and can use
its plan credit ([Services pricing](https://vercel.com/docs/services/pricing),
[Fluid compute pricing](https://vercel.com/docs/functions/usage-and-pricing),
[general pricing](https://vercel.com/docs/pricing)).

A deployment build may run for at most 45 minutes. Current build resources are
8 GB memory and 32 GB disk for Hobby and Pro, with 2 CPUs on Hobby and 4 on Pro;
Vercel bills build use according to the selected build-machine model. Since
Services builds each service separately inside one deployment, the bootstrapper
should validate both application builds and call out that adding a backend can
increase build and runtime consumption
([builds](https://vercel.com/docs/builds),
[Services](https://vercel.com/docs/services)).

## Bootstrapper decision and guardrails

Offer `Vercel Services` only when all of these conditions hold:

1. The user explicitly opts into a Beta deployment target after seeing the
   availability and usage-billing warning.
2. A read-only preflight confirms the target Vercel team/project exposes
   Services and the installed/current Vercel CLI accepts the canonical
   `services` schema. Failure produces a clear incomplete result and recommends
   the separate-project or split-platform fallback; it must not silently emit
   `experimentalServices`.
3. The generated repository has one root `vercel.json`, isolated `frontend/`
   and `backend/` dependency boundaries, pinned `nextjs` and `fastapi`
   frameworks, a declared Python version, and a locked `uv` environment.
4. Public routing reserves `/api/**` for FastAPI before the frontend catch-all,
   and generated application routes are tested against the preserved `/api`
   prefix. Backend access is private unless a rewrite explicitly exposes it.
5. `vercel dev` is an integration command, while isolated native dev commands
   remain available. CI builds and tests both services before deployment.
6. The workload passes an explicit suitability check: external durable storage,
   no indefinitely resident process, body sizes below 4.5 MB, expected request
   time within the selected plan's duration, and Python bundle size below the
   standard 500 MB unless the user separately opts into and verifies Large
   Functions.
7. Generated documentation names the compute, binding-call, transfer, and build
   cost dimensions and recommends spend controls for non-Hobby deployments.
8. Container runtime, Large Functions, and durations above 800 seconds are
   separately labelled experimental capabilities and are never inferred from a
   dependency or build failure.

Under these guardrails, Services is a valuable convenience capability for the
mixed profile: it removes cross-project preview URL coordination and gives the
repository one deployment and routing surface. Until it is generally available
without an entitlement caveat and its current schema has had more time to
stabilize, it should remain an explicit exception to the safer default rather
than redefine that default.
