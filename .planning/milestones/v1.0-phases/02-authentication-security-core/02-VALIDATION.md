# Phase 2: Authentication & Security Core - Validation Strategy

## Dimensions

1. **Password Hashing**: Verify that user passwords are NOT stored in plain text inside `phishguard.db`.
2. **Registration Endpoint**: Verify that a new user can be created via `/auth/register` and duplicate usernames are handled gracefully.
3. **Token Generation**: Verify that valid credentials submitted to `/auth/token` return a valid JWT.
4. **Endpoint Protection**: Verify that accessing the protected `/auth/me` endpoint without a valid token returns `401 Unauthorized`.

## Release Criteria

- [ ] Inspecting `phishguard.db` shows `$2b$` style hashes in the `hashed_password` column.
- [ ] `POST /auth/register` with `{"username": "test", "password": "password123"}` returns `201 Created` or `200 OK`.
- [ ] `POST /auth/token` with the same credentials returns `{"access_token": "eyJ...", "token_type": "bearer"}`.
- [ ] `GET /auth/me` with the access token succeeds and returns the user object (without the password hash).
