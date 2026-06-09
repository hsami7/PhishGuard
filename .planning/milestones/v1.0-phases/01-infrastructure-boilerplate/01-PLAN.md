# Phase 1: Infrastructure & Boilerplate - Plan

## Goal
Set up the foundational structures for FastAPI, SQLite, and gRPC communication to enable future security and analysis features.

## Proposed Changes

### Dependencies & Setup

#### [NEW] requirements.txt
- Add core dependencies: `fastapi`, `uvicorn`, `grpcio`, `grpcio-tools`, `sqlalchemy`, `jinja2`, `python-multipart`.

### API Gateway & Web App

#### [NEW] app/main.py
- Initialize the FastAPI application.
- Mount static files and set up Jinja2Templates.
- Add a basic `/health` endpoint to verify startup.

#### [NEW] templates/base.html
- Base HTML skeleton using Tailwind CSS via CDN.
- Basic dark mode styling (Tokyo Night / Catppuccin flavor) as requested by `ui-ux-pro-max`.

### Database Skeleton

#### [NEW] app/database.py
- Configure SQLAlchemy with a SQLite URL (`sqlite:///./phishguard.db`).
- Setup `SessionLocal` and `Base` declarative mapping.

### Analysis Service (gRPC)

#### [NEW] proto/analyzer.proto
- Define `AnalysisService` with an `AnalyzeEmail` RPC method.
- Define `EmailRequest` and `AnalyzeResponse` messages.

#### [NEW] scripts/generate_proto.sh
- Bash script containing the `grpc_tools.protoc` command to compile the protobuf file.

#### [NEW] analysis/server.py
- Python script to start the gRPC server on port `50051`.
- Implement a dummy response for `AnalyzeEmail` to satisfy the RPC contract.

## Verification Plan

### Automated Tests
- No unit tests in Phase 1 (focus is on boilerplate), but syntax checks will run.

### Manual Verification
- Execute `scripts/generate_proto.sh`.
- Start the gRPC server: `python analysis/server.py`.
- Start the FastAPI gateway: `uvicorn app.main:app --reload`.
- Navigate to `http://localhost:8000/health` to confirm the gateway is alive.
- Check if `phishguard.db` is created.
