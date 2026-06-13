# PhishGuard

**Plateforme distribuée de détection et qualification d'e-mails de phishing**

PhishGuard est une application Python qui analyse les e-mails pour détecter les tentatives de phishing. Elle utilise un moteur heuristique multi-couches (12 règles + ML) et expose une interface web moderne.

**Développé par Hatim Sami — Juin 2026**

---

## Architecture

3 services distribués communiquant entre eux :

| Service | Port | Protocole | Rôle |
|---------|------|-----------|------|
| **FastAPI Gateway** | 8000 | HTTPS/JSON | Auth JWT, validation, UI web, rate limiting |
| **AnalysisService** | 50051 | gRPC/Protobuf | Moteur heuristique 12 règles + ML, score 0-100 |
| **AuditService** | 50052 | gRPC/Protobuf | Journalisation structurée des événements de sécurité |

**Stockage :** SQLite (`phishguard.db`) — 4 tables : `users`, `analysis_history`, `phishtank_urls`, `audit_log`

---

## Démarrage rapide

### Prérequis
- Python 3.9+
- pip

### Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Compilation Protobuf
```bash
python -m grpc_tools.protoc -I protos --python_out=protos --grpc_python_out=protos protos/analyzer.proto
python -m grpc_tools.protoc -I protos --python_out=protos --grpc_python_out=protos protos/audit.proto
```

### Démarrage des 3 services

**Terminal 1 — AnalysisService :**
```bash
python analysis/server.py
```

**Terminal 2 — AuditService :**
```bash
python audit/server.py
```

**Terminal 3 — Gateway :**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Accès
Naviguer vers `http://localhost:8000` → Créer un compte → Dashboard

---

## Fonctionnalités

### Moteur d'analyse (12 catégories)
1. **Spoofing** — Display name imite un brand (+40)
2. **Typosquatting** — Levenshtein ≤ 2 vs brands connus (+40)
3. **TLD suspect** — 34 TLDs surveillés (+30)
4. **IP brute** — Expéditeur ou URL en IP (+30)
5. **Urgence** — Mots-clés manipulateurs (+20 sujet, +10 corps)
6. **Salutation générique** — "Dear Customer/User" (+10)
7. **Scam keywords** — 39 mots-clés (+15/unité, max +45)
8. **Densité emojis** — ≥5 emojis (+20)
9. **Domaines numériques** — Ex: 866698.com (+20)
10. **Problèmes URL** — PhishTank, IP, excess (+10 à +50)
11. **ML classifier** — LogReg + TF-IDF, ~200k emails (+0 à +30)
12. **Brand Trust** — Domaine reconnu, liens cohérents (-40)

### Interface web
- Page d'accueil avec CTA
- Inscription / Connexion (JWT)
- Dashboard d'analyse avec score animé, catégorie colorée, justification
- Historique avec recherche par mot-clé, expéditeur, catégorie

### Sécurité
- bcrypt hashing, JWT (30 min expiry)
- RBAC admin/analyste (403 Forbidden)
- Rate limiting (5/min register, 10/min login)
- Validation stricte Pydantic
- Erreurs génériques côté client
- AuditService séparé avec table `audit_log`

---

## Structure du projet

```
PhishGuard/
├── app/                    # FastAPI Gateway
│   ├── main.py            # App FastAPI, routes, startup
│   ├── database.py        # SQLAlchemy engine + session
│   ├── models.py          # User, AnalysisHistory ORM
│   ├── schemas.py         # Pydantic request/response
│   ├── security.py        # JWT, bcrypt, RBAC
│   └── routers/
│       ├── auth.py        # /auth/register, /token, /me
│       └── analysis.py    # /analysis/, /history
├── analysis/              # AnalysisService (gRPC :50051)
│   ├── server.py          # gRPC servicer
│   ├── heuristics.py      # Moteur 12 règles + scoring
│   ├── parser.py          # Parseur .eml + extraction URLs
│   ├── train_model.py     # Entraînement ML
│   ├── email_classifier.pkl  # Modèle ML entraîné
│   └── vectorizer.pkl     # TF-IDF vectorizer
├── audit/                 # AuditService (gRPC :50052)
│   └── server.py          # gRPC servicer + audit_log table
├── protos/                # Définitions Protocol Buffers
│   ├── analyzer.proto     # EmailRequest → AnalyzeResponse
│   ├── analyzer_pb2.py    # Code généré
│   ├── analyzer_pb2_grpc.py
│   ├── audit.proto        # AuditEvent → AuditResponse
│   ├── audit_pb2.py       # Code généré
│   └── audit_pb2_grpc.py
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Layout + nav + footer
│   ├── index.html         # Landing page
│   ├── login.html         # Connexion
│   ├── register.html      # Inscription
│   └── dashboard.html     # Dashboard d'analyse (SPA)
├── static/                # Fichiers statiques
├── reports/               # Livrables
│   ├── rapport-synthetique.pdf    # Rapport 6 pages
│   ├── rapport-synthetique.md     # Source markdown
│   ├── architecture-diagram.excalidraw  # Schéma d'architecture
│   ├── threat-table.md            # Tableau menaces/contre-mesures
│   └── screenshots/               # 8 captures d'écran
├── scripts/               # Scripts utilitaires
│   ├── take_screenshots.py        # Génération des screenshots
│   └── generate_pdf.py            # Conversion MD → PDF
├── data/                  # Données
│   └── spam_ham_dataset.csv       # Dataset ML (5572 emails)
├── requirements.txt       # Dépendances Python
└── phishguard.db          # Base SQLite
```

---

## Tests

**Résultats : 97.1% accuracy (33/34 tests)**

| Catégorie | Tests | Succès | Taux |
|-----------|-------|--------|------|
| Phishing | 13 | 13 | 100% |
| Légitime | 11 | 10 | 90.9% |
| Spam/Junk | 5 | 5 | 100% |
| Edge cases | 5 | 5 | 100% |

---

## Livrables

- ✅ Code source complet
- ✅ README avec instructions
- ✅ Schéma d'architecture (`reports/architecture-diagram.excalidraw`)
- ✅ Rapport synthétique 6 pages (`reports/rapport-synthetique.pdf`)
- ✅ Jeu de données (`data/spam_ham_dataset.csv`)
- ✅ Captures d'écran (`reports/screenshots/`)
- ✅ Tableau menaces/contre-mesures (`reports/threat-table.md`)

---

## Licence

Projet académique — Module Applications réparties et cybersécurité
