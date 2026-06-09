# Phase 4: API Gateway Integration - Validation Strategy

## Dimensions

1. **Access Control**: Verify that unauthenticated requests to `/analysis/` are firmly rejected.
2. **Data Transformation**: Verify that JSON requests are properly unpacked, passed via Protobuf to the gRPC service, and the Protobuf response is serialized back to JSON.
3. **Resilience**: Verify that a failure in the gRPC backend doesn't crash the FastAPI server, but instead returns a `503`.

## Release Criteria

- [ ] `POST /analysis/` without a JWT header returns `401 Unauthorized`.
- [ ] `POST /analysis/` with a valid JWT header returns a `200 OK` and the correct analysis score (`{"score_level": "...", "numeric_score": ...}`).
- [ ] Stopping the gRPC server (`analysis/server.py`) and sending a valid `POST /analysis/` request returns `503 Service Unavailable`.
