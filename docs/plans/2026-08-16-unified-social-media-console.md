# Unified Social Media Console

**Goal:** Build a standalone Social Media OS controlled by `web`, separate from
Financial OS. Each agent keeps independent business data and an internal
read-only adapter, while the browser enters Social Media OS on port `4000`.

**Constraints:** Financial OS and Social Media OS remain separate applications;
`web` controls their independent start and stop targets.
Each platform maintains its own data and knowledge locally.
The browser may only use the Web application's `/api/media/*` routes; those
server routes may read loopback internal adapters. No real account action is in
scope. Do not modify unrelated in-progress Financial OS changes.

**Out of scope:** Shared media data, fake agent metrics, direct database access
from the browser, publication, login, commenting, messaging, commerce, ads,
and automation.

## Must-Haves

- MH1: Social Media OS has one public browser port: `4000`; `web` controls its
  runtime separately from Financial OS. A:I1
- MH2: Six platform agents have distinct UI entries and truthful connection
  states. A:I1
- MH3: All browser data access passes through a Web-owned server route; no
  standalone Douyin SPA remains. A:I1
- MH4: The implementation preserves independently owned platform data and does
  not fabricate unconnected agent snapshots. A:I1

### Task 1: Establish the dual-system Web control boundary A:I1

- [ ] Update `web` gateway documentation, start/stop scripts, and workspace
  metadata to control Financial OS on `3000` and Social Media OS on `4000`.
- [ ] Keep the two applications independent; do not embed Social Media OS in
  Financial OS.
- [ ] Verification: shell syntax checks pass and each target resolves to its
  documented port.

### Task 2: Define the six-agent media registry A:I1

- [ ] Add one Social Media OS configuration module for Douyin, Xiaohongshu,
  Kuaishou, X, WeChat Channels, and Xianyu.
- [ ] Define names, routes, independent data ownership, and optional internal
  snapshot environment variables in that one registry.
- [ ] Verification: a unit test asserts exactly six unique ids and routes.

### Task 3: Implement the server-side media snapshot adapter A:I1

- [ ] Add a typed `/api/agents/{agentId}` route that resolves agent
  configuration and fetches a configured loopback adapter server-side only.
- [ ] Return `not_configured`, `unavailable`, or `connected` instead of
  fabricated operational values.
- [ ] Normalize the existing Douyin `/api/dashboard` response when its internal
  adapter is configured.
- [ ] Verification: route tests cover unknown agents, no adapter, unavailable
  adapters, and a normalized Douyin snapshot.

### Task 4: Build the shared media overview and agent detail entries A:I1

- [ ] Add the Social Media OS overview with six operational cards and visible
  connection state.
- [ ] Add an agent detail view that loads the server-side snapshot route and
  exposes platform name, independent data ownership, observer state, and
  normalized records when connected.
- [ ] Include loading, empty, unavailable, and connected states without any
  publish or account-action controls.
- [ ] Verification: tests render all six entries and the service starts
  without Financial OS dependencies.

### Task 5: Remove the duplicate Douyin frontend A:I1

- [ ] Remove the standalone static SPA and its FastAPI frontend mount while
  keeping the local SQLite, knowledge base, and internal read-only API.
- [ ] Update Douyin documentation to name Social Media OS on the Web port as
  the browser entry and `8010` as its loopback-only adapter.
- [ ] Verification: Douyin API tests pass and its FastAPI route list contains
  no frontend route.

### Task 6: Validate the Social Media OS build A:I1

- [ ] Run Social Media OS tests and Python compilation.
- [ ] Verification: tests and compilation pass without Financial OS imports.

### Task 7: Validate the public Web runtime A:I1

- [ ] Start Social Media OS on port `4000` and the Douyin adapter on `8010`.
- [ ] Verify `/`, `/api/agents`, and `/api/agents/douyin` respond through the
  public Social Media OS process.
- [ ] Verification: browser smoke test captures the shared overview and a
  connected Douyin detail view.

### Task 8: Record the verified federated baseline A:I1

- [ ] Update local state and next-action files to distinguish the Web frontend
  owner from each platform's independent data owner.
- [ ] Re-index affected workspaces and inspect for an extra frontend or direct
  browser database path.
- [ ] Verification: architecture inspection shows one Web frontend and six
  media registry entries.
