# Secure Password Hashing (bcrypt) Implementation Plan

## Phase 1: Dependency Setup

1. Add `bcrypt>=4.0.0` to `dependencies` in `backend/pyproject.toml`.
2. Run `uv sync` (or `pip install bcrypt`) to install the package.
3. Confirm `import bcrypt` resolves without error before proceeding.

---

## Phase 2: Update `security.py`

1. Remove the `hashlib` import and the existing `hash_password()` function entirely.
2. Add `import bcrypt`.
3. Implement a new `hash_password()` that uses bcrypt with a minimum work factor of 12:
   ```python
   def hash_password(password: str) -> str:
       return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()
   ```
4. Add a `verify_password()` function for use during login:
   ```python
   def verify_password(plain: str, hashed: str) -> bool:
       try:
           return bcrypt.checkpw(plain.encode(), hashed.encode())
       except Exception:
           return False
   ```
5. The `try/except` in `verify_password()` guards against malformed hash strings (e.g., legacy MD5 values) without raising unhandled exceptions.

---

## Phase 3: Update `auth_service.py`

1. Add `verify_password` to the import from `app.core.security`.
2. In `signup()`: the call to `hash_password(str(password))` remains — no change needed beyond the updated implementation in Phase 2.
3. In `login()`:
   - Remove the line that computes `hashed = hash_password(str(password))`.
   - Change the SQL query to fetch the user by username only (password comparison moves to Python):
     ```python
     query = "SELECT * FROM users WHERE username = ?"
     user = conn.execute(query, (username,)).fetchone()
     ```
   - After the fetch, add the bcrypt check:
     ```python
     if user and verify_password(str(password), user['password']):
         # establish session
     else:
         return JSONResponse({'error': 'Invalid credentials.'}, status_code=401)
     ```
   - This also eliminates the SQL injection vulnerability in the login query as a side effect.

---

## Phase 4: Database Migration

1. Existing accounts have MD5-hashed passwords. These hashes are incompatible with bcrypt verification.
2. Reset the database before testing: delete `vulnerable_app.db` and restart the application so `init_db()` recreates it.
3. Re-register all test accounts so their passwords are stored as bcrypt hashes.
4. Document in code comments that accounts created before this change require a password reset.

---

## Phase 5: Verification

### Registration Tests

* Register a new account → open `vulnerable_app.db` → confirm the `password` column value starts with `$2b$`.
* Confirm the plaintext password and its MD5 value are absent from the stored hash.
* Register two accounts with the same password → confirm the two stored hashes differ.

### Login Tests

* Log in with the correct password → confirm redirect to `/welcome` and session established.
* Log in with an incorrect password → confirm 401 returned and no session created.
* Manually set a row's password to an MD5 string → attempt login → confirm 401 returned without a crash.

### Regression Tests

* Full signup → login → dashboard → logout flow completes without error.
* Duplicate username registration still returns the existing error response.
* Empty username or password on login still returns 401 before any hashing occurs.

---

## Completion Criteria

* `security.py` exports `hash_password()` and `verify_password()` using bcrypt; `hashlib` is removed.
* All new password records in the database begin with `$2b$`.
* Login with a correct bcrypt-hashed password succeeds.
* Login with a wrong password or a legacy MD5-hashed record returns 401 without crashing.
* All regression tests pass.
* `bcrypt` added to `pyproject.toml` dependencies.
