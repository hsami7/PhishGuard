# Project Retrospective: PhishGuard

## Milestone: v1.0 — MVP

**Shipped:** 2026-06-09
**Phases:** 8 | **Plans:** 8

### What Was Built
- Initialized FastAPI and gRPC boilerplate structure.
- Implemented SQLite user table, bcrypt hashing, and JWT token generation/validation.
- Built independent gRPC microservice and heuristic scoring engine.
- Connected FastAPI Gateway to Analysis Service.
- Developed FastAPI Jinja2 templates styled with Tailwind CSS for submission and history.
- Implemented structured JSON audit logging.
- Closed gaps by adding Admin/Analyst RBAC roles and an Analysis History table.
- Enhanced heuristics with URL unshortening, local PhishTank DB lookups, and advanced spoofing detection.

### What Worked
- **Hybrid Architecture:** The split between the public-facing FastAPI gateway and the private gRPC analysis service created a strong boundary for security and performance.
- **Tailwind via CDN:** Avoided the immense overhead of a heavy Node.js build process while still achieving a highly polished, modern "Dark Cyber" aesthetic.
- **Rule-Based Heuristics:** By using regex and keyword matching instead of a heavyweight AI model, the analysis service remains lightning fast and completely private (no third-party API calls).

### What Was Inefficient
- **Missed Requirements:** During the initial phase execution, two requirements (SEC-04 and UI-03) were overlooked because they were not explicitly mapped into the phase breakdown early on. This required a retroactive Phase 7 to close the gaps.
- **Database Migrations:** Because Alembic was omitted to save time on the MVP, schema changes required dropping and recreating the SQLite database, erasing test data.

### Patterns Established
- **Direct Database Access in Gateway:** The FastAPI gateway handles all user and history data persistence, while the gRPC service remains completely stateless.
- **Glassmorphism UI:** Established a consistent design language using translucent panels (`bg-slate-800/50`) and glowing SVG animations for data visualization.

### Key Lessons
- Always cross-reference the `REQUIREMENTS.md` traceability table *before* finalizing the execution of a phase to prevent feature drops.
- Even for prototypes, introducing a lightweight migration tool (or at least seed scripts) prevents friction when schema changes inevitably occur.
