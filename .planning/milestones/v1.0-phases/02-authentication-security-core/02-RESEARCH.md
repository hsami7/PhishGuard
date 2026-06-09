# Phase 2: Authentication & Security Core - Research

## Technical Approach

**Authentication Mechanism**:
- We will implement JWT (JSON Web Tokens) for secure, stateless authentication.
- The `python-jose` library will handle JWT encoding and decoding.
- We will configure an OAuth2 flow (password bearer) using FastAPI's built-in `OAuth2PasswordBearer` so that tools like Swagger UI can automatically authenticate.

**Password Security**:
- Storing passwords in plain text is strictly forbidden by the project requirements.
- We will use `passlib` with `bcrypt` to hash passwords before storing them in the SQLite database.

**Database Schema**:
- A `User` SQLAlchemy model will be created with `id`, `username`, `hashed_password`, and `is_active` fields.
- Pydantic models (schemas) will strictly validate incoming requests (`UserCreate`) and outgoing responses (`UserResponse`) to ensure we never leak `hashed_password`.

**Endpoints**:
- `POST /auth/register`: Create a new user account.
- `POST /auth/token`: Authenticate with username/password and return a JWT token.
- `GET /auth/me`: A protected test endpoint to verify the token logic is working.

## Risks
- JWT secret management: For development, we'll hardcode a secure random string or load it from the environment, but in production, this needs strict secret management.
- SQLite concurrent writes: Authentication creates users. We must ensure SQLite locks do not become a bottleneck during testing, though `check_same_thread=False` handles basic dev setups.
