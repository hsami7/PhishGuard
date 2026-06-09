# Phase 3: Analysis Service Logic - Research

## Technical Approach

**Core Concept**: 
The analysis is 100% heuristic. We will use simple rule-based scanning over the email components (sender, subject, text, URLs) to calculate a phishing probability score. No machine learning models or paid APIs are used.

**Heuristic Modularity**:
- We will encapsulate the rules in `analysis/heuristics.py` to keep the gRPC `server.py` clean.
- The `Analyzer` class will process an `EmailRequest` and return a numeric score between `0` and `100`, along with a justification list.

**Rules to Implement**:
1. **Urgency Keywords**: Words like "urgent", "immediate", "password", "bank", "suspend", "action required" in the subject or body add +20.
2. **Suspicious Sender**: Domains like `.xyz`, `.top` or IP-based email addresses add +30.
3. **URL Analysis**: If a URL contains an IP address instead of a domain, add +40. Too many URLs (> 3) add +10.
4. **Greeting**: Missing personalized greeting (e.g., "Dear Customer") adds +10.

**Scoring Buckets**:
- `0 - 29`: **Low** Risk
- `30 - 69`: **Medium** Risk
- `70 - 100`: **High** Risk

**gRPC Integration**:
- The `server.py` will instantiate the analyzer, pass the request parameters, and construct the `AnalyzeResponse` Protobuf message with the derived `score_level`, `numeric_score`, and joined `justification` list.
