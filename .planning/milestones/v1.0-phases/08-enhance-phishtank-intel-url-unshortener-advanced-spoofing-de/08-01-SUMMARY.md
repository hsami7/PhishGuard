---
phase: "08"
plan: "08-01"
subsystem: "heuristics"
tags: ["security", "url-unshortening", "spoofing-detection", "phishtank"]
tech-stack:
  added: ["requests"]
key-files:
  modified: ["analysis/heuristics.py", "app/main.py", "requirements.txt"]
requirements-completed: ["CORE-01"]
duration: "10 min"
completed: "2026-06-09T16:38:00Z"
---

# Phase 08 Plan 01: Enhance Heuristics & Analysis Summary

Implemented URL unshortening, local PhishTank DB queries, and advanced display name spoofing heuristics to significantly increase the accuracy of the email analysis engine.

## Execution Metrics
- **Duration**: 10 minutes
- **Tasks Completed**: 2
- **Files Modified**: 3

## What Was Done
- **URL Unshortening**: Added `_unshorten_url` to `EmailAnalyzer` utilizing the `requests` library to follow up to 5 HTTP redirects gracefully.
- **PhishTank Database**: Added `_check_phishtank` to lookup extracted domains against the `phishtank_urls` SQLite table in `phishguard.db`.
- **Display Name Spoofing**: Implemented `_detect_spoofing` using `email.utils.parseaddr` to identify high-profile brand domain mismatches and detect malicious `@` symbols injected into the display name.
- **Application Startup**: Updated `app/main.py` to run a `CREATE TABLE IF NOT EXISTS phishtank_urls` query during FastAPI's `on_startup` event, ensuring the heuristics don't crash when querying the local intel database.

## Deviations from Plan
None - plan executed exactly as written.

## Self-Check: PASSED
- `analysis/heuristics.py` successfully contains the new methods and `_unshorten_url` explicitly manages redirects safely.
- `app/main.py` includes the proper SQLite table initialization.
- Syntax checks passed successfully.

## Next Steps
Phase complete, ready for next step.
