# SecureAuth API

A secure user authentication and account-management REST API built with **Python 3.12+** and **FastAPI**. The project demonstrates user registration, password hashing with Argon2id, JWT access tokens, protected routes, PostgreSQL persistence, database migrations, and automated API tests.

## Features

- Register users with name, email, and password.
- Authenticate users with email and password.
- Hash passwords with Argon2id; plaintext passwords are never stored.
- Issue signed, expiring JWT access tokens.
- Validate token signature, expiration, token type, subject, and token version.
- Protect endpoints with HTTP Bearer authentication.
- Retrieve and update the authenticated user's own profile.
- Change the authenticated user's password.
- Invalidate previously issued access tokens after a password change using an internal token-version counter.
- Prevent duplicate email addresses.
- Keep password hashes out of API response schemas.
- Avoid echoing submitted values in validation error responses.
- Manage PostgreSQL schema changes with Alembic.
- Run endpoint tests using pytest, HTTPX, and an isolated in-memory SQLite database.
- Explore the API through generated OpenAPI documentation at `/docs`.

## Technology stack

| Technology | Purpose |
| --- | --- |
| Python 3.12+ | Application language |
| FastAPI | REST API framework |
| Pydantic v2 | Request validation and response schemas |
| SQLAlchemy 2 | ORM and database access |
| PostgreSQL | Relational database |
| Psycopg 3 | PostgreSQL driver |
| Alembic | Database migrations |
| PyJWT | JWT creation and validation |
| argon2-cffi (Argon2id) | Password hashing |
| pytest | Automated tests |
| HTTPX | HTTP client for API tests |

## Architecture

The application separates HTTP handling, business rules, data access, and persistence.

```text
secureauth-api/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── database.py
│   │   └── models/
│   │       └── user.py
│   ├── schemas/
│   │   └── user.py
│   ├── repositories/
│   │   └── user_repository.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── exceptions.py
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── auth.py
│   │       └── users.py
│   └── main.py
├── migrations/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py
│   ├── helpers.py
│   ├── test_auth.py
│   └── test_users.py
├── .env.example
├── .gitignore
├── alembic.ini
└── requirements.txt
```

### Request flow

1. A route receives and validates an HTTP request.
2. Pydantic schemas validate the request or shape the response.
3. Services apply authentication and account-management rules.
4. Repositories perform user queries through SQLAlchemy.
5. PostgreSQL persists user records and password hashes.

## API endpoints

### Authentication

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | Register a new account | `201 Created` |
| `POST` | `/auth/login` | Verify credentials and issue an access token | `200 OK` |

### Authenticated user

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| `GET` | `/users/me` | Retrieve the authenticated user's profile | `200 OK` |
| `PATCH` | `/users/me` | Update the authenticated user's name and/or email | `200 OK` |
| `PATCH` | `/users/me/password` | Change the authenticated user's password | `204 No Content` |

### Health and documentation

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Basic API information |
| `GET` | `/health` | Check API and database connectivity |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/redoc` | ReDoc documentation |

A refresh-token endpoint is intentionally not included in this first version. The API issues short-lived access tokens (30 minutes by default).

## User data model

The `users` table contains:

| Column | Description |
| --- | --- |
| `id` | Integer primary key |
| `name` | Display name (1–100 characters) |
| `email` | Unique email address |
| `hashed_password` | Argon2id password hash; never returned by the API |
| `is_active` | Account active flag |
| `token_version` | Internal counter used to invalidate older access tokens after password changes |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |

## Security decisions

- Passwords are hashed with Argon2id via `argon2-cffi`; plaintext passwords are not persisted.
- JWTs are signed with HS256 using a secret supplied through the environment.
- Access tokens include `sub`, `iat`, `exp`, `type`, and `ver` claims. The API checks the signature, expiration, token type, subject, and current token version.
- Protected routes require an HTTP `Authorization: Bearer <token>` header.
- `/users/me` uses the authenticated identity from the token; callers cannot supply another user's ID to access these operations.
- Login returns the same public error for an unknown email and an incorrect password.
- Password hashes are excluded from response schemas.
- Validation responses omit submitted input values, which prevents password values from being echoed in error details.
- Changing a password increments `token_version`, invalidating access tokens issued before the change.
- JWT secrets and database credentials are kept in `.env`, which is excluded from Git.
- Production deployments must use HTTPS and a strong, unique JWT secret.

This project is a learning and portfolio implementation. A production deployment should additionally consider rate limiting on authentication endpoints, monitoring, operational secret management, backup policies, and a formal account-recovery flow.

## Requirements

- Python 3.12 or newer
- PostgreSQL 14 or newer
- Git

## Local setup

### 1. Clone the repository and enter the project

```bash
git clone <your-repository-url>
cd secureauth-api
```

### 2. Create and activate a virtual environment

Linux / macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Create a PostgreSQL role and database

Connect to PostgreSQL as an administrator and run the following SQL. Replace the example password with a strong, private value.

```sql
CREATE USER secureauth_user WITH LOGIN PASSWORD 'replace_with_a_private_password';
CREATE DATABASE secureauth_db OWNER secureauth_user;
```

### 5. Configure environment variables

Copy the example file:

```bash
cp .env.example .env
```

Generate a JWT secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Put the generated value in `JWT_SECRET_KEY` in `.env`. Update `DATABASE_URL` with the PostgreSQL username, password, host, port, and database name.

Example format (use your own credentials and secret):

```dotenv
DATABASE_URL=postgresql+psycopg://secureauth_user:your_password@localhost:5432/secureauth_db
JWT_SECRET_KEY=paste_your_generated_secret_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=SecureAuth API
ENVIRONMENT=development
```

If your database password contains reserved URL characters such as `@`, `:`, `/`, `#`, or `%`, URL-encode the password portion of the connection URL. Never commit `.env` or share its contents.

### 6. Apply database migrations

```bash
alembic upgrade head
```

### 7. Run the API

```bash
python -m uvicorn app.main:app --reload
```

Open:

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

Keep the terminal running while using the API. Press `Ctrl+C` to stop the development server.

## Example requests

### Register

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada Lovelace","email":"ada@example.com","password":"Strong-Password-123!"}'
```

The response contains the public user profile only. It never contains the password or password hash.

### Login

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ada@example.com","password":"Strong-Password-123!"}'
```

Copy the returned `access_token` and use it as a Bearer token in requests to protected endpoints.

### Get the current profile

```bash
curl http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer <access_token>"
```

### Update the current profile

```bash
curl -X PATCH http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada Byron"}'
```

### Change password

```bash
curl -X PATCH http://127.0.0.1:8000/users/me/password \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"current_password":"Strong-Password-123!","new_password":"Another-Strong-456!"}'
```

A successful password change returns `204 No Content` and invalidates older access tokens for that account.

## Automated tests

The test suite uses an isolated in-memory SQLite database. It does not connect to or modify the configured PostgreSQL database.

```bash
pytest -v
```

Coverage includes registration, duplicate email, invalid input, login success/failure, missing/invalid/expired/wrong-type tokens, profile retrieval and update, duplicate email on profile update, password change, token invalidation, and safe response fields.

## Future improvements

- Add refresh-token rotation and revocation.
- Add rate limiting and account lockout controls for authentication endpoints.
- Add email verification and password-reset workflows.
- Add structured logging and monitoring.
- Add database-backed integration tests against a temporary PostgreSQL instance.
- Add CI for linting, type checking, and automated tests.

## Scope

This version intentionally excludes a frontend, OAuth/social login, refresh tokens, Docker, email delivery, and external integrations. The focus is a clear, testable foundation for understanding secure authentication in a Python REST API.
# secureauth-api
