# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Context

This is an intentionally vulnerable web application designed for security education. The application contains 8 deliberately implemented security flaws that students exploit to learn about OWASP Top 10 vulnerabilities. It is built with FastAPI and SQLite, designed to be simple enough to read in one session while demonstrating real attack techniques.

**WARNING**: This app should never be deployed to production or used on systems without explicit authorization.

---

## Development Commands

Run the application (from `backend/` directory):
```powershell
python app/main.py
```

Install/update dependencies:
```powershell
cd backend
uv sync
```

View database contents:
```powershell
python -c "import sqlite3; conn = sqlite3.connect('vulnerable_app.db'); [print(r) for r in conn.execute('SELECT * FROM users').fetchall()]; conn.close()"
```

---

## Architecture Overview

The application follows a simple three-layer architecture:

### Request Flow
1. **FastAPI App** (`main.py`) - Entry point that configures middleware, static files, and routes
2. **HTTP Routes** (`api/routes/auth.py`) - All route handlers that receive requests and return responses
3. **Business Logic** (`services/auth_service.py`) - Core authentication logic with vulnerable SQL queries
4. **Database Layer** (`db/session.py`) - SQLite connection and schema management

### Key Architectural Pattern

The vulnerability pattern is consistent across the codebase: user input flows directly into SQL query construction via string concatenation, without parameterization or sanitization.

**Critical Vulnerability Chain:**
- `auth.py` receives form data via FastAPI `Form()` parameters
- `auth_service.py` builds SQL queries using `+` string concatenation
- `session.py` executes raw SQL without prepared statements
- `security.py` uses `hashlib.md5()` without salt

### Session Management

Session state is managed by Starlette's `SessionMiddleware` with a hardcoded weak secret key in `main.py`. Session data (`user_id`, `username`, `email`) is stored server-side and accessed via `request.session`. The `/welcome` endpoint checks for `'user_id'` in session before granting access.

### Database Schema

Single `users` table: `id` (auto-increment), `username` (unique), `email`, `password` (MD5 hash). Database file (`vulnerable_app.db`) lives in project root.

---

## Intentional Vulnerabilities Map

| # | Vulnerability | Location | Root Cause |
|---|---|---|---|
| 1 | SQL Injection | `auth_service.py:login()` | String concatenation in query: `"WHERE username = '" + username + "'"` |
| 2 | Stored XSS | `signup.html` → dashboard | Username saved to database unescaped, reflected in `welcome_page()` |
| 3 | Reflected XSS | `auth.py:search_user()` | Query parameter `q` directly interpolated into HTML response |
| 4 | Session Hijacking | `main.py:25` | Hardcoded `SECRET_KEY = "super-secret-key-12345"` |
| 5 | Weak Password Storage | `security.py:13` | `hashlib.md5()` without salt |
| 6 | Exposed Database | `auth.py:download_db()` | No authentication check on `/download/db` endpoint |
| 7 | No Rate Limiting | All endpoints | No middleware configured for request throttling |
| 8 | CSRF | All forms | No CSRF token validation on any POST endpoint |

---

## Frontend-Backend Integration

FastAPI serves static files via `StaticFiles` mounts:
- `/static/css` → `frontend/static/css/`
- `/static/images` → `frontend/static/images/`

Templates are rendered as `FileResponse` from `frontend/templates/` with client-side JavaScript performing form submissions. The dashboard (`welcome.html`) uses `{{username}}` placeholder that gets replaced server-side in `auth.py:welcome_page()`.

---

## Security Education Context

When working with this codebase, remember:
- Vulnerabilities are intentional, not bugs to be "fixed" unless explicitly asked
- The project includes `docs/EXPLOITS.md` with step-by-step exploitation guides
- This is for ethical security education only
- University branding (logos in frontend) supports its use in academic settings

If asked to demonstrate or fix vulnerabilities, prioritize educational clarity over comprehensive hardening. The goal is understanding the vulnerability concept, not production-ready security.

# Specification Hierarchy

When implementing features:

1. Read PRD.md for product requirements.
2. Read TDD.md for technical design constraints.
3. Read Spec.md for detailed implementation specifications.
4. Read feature specifications in `.Codex/Specs/`.
5. Follow the associated `*-plan.md` file.
6. Keep implementation aligned with the feature specification.

Feature files take precedence over implementation assumptions.