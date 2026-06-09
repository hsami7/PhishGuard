# Phase 6: Audit Logging & Final Polish - Validation Strategy

## Dimensions

1. **Observability**: Verify that interactions on the frontend result in structured logs being printed to the respective terminal windows (FastAPI terminal and gRPC terminal).
2. **Documentation**: Verify that `README.md` exists, is well-formatted, and clearly explains how to boot the system.

## Release Criteria

- [ ] Creating an account and logging in prints `INFO` logs in the FastAPI terminal.
- [ ] Submitting an email analysis prints `INFO` logs in the gRPC terminal showing the final calculated score.
- [ ] `README.md` contains startup instructions for both `uvicorn` and `python analysis/server.py`.
