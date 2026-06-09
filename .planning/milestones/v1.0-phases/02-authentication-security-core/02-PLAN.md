# Phase 2: Authentication & Security Core - Plan

## Goal
Implement a robust security layer utilizing Bcrypt for password hashing and JWT for API authentication, fulfilling the strict cybersecurity constraints.

## Proposed Changes

### Dependencies
#### [MODIFY] requirements.txt
- Add `passlib[bcrypt]`, `python-jose[cryptography]`.

### Database & Models
#### [NEW] app/models.py
- Create the SQLAlchemy `User` model with `id`, `username`, `hashed_password`, and `is_active`.
#### [NEW] app/schemas.py
- Create Pydantic models: `UserBase`, `UserCreate`, `UserResponse`, and `Token`.

### Security Core
#### [NEW] app/security.py
- Implement password hashing and verification using `passlib.context.CryptContext`.
- Implement JWT token generation using `jose.jwt` (with a dummy dev secret key).
- Provide `get_current_user` dependency for FastAPI protected routes.

### API Routing
#### [NEW] app/routers/auth.py
- Define `APIRouter` for `/auth`.
- Implement `/register` to hash passwords and save users.
- Implement `/token` endpoint compatible with `OAuth2PasswordRequestForm`.
- Implement `/me` endpoint to test JWT validation.

#### [MODIFY] app/main.py
- Include the `auth` router.
- Call `models.Base.metadata.create_all(bind=engine)` on startup to provision the `User` table.

## Verification Plan

### Manual Verification
- Restart the FastAPI gateway.
- Use Swagger UI (`http://localhost:8000/docs`) to test the registration endpoint.
- Use Swagger UI's "Authorize" button to test token retrieval.
- Call the `/me` endpoint with the authenticated session to ensure the JWT works.
