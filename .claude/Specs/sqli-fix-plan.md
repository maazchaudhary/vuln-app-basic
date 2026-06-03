# SQL Injection Mitigation Implementation Plan

## Phase 1: Fix Login Query (`auth_service.py`)

1. Locate the string-concatenated `SELECT` query in `login()`.
2. Replace it with a parameterized query using `?` placeholders:
   ```python
   query = "SELECT * FROM users WHERE username = ? AND password = ?"
   user = conn.execute(query, (username, hashed)).fetchone()
   ```
3. Remove the concatenation variables — `username` and `hashed` are passed as a tuple, not embedded in the string.

---

## Phase 2: Fix Signup Query (`auth_service.py`)

1. Locate the string-concatenated `INSERT` query in `signup()`.
2. Replace it with a parameterized query:
   ```python
   query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
   conn.execute(query, (username, email, hashed))
   ```
3. Confirm the `UNIQUE` constraint exception path still fires correctly for duplicate usernames — parameterized queries do not affect constraint enforcement.

---

## Phase 3: Fix Search Query (`auth.py`)

1. Locate the string-concatenated `LIKE` query in `search_user()`.
2. Replace it with a parameterized query using `LIKE` with a bound wildcard pattern:
   ```python
   pattern = f"%{q}%"
   query = "SELECT username, email FROM users WHERE username LIKE ? OR email LIKE ?"
   results = conn.execute(query, (pattern, pattern)).fetchall()
   ```
3. The HTML rendering of `q` in the heading (`<h2>Search Results for: {q}</h2>`) is a separate Reflected XSS issue and is out of scope for this feature — do not fix it here.

---

## Phase 4: Verification

### Injection Attempt Tests

* Attempt login bypass with `admin' OR '1'='1' --` → confirm 401 is returned.
* Attempt `' UNION SELECT username, password FROM users --` via `/search` → confirm no password data is returned.
* Attempt `'); DROP TABLE users; --` as signup username → confirm `users` table still exists afterward.

### Regression Tests

* Register a new account with normal credentials → confirm redirect to `/login`.
* Log in with valid credentials → confirm session established and `/welcome` loads.
* Search with a plain alphanumeric query → confirm matching results return.
* Attempt login with wrong password → confirm 401 still returned.
* Attempt duplicate username registration → confirm error message still returned.

### Edge Case Tests

* Register and log in with a username containing a single quote (e.g., `O'Brien`) → confirm it works without error.
* Submit an empty search (`/search` with no `q` parameter) → confirm the existing error response is returned.

---

## Completion Criteria

* All three vulnerable query sites replaced with parameterized equivalents.
* No `+`, f-string interpolation, `.format()`, or `%` formatting used to construct SQL with user data.
* All regression tests pass.
* All injection attempt tests return the expected non-bypass responses.
* No new dependencies introduced.
