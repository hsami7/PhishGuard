# Phase 08: enhance-phishtank-intel-url-unshortener-advanced-spoofing-de - Context

**Gathered:** 2026-06-09
**Status:** Ready for planning

<domain>
## Phase Boundary

Enhance heuristics with URL unshortening, PhishTank intel, and advanced spoofing detection.
</domain>

<decisions>
## Implementation Decisions

### URL Unshortening
- **D-01:** Custom redirect follower
- Custom HTTP redirect follower using `requests` to avoid external API rate limits, despite being slightly slower.

### PhishTank Integration
- **D-02:** Local database download
- Download the PhishTank database locally for fast, private lookups, requiring a periodic update mechanism.

### Advanced Spoofing Logic
- **D-03:** Display Name heuristic
- Use Display Name mismatch heuristics (e.g., checking if display name implies trusted entity but domain doesn't match) since users only provide simplified text/metadata, not raw headers.

### the agent's Discretion
- None
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### General
- `analysis/heuristics.py` — Core scoring engine that will receive these enhancements.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `analysis/heuristics.py`: Contains the `EmailAnalyzer` class where logic needs to be integrated.

### Established Patterns
- Score-based heuristics capping at 100 with Low/Medium/High levels.
- Appending specific `justifications` for each hit.

### Integration Points
- `analyze` method in `EmailAnalyzer` needs updating to incorporate URL redirects and PhishTank DB checks.
</code_context>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches
</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope
</deferred>

---

*Phase: 08-enhance-phishtank-intel-url-unshortener-advanced-spoofing-de*
*Context gathered: 2026-06-09*
