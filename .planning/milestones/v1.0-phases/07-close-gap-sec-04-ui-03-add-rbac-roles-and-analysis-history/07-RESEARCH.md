# Phase 7: Close Gaps (SEC-04 & UI-03) - Research

## Technical Approach

### 1. SEC-04: Role-Based Access Control (Admin vs Analyst)
- **Database Model**: Add a `role` column to the `User` model in `app/models.py`. Default to `"analyst"`.
- **Schemas**: Update Pydantic schemas in `app/schemas.py` to support role input and output.
- **Security Logic**: Implement a new FastAPI dependency `get_current_admin_user` in `app/security.py` that wraps `get_current_user` and raises an `HTTP 403 Forbidden` if the `role != "admin"`.
- **Proof of Concept**: We will create a protected route (`GET /admin/stats` in `app/main.py`) to verify that standard analysts cannot access admin features.

### 2. UI-03: Email Analysis History
- **Database Model**: Create a new `AnalysisHistory` table in `app/models.py` with a foreign key to the `User` table. It will store `sender`, `subject`, `score_level`, and `numeric_score`.
- **Service Logic**: Modify `POST /analysis/` in `app/routers/analysis.py` to insert a new `AnalysisHistory` record into SQLite immediately after receiving the gRPC calculation.
- **API Endpoint**: Create a new `GET /analysis/history` endpoint to return a user's past records.
- **Frontend Integration**: Update `templates/dashboard.html` to include a new section below the analysis form. We will write Vanilla JS to fetch the history on page load and render it dynamically into a Tailwind-styled dark-mode table.

### Schema Migration Note
Since we are using raw SQLite without Alembic migrations for this prototype, we will alter `app/main.py` to drop and recreate the tables upon server startup to ensure the schema updates apply cleanly.
