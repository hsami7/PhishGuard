# Phase 08: enhance-phishtank-intel-url-unshortener-advanced-spoofing-de - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-09
**Phase:** 08-enhance-phishtank-intel-url-unshortener-advanced-spoofing-de
**Areas discussed:** URL Unshortening, PhishTank Integration, Advanced Spoofing Logic

---

## URL Unshortening

| Option | Description | Selected |
|--------|-------------|----------|
| Custom redirect follower | (using `requests`, private, no external API limits) | ✓ |
| External API service | (faster to implement, but has rate limits/privacy concerns) | |

**User's choice:** Custom redirect follower (using `requests`, private, no external API limits)
**Notes:** None

---

## PhishTank Integration

| Option | Description | Selected |
|--------|-------------|----------|
| Local database download | (Faster and more private, but requires periodic update mechanism) | ✓ |
| Live API queries | (Always up to date, but adds network latency per email) | |

**User's choice:** Local database download (Faster and more private, but requires periodic update mechanism)
**Notes:** None

---

## Advanced Spoofing Logic

| Option | Description | Selected |
|--------|-------------|----------|
| Display Name heuristic | (Check if display name implies trusted entity but domain doesn't match) | ✓ |
| Other | (require user to input raw SPF/DKIM headers) | |

**User's choice:** Display Name heuristic (Check if the display name implies a trusted entity but the email domain does not match, e.g., 'PayPal Support <hacker@ru.com>')
**Notes:** None

---

## the agent's Discretion

None

## Deferred Ideas

None
