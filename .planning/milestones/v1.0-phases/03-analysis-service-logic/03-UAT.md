---
status: complete
phase: 03-analysis-service-logic
source: 03-01-SUMMARY.md
started: 2026-06-09T00:40:30Z
updated: 2026-06-09T00:43:30Z
---

## Current Test

[testing complete]

## Tests

### 1. Cold Start Smoke Test
expected: Kill any running server/service. Clear ephemeral state. Start the gRPC server from scratch (`python analysis/server.py`). The server boots without errors and logs "AnalysisService gRPC server started on port 50051".
result: pass

### 2. Heuristic Engine - Benign Email Validation
expected: While the server is running, execute `python scripts/test_grpc.py` in another terminal. The "Testing Benign Email" section should output `Level: Low`, a low numerical score (<30), and `Justification: No threats detected.`
result: pass

### 3. Heuristic Engine - Phishing Email Validation
expected: In the output of `python scripts/test_grpc.py`, the "Testing Phishing Email" section should output `Level: High`, a high numerical score (>=70), and list multiple justifications (e.g., Sender contains raw IP address, Urgency keyword in subject/body, Generic greeting, URL contains raw IP).
result: pass

## Summary

total: 3
passed: 3
issues: 0
pending: 0
skipped: 0

## Gaps
