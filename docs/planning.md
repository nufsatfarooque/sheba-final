## Pulse Hackathon Planning – Feature List & Scope

**Goal:** Ship a demo-ready, end-to-end Pulse platform in 6 days: Identity Intelligence Engine + Business Dashboard + (optional) Customer Widget, all running via Docker.

---

## 1. Must-Have Features (Hackathon Demo Core)

- **Identity Engine & Data**
  - Identity Strength Score (0–100) per customer using existing SHAP model + new identity framing.
  - Weighted scoring across: tenure, engagement, satisfaction, loyalty, value.
  - SHAP-based Cause Diagnostics (top 3 drivers) for each Identity Score.
  - Identity segments (Strong / Growing / At-Risk / Critical) with mapping based on score thresholds.
  - Historical identity snapshots table and API for “last vs current” comparison.
  - Seed/demo data for at least 50–200 synthetic customers across 1–2 demo businesses.

- **Backend API (FastAPI)**
  - `GET /api/customers/{customer_id}` – Customer details + latest identity_strength + segment.
  - `GET /api/customers/{customer_id}/identity` – Score, SHAP factors, last snapshot, simple trend.
  - `POST /api/customers/{customer_id}/identity/recalculate` – Recompute score on-demand.
  - `GET /api/customers?segment={segment}` – Paginated customer list by segment.
  - `POST /api/customers/upload` – CSV upload to load/update demo customers (happy path).
  - `GET /health` – Health check for Docker / judges.

- **Conversation Cards (AI-Prepared Human Touchpoints)**
  - Identity-drop detection (e.g., drop ≥ 10 points between snapshots).
  - GPT-4o-mini integration for AI-generated conversation opener (with rule-based fallback).
  - Card model fields: customer_id, business_id, opener, status (pending/actioned/completed), outcome.
  - API:
    - `GET /api/conversation-cards?status=pending` – Pending queue for dashboard.
    - `POST /api/conversation-cards/{card_id}/action` – Mark as actioned.
    - `PUT /api/conversation-cards/{card_id}/outcome` – Set outcome (responded/ignored/converted).

- **Authentication & Multi-Tenancy (Hackathon Level)**
  - JWT validation (HS256) with `customer_id`, `business_id`, `exp`.
  - Request/connection helpers that always filter by `business_id`.
  - Simple role separation: customer vs business user (via claim or token type).

- **Business Dashboard – Core UI (React)**
  - Landing Dashboard:
    - KPI cards: average identity_strength, customers per segment, simple trend indicator.
    - Segment chart (pie/bar) by Strong/Growing/At-Risk/Critical.
  - Customer Table:
    - Identity Strength and segment columns (color-coded threshold bands).
    - Sort/filter by score and segment.
    - Click row → open Customer Modal.
  - Customer Modal:
    - Prominent Identity Score visualization (circular meter or donut).
    - SHAP-based “Why” list (top 3 drivers, positive/negative).
    - Recent identity trend (basic sparkline or last few snapshots).
    - Conversation card history preview for that customer.
  - Conversation Queue Page:
    - List of pending conversation cards with customer, segment, reason summary, AI opener.
    - Actions: “Mark Actioned” + outcome selection.

- **Customer Widget – Minimal but Real**
  - UMD bundle via Vite, embeddable with `PulseWidget.init({ token, apiUrl, position })`.
  - Compact Identity view:
    - Current Identity Strength (number + small progress ring or bar).
    - “Strong because…” list (top 2–3 factors).
  - One-Tap Context Buttons:
    - Buttons: “I’m busy”, “I’m stuck”, “I’m exploring”, “I’m frustrated”.
    - Visual feedback on send, simple “Thanks, we’ll adjust” state.
  - Graceful error state if backend/websocket not available (widget never breaks host).

- **Real-Time Path (Minimum Viable)**
  - WebSocket endpoints:
    - `/ws` – Customer widget connects with JWT; supports context_share messages.
    - `/ws/dashboard` – Dashboard connects per business; receives notifications.
  - Message types:
    - Client → Server: `context_share` with `context_type`.
    - Server → Dashboard: `context_share` notifications and (optionally) `identity_update`.
  - Basic reconnection logic on frontend + widget (simple retry with backoff).

- **DevOps & Demo**
  - `docker-compose.yml` to run backend + PostgreSQL + frontend + widget.
  - `.env.example` populated for backend, frontend, widget (API URLs, WS URLs, JWT secret, OpenAI key).
  - One “golden path” demo script:
    - Business views dashboard → sees segments.
    - Judge plays customer in demo host → clicks context button.
    - Dashboard shows real-time context + new conversation card.
    - Human “sends” card and marks outcome.

---

## 2. Nice-to-Have Features (If Time Allows)

- **Identity Engine Enhancements**
  - Configurable feature weights via config file or DB table.
  - Simple UI toggle to switch between “legacy churn score” vs “identity strength” for comparison.
  - Per-segment recommended “next best action” (rule-based predictive enablement).

- **Dashboard UX Polish**
  - Identity-focused “Identity View” page with richer filters (score ranges, search).
  - Improved charts: trend over time for each segment, identity distribution over days.
  - “Demo compare” page showing old churn risk vs new identity framing for the same customer.

- **Widget Experience**
  - Progress milestones timeline with 3–4 hard-coded demo milestones.
  - Micro celebrations for hitting threshold (e.g., score crossing 70 or 80).
  - Very simple “Wrapped” card summarizing last 30 days for the demo user.

- **Real-Time Depth**
  - Identity updates pushed over WebSocket to both widget and dashboard when recalculated.
  - Per-business broadcast of “celebration” events (e.g., when a customer hits Strong).

- **Observability & Testing**
  - Structlog JSON logging with `business_id` and `customer_id` on identity calc + card generation.
  - A handful of backend tests:
    - Identity score within 0–100.
    - Conversation card generation when drop ≥ threshold.
    - JWT auth failure paths.
  - Smoke test for widget → backend WebSocket → dashboard round-trip.

---

## 3. Stretch / Storytelling Features (Demo Wow Factor)

- **Predictive Enablement v1**
  - For each At-Risk/Critical customer, show “This customer likely needs X next” (rule-based).
  - Surface these suggestions inside Conversation Cards and in Customer Modal.

- **A/B “Transparency” Story**
  - Simple toggle that hides the widget or hides identity score → used in narrative to say:
    - “This is how traditional tools work (hidden scores).”
    - “This is Pulse, where customers see their own progress.”

- **Judge-Facing Extras**
  - Architecture diagram in `architecture.md` rendered via mermaid for slide inclusion.
  - Short “Judge one-pager” PDF/markdown summarizing:
    - Problem, solution, why unique, how it works (1 diagram), and hackathon achievements.

---

## 4. Phase Breakdown (Aligned With Team Work Allocation)

- **Phase 1 – Foundations (Days 1–3)**
  - Backend: Identity engine, models, core APIs, demo seed data.
  - Backend: Auth, basic WebSocket manager, OpenAI integration (no heavy tuning).
  - Frontend: Dashboard scaffolds, Zustand store, REST + WebSocket client (mocked initially).
  - Widget: Vite setup, PulseWidget container, simple Identity view + static context buttons.

- **Phase 2 – Integration (Days 4–5)**
  - Wire frontend to real backend APIs and WebSockets.
  - Wire widget to real backend WebSocket + auth.
  - Ensure conversation card creation triggers from identity change or explicit API call.
  - Docker Compose end-to-end run; fix integration bugs.

- **Phase 3 – Polish & Demo (Day 6)**
  - UI polish on Identity visuals, colors, microcopy.
  - Stable demo script + demo host pages (JWT generator, embed example).
  - Add at least 2–3 pre-scripted “stories” (e.g., Strong/growing customer, At-Risk with context, recovery).

---

## 5. Hackathon Readiness Checklist

- **End-to-End Flow**
  - Identity scores load in dashboard for all demo customers.
  - Widget successfully loads, authenticates, shows identity for demo customer.
  - Context share travels: widget → backend → dashboard notification.
  - Identity change or manual trigger creates conversation card → shown in queue.

- **Demo Reliability**
  - All core paths work offline with seeded data (no external DB migration surprises).
  - OpenAI failures gracefully fall back to template text.
  - Docker `up --build` plus a short README “run demo in 5 minutes”.

If time runs tight, prioritize: **(1) Identity Engine + Dashboard**, **(2) Conversation Cards**, **(3) Minimal Widget + one-tap context**, then only add advanced real-time and celebrations if the core story is solid. 


