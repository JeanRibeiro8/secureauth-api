 <div align="center">

# SecureAuth API

### Secure User Authentication & Account Management REST API

A REST API built with Python and FastAPI, featuring secure user authentication, JWT access tokens, Argon2id password hashing, and PostgreSQL persistence.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

</div>


---

## 📸 Preview

<div align="center">

### Dashboard Preview

![DevInsight Preview](./public/secureauthapi.png)

</div>

> **Live Demo:** [https://secureauth-api-kttl.onrender.com/docs]
> **Repository:** [https://github.com/JeanRibeiro8/secureauth-api]

---

## 📌 About the Project

**SecureAuth API** is a backend project focused on implementing secure authentication and account-management functionality through a RESTful API.

Built with **Python 3.12+**, **FastAPI**, and **PostgreSQL**, the application provides user registration, credential verification, JWT-based authentication, protected endpoints, and profile management.

The project emphasizes security practices such as Argon2id password hashing, token validation, environment-based configuration, and automated testing.

### Key Features

- User registration and authentication.
- Secure password hashing using Argon2id.
- JWT access token generation and validation.
- Protected routes using HTTP Bearer authentication.
- Authenticated user profile retrieval and updates.
- Password changes with automatic invalidation of previously issued access tokens.
- Duplicate email prevention.
- PostgreSQL persistence and Alembic migrations.
- Automated API tests with pytest and HTTPX.
- Interactive API documentation with Swagger UI.

## ✨ Features

### Authentication & Security

- Register users with name, email, and password.
- Authenticate users using email and password.
- Hash passwords with Argon2id — plaintext passwords are never stored.
- Generate signed and expiring JWT access tokens.
- Validate token signature, expiration, type, subject, and version.
- Invalidate previously issued access tokens after password changes.
- Keep password hashes out of API responses.
- Avoid exposing submitted values in validation error responses.

### Account Management

- Retrieve the authenticated user's profile.
- Update account name and email.
- Change the authenticated user's password.
- Prevent duplicate email addresses.
- Use the authenticated identity instead of accepting another user's ID.

### API & Database

- RESTful endpoints with structured request and response schemas.
- PostgreSQL database integration.
- SQLAlchemy ORM for database operations.
- Alembic for database schema migrations.
- Pydantic v2 for data validation.
- Automated tests using an isolated in-memory SQLite database.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12+ | Core programming language |
| FastAPI | REST API framework |
| Pydantic v2 | Request validation and response schemas |
| SQLAlchemy 2 | ORM and database access |
| PostgreSQL | Relational database |
| Psycopg 3 | PostgreSQL driver |
| Alembic | Database migrations |
| PyJWT | JWT creation and validation |
| Argon2-cffi | Password hashing |
| Pytest | Automated testing |
| HTTPX | API testing client |

## 🏗️ Architecture

The application follows a layered architecture, separating HTTP handling, business logic, data access, and database persistence.

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

### Request Flow

1. API routes receive HTTP requests.
2. Pydantic schemas validate incoming data and structure responses.
3. Services handle authentication and account-management rules.
4. Repositories perform database queries through SQLAlchemy.
5. PostgreSQL stores user records and password hashes.

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new account |
| `POST` | `/auth/login` | Authenticate and receive an access token |

### Authenticated User

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/users/me` | Retrieve the authenticated user's profile |
| `PATCH` | `/users/me` | Update the user's name and/or email |
| `PATCH` | `/users/me/password` | Change the user's password |

### Health & Documentation

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Basic API information |
| `GET` | `/health` | Check API and database connectivity |
| `GET` | `/docs` | Interactive Swagger documentation |
| `GET` | `/redoc` | ReDoc documentation |

**Token expiration:** Access tokens expire after 30 minutes by default. Refresh-token functionality is not included in this version.

## 🔐 Security Implementation

Security is a central part of this project.

- **Argon2id:** Passwords are securely hashed before database storage.
- **JWT:** Access tokens are signed using HS256.
- **Token validation:** Signature, expiration, token type, subject, and token version are checked.
- **Protected routes:** Authenticated endpoints require a Bearer token.
- **Token invalidation:** Password changes increment an internal token-version counter.
- **Data protection:** Password hashes are excluded from API response schemas.
- **Environment variables:** Database credentials and JWT secrets are stored outside the source code.

> This project is a learning and portfolio implementation. A production deployment should additionally consider rate limiting, monitoring, operational secret management, backup policies, HTTPS, and account-recovery workflows.

## 🚀 Getting Started

### Requirements

- Python 3.12 or newer
- PostgreSQL 14 or newer
- Git

### Installation

**Clone the repository**

```bash
git clone https://github.com/JeanRibeiro8/secureauth-api
cd secureauth-api
```

**Create and activate a virtual environment**

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

**Install dependencies**

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Database Configuration

Create a PostgreSQL user and database:

```sql
CREATE USER secureauth_user WITH LOGIN PASSWORD 'your_private_password';
CREATE DATABASE secureauth_db OWNER secureauth_user;
```

### Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Generate a secure JWT secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Configure your `.env` file:

```dotenv
DATABASE_URL=postgresql+psycopg://secureauth_user:your_password@localhost:5432/secureauth_db
JWT_SECRET_KEY=your_generated_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=SecureAuth API
ENVIRONMENT=development
```

Use your own database credentials and generated secret. Never commit your `.env` file.

### Run Database Migrations

```bash
alembic upgrade head
```

### Start the Development Server

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

## 🔄 Example Usage

### Register a User

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada Lovelace","email":"ada@example.com","password":"Strong-Password-123!"}'
```

### Authenticate

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ada@example.com","password":"Strong-Password-123!"}'
```

Use the returned `access_token` to access protected endpoints.

### Retrieve the Authenticated User

```bash
curl http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer <access_token>"
```

## 🧪 Testing

The project uses **pytest** and **HTTPX** for automated API testing.

Tests run against an isolated in-memory SQLite database, without connecting to or modifying the configured PostgreSQL database.

Run the test suite:

```bash
pytest -v
```

Test coverage includes:

- User registration and duplicate email handling.
- Invalid registration data.
- Successful and unsuccessful login.
- Missing, invalid, expired, and incorrect-type tokens.
- Profile retrieval and updates.
- Duplicate email during profile updates.
- Password changes and token invalidation.
- Safe API response fields.

## 🔮 Future Improvements

- Refresh-token rotation and revocation.
- Rate limiting and account lockout protection.
- Email verification.
- Password recovery workflows.
- Structured logging and monitoring.
- PostgreSQL integration tests.
- Continuous integration with GitHub Actions.
- Docker support.

## 📌 Project Scope

This version focuses on the foundations of secure authentication and account management.

The following are intentionally outside the current scope:

- Frontend application.
- OAuth and social login.
- Refresh-token functionality.
- Email delivery.
- Docker deployment.
- External integrations.

---

<div align="center">

### Developed by Jean Ribeiro

**Junior Full Stack Developer | Python | FastAPI | React**

[GitHub](https://github.com/JeanRibeiro8) · [LinkedIn](https://www.linkedin.com/in/jean-ribeiro-9a3792267/) · [Portfolio](https://jeanribeiro8.github.io/JeanRibeiro/)

</div>