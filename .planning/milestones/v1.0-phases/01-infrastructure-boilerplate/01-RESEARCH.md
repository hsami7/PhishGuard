# Phase 1: Infrastructure & Boilerplate - Research

## Technical Approach

**FastAPI Gateway**: 
- A minimal FastAPI app acting as the main entry point.
- Configured to use `jinja2` for templates and serve static files (CSS/JS).
- Serves as an API Gateway and frontend router.

**Analysis Service (gRPC)**:
- Requires an `analyzer.proto` file defining the service (e.g., `AnalyzeEmail` RPC taking `EmailRequest` and returning `AnalyzeResponse`).
- Will need `grpcio` and `grpcio-tools` in dependencies to compile the protobuf definition into python modules (`analyzer_pb2.py` and `analyzer_pb2_grpc.py`).

**Database (SQLite)**:
- Use SQLAlchemy with SQLite for straightforward integration and ORM support.
- Connection string: `sqlite:///./phishguard.db`.

**Frontend Setup**:
- A `templates` directory containing a `base.html`.
- Integrates Tailwind CSS via CDN for rapid styling without a build step.

**Directory Structure**:
- `/app` (FastAPI Gateway & Database config)
- `/analysis` (gRPC Python Service)
- `/proto` (Protobuf definitions)
- `/templates` (HTML)
- `/static` (CSS/JS/Assets)

## Architecture Integration
- The API Gateway acts as the gRPC client, calling the AnalysisService over `localhost:50051`.
- Both processes will run concurrently in local development.

## Risks
- gRPC connection errors if the AnalysisService is not started before the Gateway attempts to communicate.
- Protobuf compilation paths can sometimes cause import errors in Python; need to ensure the generated code is imported correctly.
