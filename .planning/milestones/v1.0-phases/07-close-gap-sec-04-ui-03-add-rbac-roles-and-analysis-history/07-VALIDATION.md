# Phase 7: Close Gaps (SEC-04 & UI-03) - Validation Strategy

## Dimensions

1. **RBAC Protection**: Verify that a normal user cannot access an admin-only endpoint.
2. **Data Persistence**: Verify that after analyzing an email, the result is saved to SQLite.
3. **UI Rendering**: Verify that the history table in the dashboard correctly displays past analyses, using the matching dark cyber aesthetics.

## Release Criteria

- [ ] `User` table contains a `role` attribute.
- [ ] Attempting to access an admin route as an `analyst` returns HTTP 403.
- [ ] `GET /analysis/history` returns a JSON array of past records for the authenticated user.
- [ ] The `dashboard.html` interface displays a "Recent Analyses" table that populates correctly on page load and updates after a new analysis is run.
