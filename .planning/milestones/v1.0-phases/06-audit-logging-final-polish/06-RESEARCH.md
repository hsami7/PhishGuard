# Phase 6: Audit Logging & Final Polish - Research

## Technical Approach

**Audit Logging**:
- We will integrate Python's standard `logging` library across both services (FastAPI and gRPC).
- **FastAPI Gateway (`app/routers/auth.py`, `app/routers/analysis.py`)**: 
  - Log successful user registrations.
  - Log login attempts.
  - Log incoming analysis requests and any `503` communication errors with the gRPC service.
- **gRPC Analysis Service (`analysis/server.py`, `analysis/heuristics.py`)**:
  - Log when the server boots.
  - Log every incoming email analysis request alongside the final calculated risk score (`Low`, `Medium`, `High`) and numeric value.

**Final Polish (Documentation)**:
- We will completely overwrite the `README.md` at the root of the project.
- It will document the Hybrid Architecture (REST API Gateway + Python gRPC Microservice).
- It will explain the 100% Rule-Based Heuristic engine.
- It will provide clear, copy-pasteable instructions for booting both servers simultaneously for local development.
