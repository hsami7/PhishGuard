# Phase 3: Analysis Service Logic - Plan

## Goal
Implement a rule-based heuristic email analyzer inside the Python gRPC microservice.

## Proposed Changes

### Core Logic
#### [NEW] analysis/heuristics.py
- Create the `EmailAnalyzer` class.
- Implement rule functions for checking sender, subject, body, and URLs.
- Aggregate scores and map to Risk Levels (Low, Medium, High).

### gRPC Server Update
#### [MODIFY] analysis/server.py
- Import `EmailAnalyzer`.
- In `AnalyzeEmail` method, pass the request parameters to the analyzer.
- Return the actual calculated `score_level`, `numeric_score`, and `justification` instead of the dummy response.

### Testing Utilities
#### [NEW] scripts/test_grpc.py
- Create a simple python script acting as a gRPC client.
- Send two test emails (one benign, one malicious) and print the output.

## Verification Plan
- Run `python analysis/server.py` to start the backend.
- Run `python scripts/test_grpc.py` in a separate terminal.
- Verify the outputs align with the expected heuristic scores.
