# Phase 08: enhance-phishtank-intel-url-unshortener-advanced-spoofing-de - Research

## Objective
Identify the technical requirements and constraints for planning Phase 08 based on user decisions captured in `08-CONTEXT.md`.

## 1. URL Unshortening (Custom Redirect Follower)
**Context:** User chose to implement a custom HTTP redirect follower using Python's `requests` to avoid API limits.
**Research Findings:**
- `requests.get()` follows redirects automatically if `allow_redirects=True`.
- However, for security, we should manually control the redirect loop to prevent infinite redirect attacks or SSRF. We can do this by using `requests.Session` and checking the `Location` header, or configuring a strict timeout and a max redirect count.
- The unshortened URL needs to be analyzed by the rest of the heuristics engine.

## 2. PhishTank Integration (Local DB)
**Context:** User chose to download the PhishTank database locally for fast, private lookups.
**Research Findings:**
- PhishTank provides database dumps in CSV, XML, and JSON formats.
- Since we use SQLite (per `PROJECT.md`), we can import the PhishTank JSON or CSV directly into a new table (e.g., `phishtank_urls`).
- We need a script or a background worker (e.g., APScheduler or FastAPI background task) to periodically fetch and update the database, as downloading it on every request is not viable.
- The analysis logic simply queries this local table for the provided URLs.

## 3. Advanced Spoofing Logic (Display Name Heuristic)
**Context:** User chose to implement Display Name mismatch heuristics because only text/metadata is available.
**Research Findings:**
- A common spoofing technique is to set the display name to a trusted entity's name or domain (e.g., `"PayPal Support <hacker@ru.com>"` or `"security@paypal.com <badguy@xyz.com>"`).
- We can extract the display name using the `email.utils.parseaddr` module in Python.
- Heuristic logic: If the display name contains an "@" symbol or matches a list of high-profile domains/brands, but the actual sender domain does not match, we flag it with a high severity score.

## Validation Architecture
- We will need to write unit tests for the redirect follower, simulating redirect chains.
- We need tests that mock the local PhishTank DB.
- We need tests for display name extraction and mismatch detection.
