# Graph Report - PhishGuard  (2026-06-10)

## Corpus Check
- 85 files · ~19,947 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 515 nodes · 531 edges · 73 communities (64 shown, 9 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `64e68a7d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 68|Community 68]]

## God Nodes (most connected - your core abstractions)
1. `User` - 15 edges
2. `parse_email()` - 10 edges
3. `EmailAnalyzer` - 9 edges
4. `PhishGuard` - 9 edges
5. `UserCreate` - 7 edges
6. `UserResponse` - 7 edges
7. `Token` - 7 edges
8. `EmailAnalysisResponse` - 7 edges
9. `Phase 08: enhance-phishtank-intel-url-unshortener-advanced-spoofing-de - Context` - 7 edges
10. `Phase 08 — Validation Strategy` - 7 edges

## Surprising Connections (you probably didn't know these)
- `analyze_email()` --calls--> `parse_email()`  [EXTRACTED]
  app/routers/analysis.py → analysis/parser.py
- `test_parse_malformed_email()` --calls--> `parse_email()`  [EXTRACTED]
  tests/test_parser.py → analysis/parser.py
- `test_parse_multipart_email()` --calls--> `parse_email()`  [EXTRACTED]
  tests/test_parser.py → analysis/parser.py
- `test_parse_simple_text_email()` --calls--> `parse_email()`  [EXTRACTED]
  tests/test_parser.py → analysis/parser.py
- `test_regex_strictness()` --calls--> `parse_email()`  [EXTRACTED]
  tests/test_parser.py → analysis/parser.py

## Import Cycles
- None detected.

## Communities (73 total, 9 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.13
Nodes (33): get_db(), AnalysisHistory, User, Session, User, Session, User, AnalysisHistoryResponse (+25 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (17): Analysis Service (gRPC), API Gateway & Web App, Automated Tests, Database Skeleton, Dependencies & Setup, Goal, Manual Verification, [NEW] analysis/server.py (+9 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (15): API Routing, Database & Models, Dependencies, Goal, Manual Verification, [MODIFY] app/main.py, [MODIFY] requirements.txt, [NEW] app/models.py (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (15): Advanced Spoofing Logic, Canonical References, Deferred Ideas, Established Patterns, Existing Code Insights, General, Implementation Decisions, Integration Points (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (7): admin_stats(), index(), login_page(), User, read_dashboard(), register_page(), Request

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (12): Backend Models & Schemas, Backend Routing & Security, Frontend, [MODIFY] app/main.py, [MODIFY] app/models.py, [MODIFY] app/routers/analysis.py, [MODIFY] app/routers/auth.py, [MODIFY] app/schemas.py (+4 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (12): Active, Constraints, Context, Core Value, Current Milestone: v2.0 Intelligent Automation & UI-UX Pro-Max, Evolution, Key Decisions, Out of Scope (+4 more)

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (8): AnalysisService, AnalysisServiceServicer, AnalysisServiceStub, Missing associated documentation comment in .proto file., Constructor.          Args:             channel: A grpc.Channel., Missing associated documentation comment in .proto file., Missing associated documentation comment in .proto file., Missing associated documentation comment in .proto file.

### Community 8 - "Community 8"
Cohesion: 0.17
Nodes (11): Backend Routing, Goal, HTML Templates, [MODIFY] app/main.py, [MODIFY] templates/base.html, [NEW] templates/dashboard.html, [NEW] templates/index.html, [NEW] templates/login.html & templates/register.html (+3 more)

### Community 9 - "Community 9"
Cohesion: 0.27
Nodes (3): EmailAnalyzer, AnalysisService, serve()

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (10): Core Logic, Goal, gRPC Server Update, [MODIFY] analysis/server.py, [NEW] analysis/heuristics.py, [NEW] scripts/test_grpc.py, Phase 3: Analysis Service Logic - Plan, Proposed Changes (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.18
Nodes (10): Analysis Router, Gateway Registration, Goal, [MODIFY] app/main.py, [MODIFY] app/schemas.py, [NEW] app/routers/analysis.py, Phase 4: API Gateway Integration - Plan, Proposed Changes (+2 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (10): Audit Logging, Documentation, Goal, [MODIFY] analysis/server.py, [MODIFY] app/routers/analysis.py, [MODIFY] app/routers/auth.py, [MODIFY] README.md, Phase 6: Audit Logging & Final Polish - Plan (+2 more)

### Community 13 - "Community 13"
Cohesion: 0.18
Nodes (10): Analysis Service, API Gateway, Authentication & Security, Interface (UI), Out of Scope, Requirements Archive: v1.0 v1.0 MVP, Requirements: PhishGuard, Traceability (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.20
Nodes (9): 1. Cold Start Smoke Test, 2. Protobuf Compilation, 3. gRPC Service Initialization, 4. FastAPI Gateway Initialization & Template Rendering, 5. Database File Creation, Current Test, Gaps, Summary (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.20
Nodes (9): 1. Cold Start Smoke Test, 2. User Registration, 3. Password Hashing Verification, 4. JWT Token Generation, 5. Protected Endpoint Access, Current Test, Gaps, Summary (+1 more)

### Community 16 - "Community 16"
Cohesion: 0.20
Nodes (9): 1. Parsing Raw `.eml`, 2. Header Extraction, 3. Body Extraction (Multipart & Decoding), 4. Link Harvesting (Regex), Conclusion, Findings, Objective, Research: Phase 09 - Automated Email Parsing Engine (+1 more)

### Community 17 - "Community 17"
Cohesion: 0.20
Nodes (9): 1. Installation, 2. Generate Protobuf Files, 3. Start the Services, 4. Access the Platform, Architecture, PhishGuard, Prerequisites, Quickstart (+1 more)

### Community 18 - "Community 18"
Cohesion: 0.22
Nodes (8): 1. Cold Start Smoke Test, 2. Unauthenticated Access Rejection, 3. Authenticated Analysis Success, 4. Graceful Error Handling (gRPC down), Current Test, Gaps, Summary, Tests

### Community 19 - "Community 19"
Cohesion: 0.22
Nodes (8): 1. Landing Page Aesthetics, 2. User Registration Flow, 3. Login & Session Storage, 4. End-to-End Analysis Dashboard, Current Test, Gaps, Summary, Tests

### Community 20 - "Community 20"
Cohesion: 0.22
Nodes (8): 1. Cold Start Smoke Test, 2. URL Unshortening, 3. PhishTank DB Lookup, 4. Display Name Spoofing Detection, Current Test, Gaps, Summary, Tests

### Community 21 - "Community 21"
Cohesion: 0.36
Nodes (7): parse_email(), Parses a raw .eml string and extracts headers, body text, and links.     Uses be, Any, test_parse_malformed_email(), test_parse_multipart_email(), test_parse_simple_text_email(), test_regex_strictness()

### Community 22 - "Community 22"
Cohesion: 0.25
Nodes (7): 1. Cold Start Smoke Test, 2. Heuristic Engine - Benign Email Validation, 3. Heuristic Engine - Phishing Email Validation, Current Test, Gaps, Summary, Tests

### Community 23 - "Community 23"
Cohesion: 0.25
Nodes (7): 1. Final Documentation Check, 2. FastAPI Gateway Audit Logs, 3. gRPC Microservice Audit Logs, Current Test, Gaps, Summary, Tests

### Community 24 - "Community 24"
Cohesion: 0.25
Nodes (7): Manual-Only Verifications, Per-Task Verification Map, Phase 08 — Validation Strategy, Sampling Rate, Test Infrastructure, Validation Sign-Off, Wave 0 Requirements

### Community 25 - "Community 25"
Cohesion: 0.25
Nodes (7): Active Requirements, Email Parsing & Extraction, Future Requirements (Deferred), Out of Scope, Requirements: Milestone v2.0, Traceability, UI & Dashboard

### Community 26 - "Community 26"
Cohesion: 0.25
Nodes (7): Key Lessons, Milestone: v1.0 — MVP, Patterns Established, Project Retrospective: PhishGuard, What Was Built, What Was Inefficient, What Worked

### Community 27 - "Community 27"
Cohesion: 0.29
Nodes (6): 1. Database Reset & RBAC Analyst Check, 2. Analysis History Persistence, Current Test, Gaps, Summary, Tests

### Community 28 - "Community 28"
Cohesion: 0.29
Nodes (6): Deviations from Plan, Execution Metrics, Next Steps, Phase 08 Plan 01: Enhance Heuristics & Analysis Summary, Self-Check: PASSED, What Was Done

### Community 29 - "Community 29"
Cohesion: 0.29
Nodes (6): Advanced Spoofing Logic, Deferred Ideas, Phase 08: enhance-phishtank-intel-url-unshortener-advanced-spoofing-de - Discussion Log, PhishTank Integration, the agent's Discretion, URL Unshortening

### Community 30 - "Community 30"
Cohesion: 0.29
Nodes (6): 1. URL Unshortening (Custom Redirect Follower), 2. PhishTank Integration (Local DB), 3. Advanced Spoofing Logic (Display Name Heuristic), Objective, Phase 08: enhance-phishtank-intel-url-unshortener-advanced-spoofing-de - Research, Validation Architecture

### Community 31 - "Community 31"
Cohesion: 0.33
Nodes (5): 1. SEC-04: Role-Based Access Control (Admin vs Analyst), 2. UI-03: Email Analysis History, Phase 7: Close Gaps (SEC-04 & UI-03) - Research, Schema Migration Note, Technical Approach

### Community 32 - "Community 32"
Cohesion: 0.33
Nodes (5): Plan: Phase 09 - Automated Email Parsing Engine, Requirements, Strategy, Tasks, Verification

### Community 33 - "Community 33"
Cohesion: 0.33
Nodes (5): Milestones, Phase 8: Enhance: PhishTank Intel, URL Unshortener, Advanced Spoofing Detection, and Bilingual UI (FR/EN), Phases, Progress, Roadmap: PhishGuard

### Community 34 - "Community 34"
Cohesion: 0.33
Nodes (5): Milestones, Phases, Progress, Roadmap: PhishGuard, 🚧 v2.0 Intelligent Automation & UI-UX Pro-Max (In Progress)

### Community 35 - "Community 35"
Cohesion: 0.40
Nodes (4): Architecture Integration, Phase 1: Infrastructure & Boilerplate - Research, Risks, Technical Approach

### Community 36 - "Community 36"
Cohesion: 0.40
Nodes (4): Canonical refs, Context: Phase 09, Decisions, Domain

### Community 37 - "Community 37"
Cohesion: 0.40
Nodes (4): 1. Unit Tests, 2. Integration Tests, 3. Manual UAT, Validation Strategy: Phase 09

### Community 38 - "Community 38"
Cohesion: 0.40
Nodes (4): Canonical refs, Context: Phase 10, Decisions, Domain

### Community 39 - "Community 39"
Cohesion: 0.40
Nodes (4): Feature Table Stakes, Research Summary: Intelligent Automation & UI-UX Pro-Max, Stack Additions, Watch Out For

### Community 40 - "Community 40"
Cohesion: 0.50
Nodes (3): Open Items, Phase 1 Plan 01 Summary, Work Completed

### Community 41 - "Community 41"
Cohesion: 0.50
Nodes (3): Dimensions, Phase 1: Infrastructure & Boilerplate - Validation Strategy, Release Criteria

### Community 42 - "Community 42"
Cohesion: 0.50
Nodes (3): Open Items, Phase 2 Plan 01 Summary, Work Completed

### Community 43 - "Community 43"
Cohesion: 0.50
Nodes (3): Phase 2: Authentication & Security Core - Research, Risks, Technical Approach

### Community 44 - "Community 44"
Cohesion: 0.50
Nodes (3): Dimensions, Phase 2: Authentication & Security Core - Validation Strategy, Release Criteria

### Community 45 - "Community 45"
Cohesion: 0.50
Nodes (3): Open Items, Phase 3 Plan 01 Summary, Work Completed

### Community 46 - "Community 46"
Cohesion: 0.50
Nodes (3): Dimensions, Phase 3: Analysis Service Logic - Validation Strategy, Release Criteria

### Community 47 - "Community 47"
Cohesion: 0.50
Nodes (3): Open Items, Phase 4 Plan 01 Summary, Work Completed

### Community 48 - "Community 48"
Cohesion: 0.50
Nodes (3): Dimensions, Phase 4: API Gateway Integration - Validation Strategy, Release Criteria

### Community 49 - "Community 49"
Cohesion: 0.50
Nodes (3): Open Items, Phase 5 Plan 01 Summary, Work Completed

### Community 50 - "Community 50"
Cohesion: 0.50
Nodes (3): Dimensions, Phase 5: Frontend UI & Templates - Validation Strategy, Release Criteria

### Community 51 - "Community 51"
Cohesion: 0.50
Nodes (3): Open Items, Phase 6 Plan 01 Summary, Work Completed

### Community 52 - "Community 52"
Cohesion: 0.50
Nodes (3): Dimensions, Phase 6: Audit Logging & Final Polish - Validation Strategy, Release Criteria

### Community 53 - "Community 53"
Cohesion: 0.50
Nodes (3): Accomplishments, Phase 7: Close Gaps (SEC-04 & UI-03), Verification

### Community 54 - "Community 54"
Cohesion: 0.50
Nodes (3): Dimensions, Phase 7: Close Gaps (SEC-04 & UI-03) - Validation Strategy, Release Criteria

### Community 55 - "Community 55"
Cohesion: 0.50
Nodes (3): Implementation Guidelines, Selected Pattern & Style, UI-SPEC: Phase 10

### Community 56 - "Community 56"
Cohesion: 0.50
Nodes (3): Integration Status, Milestone v1.0 Audit Report, Requirements Assessment

### Community 57 - "Community 57"
Cohesion: 0.50
Nodes (3): Milestones, v1.0 MVP (Shipped: 2026-06-09), v1.0 v1.0 MVP (Shipped: 2026-06-09)

### Community 58 - "Community 58"
Cohesion: 0.50
Nodes (3): Current Position, Operator Next Steps, Performance Metrics

## Knowledge Gaps
- **255 isolated node(s):** `Any`, `User`, `Config`, `generate_proto.sh script`, `v1.0 MVP (Shipped: 2026-06-09)` (+250 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `parse_email()` connect `Community 21` to `Community 0`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `User` (e.g. with `Session` and `User`) actually correct?**
  _`User` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `UserCreate` (e.g. with `Session` and `User`) actually correct?**
  _`UserCreate` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Any`, `Parses a raw .eml string and extracts headers, body text, and links.     Uses be`, `User` to the rest of the system?**
  _261 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.13170731707317074 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._