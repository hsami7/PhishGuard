# Phase 7: Close Gaps (SEC-04 & UI-03) - Plan

## Proposed Changes

### Backend Models & Schemas
#### [MODIFY] app/models.py
- Add `role` column to `User`.
- Create `AnalysisHistory` class (id, user_id, sender, subject, score_level, numeric_score).

#### [MODIFY] app/schemas.py
- Update `UserCreate` and `UserResponse` with `role: str = "analyst"`.
- Create `HistoryResponse` schema.

### Backend Routing & Security
#### [MODIFY] app/main.py
- Add drop/create table logic to startup event to reset SQLite schema.
- Add a dummy `GET /admin/stats` route protected by `get_current_admin_user`.

#### [MODIFY] app/security.py
- Create `get_current_admin_user(current_user: User = Depends(get_current_user))`.

#### [MODIFY] app/routers/auth.py
- Map `role` from incoming payload to DB model during registration.

#### [MODIFY] app/routers/analysis.py
- In `analyze_email`, instantiate an `AnalysisHistory` record and commit it to `db`.
- Add `GET /history` route to fetch records for `current_user`.

### Frontend
#### [MODIFY] templates/dashboard.html
- Add HTML markup for a Tailwind table below the main cards.
- Add Javascript `fetch('/analysis/history')` on DOMContentLoaded.
- Update the table DOM dynamically. Call the fetch function again after a successful new analysis.
