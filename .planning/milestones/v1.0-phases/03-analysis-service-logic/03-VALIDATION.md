# Phase 3: Analysis Service Logic - Validation Strategy

## Dimensions

1. **Rule Evaluation**: Verify that specific triggers (e.g., IP addresses in URLs) correctly elevate the risk score.
2. **gRPC Integration**: Verify that the gRPC server properly maps the analyzer output to the Protobuf response format.
3. **End-to-End Execution**: Verify that a client can send an email via gRPC and receive a valid score.

## Release Criteria

- [ ] A test script (`scripts/test_grpc.py`) can successfully connect to the gRPC server on port `50051`.
- [ ] Submitting a benign email (normal sender, no urgency, no URLs) returns a "Low" score.
- [ ] Submitting a phishing email ("Action Required", IP URL, suspicious sender) returns a "High" score.
- [ ] The `justification` field clearly explains why the score was given.
