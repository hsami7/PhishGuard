# PhishGuard

## What This Is

A lightweight, distributed phishing email detection system. It allows users to submit suspected emails via text or simplified metadata and view the history of reports through a secure, professional web interface.

## Core Value

Accurate, explainable phishing detection achieved through a robust distributed architecture and strict cybersecurity practices without the overhead of heavy SPA frameworks or paid APIs.

## Current Milestone: v2.0 Intelligent Automation & UI-UX Pro-Max

**Goal:** Integration of automated raw email parsing, regex link harvesting, and a single-field glassmorphism dashboard layout.

**Target features:**
- Automated raw email parsing
- Regex link harvesting
- Single-field glassmorphism dashboard layout

## Requirements

### Validated

- ✓ **CORE-01**: Heuristic scoring engine (Regex, keywords) yielding a Low/Medium/High score and textual justification. — Phase 08

### Active

- [ ] **SEC-01**: Secure user authentication (JWT) with bcrypt-hashed passwords.
- [ ] **SEC-02**: Role-based access control (Admin vs Analyst).
- [ ] **SEC-03**: Structured JSON audit logging for security and traceability.
- [ ] **DIST-01**: AnalysisService operates as an independent gRPC microservice.
- [ ] **DIST-02**: API Gateway handles routing, input validation (Pydantic), and auth.
- [ ] **UI-01**: Lightweight frontend using FastAPI Jinja2Templates and Tailwind CSS via CDN.
- [ ] **UI-02**: Dashboard for email submission and viewing report history.

### Out of Scope

- Direct connection to Gmail/Outlook — Excluded to fit the 15-day timeframe.
- Complex `.eml` file parsing — Users will submit text/metadata directly.
- Full AI/ML model for analysis — Explicitly excluded; rules/heuristics are sufficient and meet the constraints.
- Separate frontend SPA (React/Vue) — Too much build overhead and CORS complexity; Jinja templates are sufficient and faster to implement.

## Context

This project is being developed within a strict 15-day timeframe with specific academic grading criteria:
- 30% for distributed communication (met via gRPC).
- 25% for cybersecurity (met via JWT, bcrypt, and audit logging).
The design will leverage `ui-ux-pro-max` guidelines (HTML/Tailwind) for a professional, dark-mode aesthetic (e.g., Tokyo Night or Catppuccin) to ensure a premium UI/UX without SPA complexity.

## Constraints

- **Architecture**: Must include distributed components (gRPC) to meet grading requirements.
- **Security**: Passwords must never be stored in plain text. JWT authentication is mandatory.
- **Timeline**: 15 days maximum implementation time.
- **Dependencies**: No paid APIs or mandatory cloud services. Analysis must run locally.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| FastAPI Jinja2Templates | Eliminates CORS and build overhead of SPAs while still allowing professional Tailwind styling. | — Pending |
| gRPC AnalysisService | Fulfills the 30% distributed communication requirement. | — Pending |
| SQLite + bcrypt + JWT | Fulfills the 25% cybersecurity requirement without overly complex infrastructure. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state
---
*Last updated: 2026-06-09 at the start of Milestone v2.0*
