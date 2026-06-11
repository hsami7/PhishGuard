# PhishGuard — Deep Gap Analysis: PDF Requirements vs. Actual Implementation

**Date:** June 11, 2026  
**Document:** Projet de fin de semestre — Plateforme distribuée de détection et qualification d'e-mails de phishing  
**Evaluator:** Ron Agent — Line-by-line code audit against every PDF requirement  

---

## How to Read This Report

Each PDF section is quoted verbatim (in French), then analyzed against the actual code. Status icons:
- ✅ = Fully implemented
- ⚠️ = Partially implemented / needs improvement
- ❌ = Missing or not implemented
- 🌟 = Bonus (beyond requirements)

---

## SECTION 1: Contexte (Context)

> *"Une organisation reçoit chaque jour des e-mails suspects : faux liens, demandes urgentes, usurpation d'identité, pièces jointes douteuses ou messages générés automatiquement pour tromper les utilisateurs."*

**Verdict:** ✅ The system addresses all mentioned threat types except attachment analysis.

---

## SECTION 2: Objectif général (General Objectives)

The PDF lists 6 objectives:

| # | Objective | Status | Implementation |
|---|-----------|--------|----------------|
| 1 | L'authentification des utilisateurs | ✅ | JWT + bcrypt via `/auth/register`, `/auth/token`, `/auth/me` |
| 2 | Soumission d'un e-mail suspect sous forme de texte ou métadonnées | ✅ | `POST /analysis/` accepts raw `.eml` text via `EmailAnalysisRequest.raw_email` |
| 3 | Analyse du contenu par un service dédié | ✅ | gRPC `AnalysisService` on port 50051, separate process |
| 4 | Attribution d'un score de risque : faible, moyen ou élevé | ✅ | Three-tier: Low (0-29), Medium (30-69), High (70-100) |
| 5 | Consultation de l'historique des signalements | ✅ | `GET /analysis/history` returns user's past analyses |
| 6 | Traçabilité des actions sensibles dans des logs d'audit | ⚠️ | Logging exists but not a separate `AuditService` (see Section 5) |

---

## SECTION 3: Travail demandé (Required Components)

The PDF requires **5 minimum components**:

### 3.1 AuthService
> *"Gère la connexion, la vérification d'un token simple et les rôles utilisateur / administrateur"*

**Status:** ✅ Fully implemented

**Evidence:**
- `app/routers/auth.py` — Register (`/auth/register`), Login (`/auth/token`), Me (`/auth/me`)
- `app/security.py` — JWT creation/verification with `python-jose`, bcrypt hashing via `passlib`
- `app/models.py` — User model with `role` column (defaults to `"analyst"`)
- `app/main.py` line 57 — Admin-only endpoint `/admin/stats` with role check
- `app/security.py` line 60 — `get_current_admin_user()` dependency enforces admin role

**Code quality:** Good. Proper password hashing, JWT with expiration (30 min), role-based access control with 403 Forbidden for non-admins.

### 3.2 SubmissionService / API Gateway
> *"Reçoit les signalements, valide les entrées et transmet les données aux autres services"*

**Status:** ✅ Fully implemented

**Evidence:**
- `app/main.py` — FastAPI gateway on port 8000
- `app/routers/analysis.py` — `POST /analysis/` receives `EmailAnalysisRequest`
- `app/schemas.py` — Pydantic models validate all inputs (`EmailAnalysisRequest`, `UserCreate`, etc.)
- `analysis/parser.py` — `parse_email()` extracts headers, body, and URLs from raw `.eml`
- `app/routers/analysis.py` lines 36-46 — Gateway forwards parsed data to gRPC AnalysisService

**Code quality:** Clean separation. The gateway handles auth, parsing, and delegation. Input validation via Pydantic.

### 3.3 AnalysisService
> *"Analyse le message à l'aide de règles simples, d'un score heuristique ou d'un moteur léger"*

**Status:** ✅ Fully implemented (and exceeds requirements)

**Evidence:**
- `analysis/server.py` — gRPC service on port 50051
- `analysis/heuristics.py` — 267-line heuristic engine with:
  - Suspicious TLD detection (6 TLDs)
  - Raw IP address detection (sender + URLs)
  - Display name spoofing detection (brand impersonation, @-trick)
  - Typosquatting detection (Levenshtein distance ≤ 2)
  - Urgency keyword scanning (8 keywords, subject + body weighted differently)
  - Generic greeting detection (2 patterns)
  - Excessive URL counting (>3)
  - PhishTank database lookup (SQLite)
  - URL unshortening (HTTP HEAD with redirect following)
  - Legitimate brand trust heuristic (score reduction when domain matches links)
  - ML classifier (Logistic Regression + TF-IDF, up to 30 bonus points)

**Code quality:** Excellent. Far beyond "règles simples" — this is a sophisticated multi-layered engine.

### 3.4 AuditService
> *"Enregistre les événements de sécurité et les erreurs importantes"*

**Status:** ⚠️ Partially implemented — NOT a separate service

**What exists:**
- Python `logging` is used throughout (`logging.getLogger(__name__)` in every module)
- `auth.py` line 37: `logger.info(f"New user registered: {new_user.username}")`
- `auth.py` line 53: `logger.info(f"User logged in: {user.username}")`
- `analysis.py` line 35: `logger.info(f"User '{current_user.username}' requested analysis for sender: {sender}")`
- `analysis.py` line 66: `logger.error(f"gRPC service unavailable: {e}")`
- `server.py` line 23: `logger.info(f"Received analysis request for sender: {request.sender}")`
- `server.py` line 38: `logger.info(f"Analysis complete - Sender: {request.sender} | Score: ...")`

**What's missing:**
- The PDF explicitly asks for a separate **AuditService** component. The spec says: *"API Gateway → AuditService pour les événements sensibles"*
- Currently, logging is inline within each module — there is no dedicated audit microservice
- No structured audit log file or database table for security events
- No audit trail for: failed login attempts, unauthorized access attempts, analysis submissions

**Impact:** This is a gap in the distributed architecture. The PDF wants 4+ separate services communicating, but audit is just `print()`-style logging.

### 3.5 Client
> *"Interface console, mini interface web ou script de test permettant d'utiliser la plateforme"*

**Status:** ✅ Fully implemented (web UI + test scripts)

**Evidence:**
- `templates/` — 5 Jinja2 HTML templates (base, index, login, register, dashboard)
- `templates/dashboard.html` — 342-line SPA with glassmorphism design, score ring animation, history table
- `scripts/test_grpc.py` — Standalone gRPC test client
- `test_register.py` — Registration test script
- `test_error.py` — Error handling test

**Code quality:** The dashboard is genuinely polished — animated SVG score ring, color-coded results, extracted headers/URLs display, history table with auto-refresh.

---

## SECTION 4: Données minimales à gérer (Minimum Data Fields)

The PDF requires 8 data fields:

| # | Field | Status | Implementation |
|---|-------|--------|----------------|
| 1 | Identifiant du signalement | ✅ | `AnalysisHistory.id` (auto-increment PK) |
| 2 | Expéditeur déclaré | ✅ | `AnalysisHistory.sender` + parsed from email headers |
| 3 | Objet de l'e-mail | ✅ | `AnalysisHistory.subject` + parsed from email headers |
| 4 | Contenu textuel ou extrait | ✅ | `EmailAnalysisRequest.raw_email` (full raw text stored in request) |
| 5 | Liste éventuelle d'URLs détectées | ✅ | `parsed["urls"]` — regex-extracted, deduplicated |
| 6 | Date de soumission | ✅ | `AnalysisHistory.created_at` (DateTime with `func.now()`) |
| 7 | Utilisateur ayant soumis l'alerte | ✅ | `AnalysisHistory.user_id` (FK to users table) |
| 8 | Score de risque | ✅ | `AnalysisHistory.score_level` + `AnalysisHistory.numeric_score` |
| 9 | Justification courte du score | ✅ | Returned in API response (pipe-delimited string) |

**Note:** The justification is returned in the API response but NOT stored in the database. The `AnalysisHistory` table doesn't have a `justification` column. This means historical records lose their explanations.

---

## SECTION 5: Fonctionnalités minimales obligatoires (Mandatory Features)

### 5.1 Authentification et autorisation

| Requirement | Status | Details |
|-------------|--------|---------|
| Connexion avec login et mot de passe | ✅ | `POST /auth/token` with OAuth2 password flow |
| Retour d'un token ou session simplifiée | ✅ | JWT access token returned |
| Refus des accès non authentifiés | ✅ | All `/analysis/*` routes require valid JWT |
| Au moins 2 rôles: admin + analyste | ✅ | `role` column: `"admin"` and `"analyst"` (default) |

### 5.2 Soumission et analyse

| Requirement | Status | Details |
|-------------|--------|---------|
| Soumettre un e-mail suspect | ✅ | `POST /analysis/` with raw email text |
| Vérifier et nettoyer les entrées côté serveur | ✅ | Pydantic validation + `parser.preprocess_raw_email()` |
| Calculer un score de risque à partir de règles explicables | ✅ | Heuristic engine with 10+ rule categories |
| Retourner une décision lisible: faible, moyen, élevé | ✅ | `score_level` field: "Low", "Medium", "High" |

### 5.3 Consultation

| Requirement | Status | Details |
|-------------|--------|---------|
| Lister les signalements | ✅ | `GET /analysis/history` |
| Consulter le détail d'un signalement | ⚠️ | History list exists but no single-record detail endpoint |
| **Rechercher par expéditeur, score ou mot-clé** | ❌ | **No search/filter parameters on history endpoint** |

**Gap:** The PDF explicitly requires search by sender, score, or keyword. The current `GET /analysis/history` just returns all records for the user with no query parameters.

### 5.4 Audit et résilience

| Requirement | Status | Details |
|-------------|--------|---------|
| Générer des logs structurés | ⚠️ | Logging exists but not structured (no JSON format, no audit table) |
| **Ajouter au moins un timeout sur un appel distant** | ❌ | **No gRPC timeout configured** |
| Gérer proprement l'indisponibilité d'un service | ✅ | `grpc.RpcError` caught → HTTP 503 returned |
| Renvoyer des erreurs non bavardes côté client | ✅ | Generic error messages like "Analysis service is currently unavailable" |

**Gap 1:** The gRPC call in `analysis.py` line 36 uses `grpc.insecure_channel('localhost:50051')` with no timeout. The PDF explicitly requires at least one timeout on a remote call.

**Gap 2:** Logs go to stdout/stderr but there's no structured audit trail (no dedicated audit log file, no database table for security events).

---

## SECTION 6: Contraintes techniques (Technical Constraints)

| Constraint | Status | Details |
|------------|--------|---------|
| Python uniquement | ✅ | 100% Python |
| Architecture répartie avec au moins 3 composants | ✅ | FastAPI gateway + gRPC AnalysisService + SQLite (3 processes) |
| Échanges en JSON pour les appels API | ✅ | FastAPI REST endpoints use JSON |
| Au moins un mécanisme RPC (gRPC ou Pyro5) | ✅ | gRPC with Protocol Buffers |
| Validation stricte des entrées côté serveur | ✅ | Pydantic schemas + parser preprocessing |
| Journalisation structurée | ⚠️ | Basic logging, not structured JSON |
| Code organisé par services, modules et responsabilités | ✅ | Clean separation: `app/`, `analysis/`, `proto/`, `templates/` |
| Aucune dépendance API payante ou cloud | ✅ | 100% local |
| Démontrable localement sur une seule machine | ✅ | Runs entirely locally |

---

## SECTION 7: Orientation de l'analyse (Analysis Direction)

The PDF suggests these detection methods:

| Method | Status | Details |
|--------|--------|---------|
| Détection de mots urgents ou manipulateurs | ✅ | 8 urgency keywords in subject (+20) and body (+10) |
| Détection de domaines suspects ou URLs inhabituelles | ✅ | 6 suspicious TLDs + IP address detection |
| Écart entre l'adresse affichée et le domaine détecté | ✅ | Display name spoofing + typosquatting (Levenshtein) |
| **Présence de pièces jointes annoncées dans les métadonnées** | ❌ | **No attachment analysis** |
| Score cumulatif basé sur des règles | ✅ | Cumulative scoring with 10+ rule categories |
| Explication textuelle des raisons du score | ✅ | Pipe-delimited justification string |

**Gap:** The PDF specifically mentions checking for announced attachments in metadata. The system doesn't parse or flag attachments at all.

---

## SECTION 8: Exigences cybersécurité (Security Requirements)

| Requirement | Status | Details |
|------------|--------|---------|
| Ne jamais stocker ni afficher les mots de passe en clair | ✅ | bcrypt hashing, `hashed_password` column |
| Ne pas journaliser les tokens complets | ✅ | Tokens not logged |
| Valider toutes les entrées côté serveur | ✅ | Pydantic + parser validation |
| Contrôler les rôles et les permissions | ✅ | Admin/analyst RBAC with 403 enforcement |
| Messages d'erreur génériques côté client | ✅ | "Analysis service is currently unavailable" (no stack traces) |
| Réflexion sur les risques de sérialisation | ⚠️ | Protobuf used (safe), but no documentation of serialization risks |
| **Limiter la taille des entrées** | ❌ | **No `max_length` on `raw_email` field** |
| **Protection contre l'abus d'appels** | ❌ | **No rate limiting anywhere** |
| **Documenter les menaces principales et contre-mesures** | ❌ | **No threat model document** |

**Gap 1:** The `EmailAnalysisRequest.raw_email` field has no maximum length. A user could submit a multi-GB file.

**Gap 2:** No rate limiting on any endpoint. The PDF explicitly asks for "un minimum de protection contre l'abus d'appels."

**Gap 3:** No threat documentation exists in the repo.

---

## SECTION 9: Architecture attendue (Expected Architecture)

The PDF suggests:
```
Client → API Gateway → AuthService (verify identity)
Client → API Gateway → AnalysisService (scoring)
Client → API Gateway → AuditService (sensitive events)
Storage: SQLite or JSON files
```

**Your architecture:**
```
Browser → FastAPI Gateway (:8000) → gRPC AnalysisService (:50051)
                                    → SQLite (users, history, phishtank)
                                    → Auth (inline, not separate service)
                                    → Audit (inline logging, not separate service)
```

**Verdict:** ⚠️ Close, but Auth and Audit are not separate services — they're inline modules within the FastAPI gateway. The PDF's example architecture shows 4 distinct services.

---

## SECTION 10: Livrables (Deliverables)

| Deliverable | Status | Details |
|------------|--------|---------|
| Code source complet | ✅ | All source files present |
| README avec instructions | ✅ | Complete README with install/run steps |
| **Schéma d'architecture** | ❌ | **No architecture diagram found** |
| **Rapport synthétique de 4 à 8 pages** | ❌ | **No formal report found** |
| Jeu de données de démonstration | ✅ | `spam_ham_dataset.csv` (5,572 records) |
| Captures d'écran ou script de démonstration | ⚠️ | Test scripts exist, no screenshots |
| **Tableau des menaces et protections** | ❌ | **No threat/countermeasure table** |

**3 out of 7 deliverables are missing.** These are documentation artifacts, not code issues.

---

## SECTION 11: Démonstration attendue (Expected Demo)

| Demo Requirement | Status | Details |
|-----------------|--------|---------|
| Connexion d'un utilisateur | ✅ | Login page + JWT flow |
| Soumission d'un e-mail suspect | ✅ | Dashboard textarea + analysis |
| Appel entre au moins deux services | ✅ | FastAPI → gRPC |
| Retour d'un score de risque | ✅ | Animated score ring + level |
| Refus d'un accès non autorisé | ✅ | 401/403 responses |
| Exemple d'erreur gérée proprement | ✅ | 503 when gRPC is down |
| Exemple de log d'audit | ⚠️ | Logs exist but not shown in UI |
| Explication rapide d'un choix de sécurité | ❌ | No security justification document |

---

## SECTION 13: Critères d'évaluation (Grading Criteria)

### 30% — Distributed operation and inter-service communication
**Score: 27/30** ✅
- Real gRPC communication between FastAPI and AnalysisService ✅
- Protocol Buffers serialization ✅
- JSON REST API ✅
- 3+ components communicating ✅
- **Deduction (-3):** No gRPC timeout configured, Auth/Audit not separate services

### 25% — Technical quality and code organization
**Score: 23/25** ✅
- Clean module separation ✅
- Pydantic validation ✅
- Proper error handling ✅
- Sophisticated heuristic engine ✅
- **Deduction (-2):** No input size limits, hardcoded SECRET_KEY

### 25% — Cybersecurity: validation, access control, error handling, logs
**Score: 18/25** ⚠️
- Password hashing (bcrypt) ✅
- JWT authentication ✅
- Role-based access control ✅
- Generic error messages ✅
- Graceful degradation (503) ✅
- **Deduction (-7):** No rate limiting (-3), no input size limits (-2), no structured audit trail (-1), no serialization risk documentation (-1)

### 20% — Report, demo, and justification of choices
**Score: 8/20** ❌
- README exists ✅
- Test scripts exist ✅
- **Deduction (-12):** No architecture diagram (-3), no 4-8 page report (-4), no threat/countermeasure table (-3), no screenshots (-2)

---

## BONUS FEATURES (from PDF Section 14)

| Bonus | Status |
|-------|--------|
| Tableau de bord web simple | ✅ Full glassmorphism dashboard |
| Comparaison JSON vs Protobuf | ✅ Uses both (REST + gRPC) |
| Mini système de file d'attente | ❌ Not implemented |
| Circuit breaker simplifié | ❌ Not implemented |
| Versionnement d'un signalement | ❌ Not implemented |
| Analyse automatique d'URLs plus détaillée | ✅ URL unshortening + PhishTank + typosquatting |
| Intégration d'un service RPC clairement séparé | ✅ gRPC AnalysisService on separate port |

**3 out of 7 bonuses achieved.**

---

## COMPLETE FILE-BY-FILE INVENTORY

### Core Application Files
| File | Purpose | Lines | Quality |
|------|---------|-------|---------|
| `app/main.py` | FastAPI app, routes, startup | 58 | Clean |
| `app/database.py` | SQLAlchemy engine + session | 19 | Standard |
| `app/models.py` | User + AnalysisHistory ORM models | 24 | Clean |
| `app/schemas.py` | Pydantic request/response models | 46 | Clean |
| `app/security.py` | JWT, bcrypt, role checks | 66 | Good |
| `app/routers/auth.py` | Register, login, me endpoints | 58 | Good |
| `app/routers/analysis.py` | Analyze + history endpoints | 75 | Good |

### Analysis Engine Files
| File | Purpose | Lines | Quality |
|------|---------|-------|---------|
| `analysis/heuristics.py` | Scoring engine (10+ rule types) | 267 | Excellent |
| `analysis/parser.py` | Raw .eml parser + URL extractor | 107 | Good |
| `analysis/server.py` | gRPC service wrapper | 51 | Clean |
| `analysis/train_model.py` | ML model training script | 164 | Good |

### Proto / gRPC
| File | Purpose |
|------|---------|
| `proto/analyzer.proto` | Service definition (EmailRequest → AnalyzeResponse) |
| `proto/analyzer_pb2.py` | Generated protobuf code |
| `proto/analyzer_pb2_grpc.py` | Generated gRPC stubs |

### Templates (5 files)
| File | Purpose |
|------|---------|
| `templates/base.html` | Layout with Tailwind, glassmorphism CSS, nav |
| `templates/index.html` | Landing page |
| `templates/login.html` | Login form with JWT |
| `templates/register.html` | Registration form |
| `templates/dashboard.html` | Full analysis UI (342 lines, SPA-style) |

### Test / Script Files
| File | Purpose |
|------|---------|
| `scripts/test_grpc.py` | Standalone gRPC client test |
| `test_register.py` | Registration endpoint test |
| `test_error.py` | Basic error handling test |
| `run_test_server.py` | Server startup test |
| `test_comprehensive.py` | 29-email test suite (my addition) |
| `test_pipeline.py` | 5 raw .eml pipeline tests (my addition) |

### Data Files
| File | Size | Purpose |
|------|------|---------|
| `data/spam_ham_dataset.csv` | 5.5 MB | ML training data (5,572 emails) |
| `analysis/email_classifier.pkl` | 40 KB | Trained Logistic Regression model |
| `analysis/vectorizer.pkl` | 187 KB | TF-IDF vectorizer |
| `phishguard.db` | — | SQLite (users, history, phishtank URLs) |

---

## SUMMARY: WHAT YOU DID vs. WHAT PDF ASKS

### ✅ What You Built (Strong Points)
1. **Complete distributed architecture** — FastAPI + gRPC, two separate processes communicating
2. **Sophisticated heuristic engine** — 10+ detection categories, far beyond "règles simples"
3. **ML integration** — Logistic Regression classifier trained on real phishing datasets
4. **Polished web UI** — Glassmorphism dashboard with animated score ring, history table
5. **Proper security** — bcrypt, JWT, RBAC, generic error messages, graceful degradation
6. **Email parser** — Handles raw .eml, multipart, HTML, malformed emails
7. **gRPC with Protocol Buffers** — Real RPC, not just HTTP
8. **Test scripts** — gRPC client test, registration test, error test

### ❌ What's Missing (Gaps to Close)

| # | Missing Item | PDF Section | Impact | Effort |
|---|-------------|-------------|--------|--------|
| 1 | **Search by sender/score/keyword** | §5 Consultation | Required feature | Low — add query params to `/history` |
| 2 | **gRPC timeout** | §5 Audit et résilience | Explicitly required | Low — add `timeout=` to gRPC call |
| 3 | **Rate limiting** | §8 Cybersécurité | Explicitly required | Medium — add slowapi or middleware |
| 4 | **Input size limits** | §8 Cybersécurité | Explicitly required | Low — add `max_length` to Pydantic |
| 5 | **Attachment analysis** | §7 Orientation | Explicitly mentioned | Medium — parse MIME parts for attachments |
| 6 | **Separate AuditService** | §3 Travail demandé | Architecture gap | Medium — extract logging to separate service |
| 7 | **Architecture diagram** | §10 Livrables | Required deliverable | Low — draw with excalidraw/diagrams.net |
| 8 | **4-8 page report** | §10 Livrables | Required deliverable | Medium — write the report |
| 9 | **Threat/countermeasure table** | §10 Livrables | Required deliverable | Low — document threats you addressed |
| 10 | **Justification not stored in DB** | §4 Données | Data gap | Low — add column to AnalysisHistory |
| 11 | **Hardcoded SECRET_KEY** | §8 Cybersécurité | Security issue | Low — use env variable |
| 12 | **No screenshots** | §10 Livrables | Deliverable gap | Low — take screenshots of the UI |

---

## ESTIMATED GRADE

| Criterion | Weight | Your Score | Weighted |
|-----------|--------|------------|----------|
| Distributed communication | 30% | 27/30 | 27.0 |
| Code quality | 25% | 23/25 | 23.0 |
| Cybersecurity | 25% | 18/25 | 18.0 |
| Report + demo + justification | 20% | 8/20 | 8.0 |
| **TOTAL** | **100%** | | **76/100** |

**Estimated Grade: 15.2/20 (B+)**

The code and architecture are strong — you'd score ~90% on the technical criteria. The missing points are almost entirely in **documentation** (report, diagram, threat table) and a few **security hardening** items (rate limiting, input limits, timeouts). These are quick wins that could push you to 17+/20.

---

## TOP 5 PRIORITY FIXES (Before Defense)

1. **Add search to history endpoint** — `GET /analysis/history?sender=...&score=...&keyword=...` (30 min)
2. **Add gRPC timeout** — `stub.AnalyzeEmail(grpc_req, timeout=10)` (5 min)
3. **Add rate limiting** — `slowapi` on auth endpoints (1 hour)
4. **Draw architecture diagram** — Client → Gateway → Auth/Analysis/Audit → SQLite (30 min)
5. **Write the threat table** — List each PDF security requirement and how you addressed it (1 hour)

These 5 fixes would close the biggest gaps and could gain you 4-5 more points.
