# PhishGuard

PhishGuard is a high-performance, local-first email analysis platform. It evaluates email metadata and flags phishing risks using a 100% rule-based heuristic engine, ensuring data privacy without relying on external AI APIs.

## Architecture

PhishGuard utilizes a hybrid microservice architecture:
1. **FastAPI Gateway (`:8000`)**: Acts as the public entry point. It serves the premium "Dark Cyber" frontend UI (Vanilla HTML + Tailwind CSS + Jinja2) and manages JWT-based user authentication backed by SQLite.
2. **gRPC Analysis Microservice (`:50051`)**: A decoupled Python backend utilizing Protocol Buffers to securely process and calculate risk scores based on heuristic rules (suspicious domains, urgency keywords, raw IPs, etc.).

## Quickstart

### Prerequisites
- Python 3.9+
- `pip`

### 1. Installation

Clone the repository and install the dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate Protobuf Files
Before starting the services, generate the gRPC Python code from the `.proto` definition:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/analyzer.proto
```

### 3. Start the Services
You need to run both services simultaneously in separate terminal windows.

**Terminal 1 (Start the gRPC Backend):**
```bash
source venv/bin/activate
python analysis/server.py
```
*You should see: `INFO: Starting gRPC AnalysisService on port 50051`*

**Terminal 2 (Start the FastAPI Gateway):**
```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```
*You should see standard uvicorn logs.*

### 4. Access the Platform
Open your browser and navigate to:
[http://localhost:8000](http://localhost:8000)

1. Create a new account.
2. Log in.
3. Use the Dashboard to analyze email payloads and view the dynamic heuristic scores.

## Security Features
- Complete Password Hashing using `bcrypt`.
- Protected Routes via JWT Bearer Tokens.
- Graceful Degradation: If the gRPC backend is offline, the API returns a controlled `HTTP 503` instead of crashing.
