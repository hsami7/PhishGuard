# Phase 4: API Gateway Integration - Plan

## Goal
Connect the FastAPI gateway with the internal gRPC analysis microservice, secured by JWT authentication.

## Proposed Changes

### Pydantic Schemas
#### [MODIFY] app/schemas.py
- Add `EmailAnalysisRequest` class.
- Add `EmailAnalysisResponse` class.

### Analysis Router
#### [NEW] app/routers/analysis.py
- Create a new APIRouter.
- Define `POST /` endpoint.
- Require `Depends(get_current_user)`.
- Establish gRPC channel to `localhost:50051`.
- Catch `grpc.RpcError` and raise `HTTPException(503)`.

### Gateway Registration
#### [MODIFY] app/main.py
- Import the new `analysis` router.
- Register it with `app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])`.

## Verification Plan
- Boot both servers (`uvicorn app.main:app` and `python analysis/server.py`).
- Use Swagger UI to acquire a token.
- Submit an email payload via the UI to `/analysis/` and verify the JSON response.
- Kill the python server and submit again to verify the `503` error handling.
