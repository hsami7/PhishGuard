# Phase 6: Audit Logging & Final Polish - Plan

## Goal
Implement system-wide audit logging and finalize the project documentation.

## Proposed Changes

### Audit Logging
#### [MODIFY] app/routers/auth.py
- Import `logging`. Configure logger.
- Add logs for user creation and token generation.

#### [MODIFY] app/routers/analysis.py
- Import `logging`.
- Add logs for incoming analysis requests from users.
- Log `ERROR` when gRPC connection fails.

#### [MODIFY] analysis/server.py
- Import `logging`.
- Log server startup.
- Log when `AnalyzeEmail` is invoked and what score is returned.

### Documentation
#### [MODIFY] README.md
- Replace placeholder text with full project documentation.
- Architecture diagram (text/mermaid).
- Startup commands.

## Verification Plan
- Boot the system.
- Perform actions in the browser UI.
- Check both terminals to ensure logs are actively printing.
- Review `README.md` rendering in IDE.
