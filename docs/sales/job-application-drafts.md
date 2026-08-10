# Job Application Drafts — 2026-07-14

These drafts use only claims supported by the repository. Replace every
bracketed field before submitting.

## Portfolio résumé core

### Isaac Hernandez

[City, State] · [Phone] · [Application email]  
<https://github.com/isaacsight> · <https://kernel.chat>

### Profile

Founder and software engineer building open-source infrastructure for reliable,
auditable AI agents. Creator of Kernel, kbot-finance, and agent-os: a TypeScript
stack spanning multi-provider agent execution, MCP tools, deterministic engine
adapters, content-addressed provenance, hash-chained audit logs, regulatory
verification, scoped capability tokens, quotas, taint-aware execution, and
human approval gates. Combines production-oriented systems engineering with
clear technical writing and product design.

### Selected work

#### Kernel / kernel.chat — Founder and Sole Engineer

[Start date]–Present

- Built and published `@kernel.chat/kbot`, an MIT-licensed terminal AI agent
  supporting 20 model providers, local/offline execution, specialist routing,
  hundreds of tools, an SDK, and an MCP server.
- Designed the agent runtime across routing, task planning, persistent memory,
  knowledge retrieval, tool approval, offline caching, scheduling, security,
  evaluation, and multi-agent orchestration.
- Shipped a React 19 and TypeScript web application backed by Supabase edge
  functions, Postgres, authentication, rate limiting, Stripe billing
  infrastructure, service-worker caching, internationalization, and mobile
  packaging through Capacitor.
- Built the product's testing and delivery surface with Vitest, Playwright,
  GitHub Actions, TypeScript, ESLint, Docker, and automated npm publishing.
- Created and edited kernel.chat, a technical publication with more than 400
  numbered issues, turning systems work into clear public explanations and
  reusable implementation guidance.

#### kbot-finance — Creator and Maintainer

- Published an Apache-2.0 provenance substrate for AI workflows in regulated
  industries.
- Enforced the architectural separation between probabilistic AI reasoning and
  deterministic source-of-truth computation through typed engine adapters and
  content-addressed request/response envelopes.
- Implemented append-only hash-chained audit logs, integrity verification,
  replay, human approval gates, jurisdiction-aware verifier rules, adverse
  action reason codes, and an MCP server.
- Authored the package documentation, threat model, federal alignment analysis,
  RFC material, test suite, design-partner SOW, and audit-readiness guidance.

#### agent-os — Creator and Maintainer

- Built OS-level primitives for multi-agent systems above sandbox providers and
  below MCP/A2A: signed capabilities, namespaces, token/cost/time quotas,
  taint-aware tool execution, content-addressed auditing, downscoped handoff,
  credential isolation, snapshots, and rubric-graded outcomes.
- Designed fail-closed controls so untrusted tool output cannot silently reach
  privileged tools and delegated agents cannot escalate authority.
- Published the package under Apache 2.0 with typed APIs, runnable examples,
  tests, architecture comparisons, and a public roadmap.

#### kbot-orchestrator — Creator and Maintainer

- Built auditable pipelines that route work across agents and humans, preserve
  approval gates, and support outreach, content, and maintenance workflows.
- Implemented resumable task execution, typed state transitions, CLI workflows,
  and reusable delivery artifacts.

### Technical skills

- **Languages:** TypeScript, JavaScript, SQL, HTML/CSS, [add truthful Python
  level], [others]
- **AI systems:** agent orchestration, MCP, tool use, RAG, evaluation, memory,
  prompt/version provenance, model routing, local inference
- **Backend/data:** Node.js, Supabase, PostgreSQL, edge functions, REST APIs,
  authentication, rate limiting, Stripe
- **Reliability/security:** capability security, taint tracking, audit logs,
  deterministic replay, human approval, secret handling, threat modeling
- **Frontend/product:** React, Vite, Zustand, PWA, responsive UI, Capacitor
- **Delivery:** GitHub Actions, Docker, npm package publishing, Vitest,
  Playwright, ESLint, TypeScript

### Prior employment

[Employer · title · dates · 3–5 impact bullets]

### Education

[School · degree or program · dates]

## Kepler — direct founder email

**To:** `hi@kepler.ai`  
**Subject:** I independently built your core architectural rule

Vinoo and John,

Kepler is the closest job match I have encountered because I independently
built and published the same structural separation your product is founded on:
AI interprets and orchestrates; deterministic engines produce source-of-truth
numbers; every request, response, decision, and approval remains traceable and
replayable.

My implementation is `@kernel.chat/kbot-finance`, an Apache-2.0 TypeScript
package with content-addressed engine envelopes, a hash-chained audit log,
jurisdiction-aware verifier rules, human material gates, integrity checking,
replay, and an MCP server. I also built `@kernel.chat/agent-os`, which adds
signed capabilities, per-agent quotas, taint-aware execution, downscoped
handoff, credential isolation, and outcome evaluation.

Repository: https://github.com/isaacsight/kernel  
kbot-finance: https://www.npmjs.com/package/@kernel.chat/kbot-finance  
agent-os: https://www.npmjs.com/package/@kernel.chat/agent-os

I would like to be considered for the Forward Deployed Engineer role. The
public packages show how I think about the exact problem; the broader Kernel
repository shows that I can carry a product from architecture through UI,
testing, documentation, packaging, and customer-facing explanation.

[One truthful sentence about customer-facing or prior professional experience.]

Would you be open to a 25-minute technical conversation?

Isaac Hernandez  
[Phone] · [City] · [Application email]

## Origin — cover letter

Origin's premise—that organizations need to see and verify what agents actually
do at the endpoint—matches the control-plane work I have been building in open
source. I created agent-os to constrain and prove agent authority before and
through execution: signed capability tokens, bounded invocation and cost
budgets, taint propagation, downscoped handoffs, credential isolation, and
content-addressed audit records. I created kbot-finance to preserve what an
agent saw, requested, received from deterministic systems, decided, and routed
for human approval.

That makes Origin especially interesting to me because the layers are
complementary. Origin observes real endpoint behavior; my recent work has
focused on the primitives that authorize behavior and make its chain of
authority independently verifiable. I would bring that systems perspective to
customer deployments while remaining comfortable moving through TypeScript,
React, APIs, Postgres, Supabase, Docker, tests, documentation, and the messy
integration work between them.

I am also the creator and sole engineer behind Kernel, an open-source terminal
agent and web platform spanning model routing, local inference, hundreds of
tools, MCP client/server support, memory, orchestration, approvals, and
evaluation. The repository is a working sample of both my engineering and my
ability to explain complex infrastructure clearly to users.

[Add one truthful paragraph on prior employment and customer-facing work.]

I would welcome the opportunity to discuss the Forward Deployed Engineer role
and demonstrate the capability, taint, and audit flows directly from the public
packages.

## Sobek AI — cover letter

I am applying to Sobek AI because the failure boundary described in the role—
where agent workflows meet enterprise data, sensitive environments, tool use,
grounding, and runtime trust—is the boundary my open-source work is designed to
make explicit and enforceable.

I built Kernel, a multi-provider terminal and web agent platform, and then
separated its trust primitives into two public packages. kbot-finance wraps
deterministic systems in content-addressed envelopes, records requests,
responses, approvals, verifier decisions, and incidents in a hash-chained audit
log, and exposes the system through MCP. agent-os adds signed capabilities,
resource quotas, taint-aware execution, downscoped delegation, credential
isolation, and rubric-graded outcomes. The goal is not to assume the model will
always behave correctly, but to make important boundaries structural and
reviewable.

Across the wider repository I have shipped routing, task planning, memory,
knowledge retrieval, offline caching, approvals, security controls, Supabase
edge functions, React interfaces, npm packages, CI, unit tests, end-to-end
tests, Docker support, and extensive technical documentation. I am comfortable
debugging across model behavior, application code, data, tools, and the runtime
around them.

[Add truthful Python experience.]  
[Add prior professional/customer deployment experience.]  
[Confirm Seattle hybrid availability.]

I would be excited to bring this production-first trust and systems work to
Sobek's life-science and emergency-response deployments.

## Submission checklist

- [ ] Replace every bracketed field.
- [ ] Reduce the résumé to two pages after prior employment is added.
- [ ] Confirm every numeric claim against the current README/package metadata.
- [ ] Tailor the first two bullets to each job description.
- [ ] Export résumé to PDF.
- [ ] Submit Sobek before July 22, 2026 if Seattle is viable.
- [ ] For Kepler, send the founder email and submit the formal application on
      the same day.
- [ ] Track application date, status, follow-up date, and contact in the leads
      file or a separate tracker.
