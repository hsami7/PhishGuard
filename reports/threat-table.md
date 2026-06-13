# PhishGuard — Tableau des Menaces et Contre-mesures

| # | Menace / Risk | Source PDF | Contre-mesure implémentée | Fichier |
|---|--------------|------------|--------------------------|---------|
| 1 | Mots de passe stockés en clair | §8 | bcrypt hashing via passlib | `app/security.py` |
| 2 | Tokens JWT journalisés | §8 | Tokens jamais loggés — seuls les usernames | `app/routers/auth.py` |
| 3 | Entrées malveillantes non validées | §8 | Pydantic schemas + parser preprocessing | `app/schemas.py`, `analysis/parser.py` |
| 4 | Accès non autorisé (pas de rôles) | §8 | RBAC admin/analyste avec 403 Forbidden | `app/security.py` |
| 5 | Messages d'erreur bavards (leak) | §8 | Erreurs génériques côté client ("service unavailable") | `app/routers/analysis.py` |
| 6 | Taille d'entrée illimitée | §8 | `max_length=50000` sur raw_email | `app/schemas.py` |
| 7 | Abus d'appels (brute force) | §8 | Rate limiting: 5/min register, 10/min login (slowapi) | `app/routers/auth.py` |
| 8 | Appel distant sans timeout | §5 | `timeout=10` sur appel gRPC | `app/routers/analysis.py` |
| 9 | Indisponibilité d'un service | §5 | gRPC RpcError → HTTP 503 gracieux | `app/routers/analysis.py` |
| 10 | Pas de traçabilité des événements | §5 | AuditService séparé (gRPC, port 50052) avec table audit_log | `audit/server.py` |
| 11 | Usurpation d'identité (spoofing) | §7 | Détection display name vs domaine + typosquatting (Levenshtein) | `analysis/heuristics.py` |
| 12 | Domaines suspects | §7 | 34 TLDs surveillés (.xyz, .top, .tk, .ml, .ga, etc.) | `analysis/heuristics.py` |
| 13 | URLs malveillantes | §7 | PhishTank lookup + IP brut dans URL + URL unshortening | `analysis/heuristics.py` |
| 14 | Ingénierie sociale (urgence) | §8 | 8 mots-clés d'urgence pondérés (subject +20, body +10) | `analysis/heuristics.py` |
| 15 | Risques de sérialisation/désérialisation | §8 | Protobuf (sécurisé) pour gRPC, Pydantic pour JSON | `protos/`, `app/schemas.py` |
| 16 | Pas d'audit des pièces jointes | §7 | Analyse MIME — détection .exe, .js, .docm, .pdf avec JS | `analysis/heuristics.py` |
| 17 | Attaque homograph (Unicode) | — | Détection des caractères Cyrillic/Latin similaires | `analysis/heuristics.py` |

## Données protégées

| Donnée | Protection |
|--------|-----------|
| Mots de passe | bcrypt hash, jamais en clair ni en logs |
| Tokens JWT | Non loggés, expiration 30 min |
| Emails analysés | Stockés en DB sans contenu brut (seulement métadonnées) |
| Rôles | Vérifiés côté serveur avant chaque endpoint protégé |
| Entrées | Validées par Pydantic + sanitization parser |
