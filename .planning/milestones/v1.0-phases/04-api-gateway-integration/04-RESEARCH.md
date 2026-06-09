# Phase 4: API Gateway Integration - Research

## Technical Approach

**Core Concept**: 
The frontend clients (React/Vue/Mobile) should not communicate directly via gRPC. Instead, the FastAPI backend acts as an API Gateway. It exposes RESTful JSON endpoints, secures them with JWT, and forwards the business logic to the internal gRPC service.

**Schema Definitions**:
- We need Pydantic models in `app/schemas.py` to validate incoming POST data.
- `EmailAnalysisRequest`: `sender` (str), `subject` (str), `text_content` (str), `urls` (list of str).
- `EmailAnalysisResponse`: `score_level` (str), `numeric_score` (int), `justification` (str).

**Route & Security**:
- Endpoint: `POST /analysis/`
- Protection: `Depends(get_current_user)` ensures only authenticated users can trigger the analysis.
- The route will use the Python `grpc.insecure_channel` to communicate with `localhost:50051`.

**Error Handling**:
- If the gRPC backend is offline, the channel will raise a `grpc.RpcError`. We must catch this and return a clean HTTP 503 (Service Unavailable) to the client so the frontend can handle it gracefully.
