# Context: Phase 09

## Domain
Automated Email Parsing Engine (1 plans)

## Canonical refs
- (No external specs referenced)

## Decisions
- **Handling Malformed Emails**: Best-effort extraction — spam is often intentionally malformed; grab whatever text/headers we can find.
- **Body Preference**: Merge both — Harvest links from both the plain text and HTML parts, deduplicating them.
- **URL Regex Strictness**: Strict — Only extract fully qualified URLs that begin with `http://` or `https://` to avoid false positives.
