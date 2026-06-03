# Secure Password Hashing (bcrypt) Feature

## Overview

Replace insecure MD5 password hashing with bcrypt-based password hashing to improve authentication security and align with modern security practices.

## Purpose

Protect user credentials against rainbow table attacks, brute-force attacks, and database compromise scenarios.

---

## Functional Requirements

### FR-BCRYPT-1

The system SHALL hash all newly created passwords using bcrypt.

### FR-BCRYPT-2

The system SHALL never store plaintext passwords.

### FR-BCRYPT-3

The system SHALL use bcrypt's automatic per-password salt generation.

### FR-BCRYPT-4

The system SHALL verify passwords using bcrypt verification APIs during authentication.

### FR-BCRYPT-5

Legacy MD5 hashes SHALL be considered unsupported and migrated or reset.

### FR-BCRYPT-6

The `hash_password()` function in `security.py` SHALL be replaced with a `hash_password()` / `verify_password()` pair so that callers do not re-implement comparison logic.

### FR-BCRYPT-7

The login flow SHALL call `verify_password(plain, stored_hash)` instead of hashing the input and comparing strings directly, because bcrypt hashes are non-deterministic across calls.

### FR-BCRYPT-8

The signup flow SHALL store only the bcrypt hash returned by `hash_password()`. No intermediate MD5 value SHALL be computed or stored.

---

## Non-Functional Requirements

### NFR-BCRYPT-1

Password hashes SHALL include embedded salt and cost-factor metadata (bcrypt `$2b$` format).

### NFR-BCRYPT-2

Password verification SHALL use bcrypt's secure constant-time comparison mechanisms to prevent timing attacks.

### NFR-BCRYPT-3

The hashing implementation SHALL be centralized in `backend/app/core/security.py`. No other file SHALL import `hashlib` or any hashing primitive directly.

### NFR-BCRYPT-4

The bcrypt work factor (rounds) SHALL be a minimum of 12 to provide adequate resistance to brute-force attacks on modern hardware.

---

## Affected Files

* `backend/app/core/security.py` — replace `hash_password()` with bcrypt; add `verify_password()`
* `backend/app/services/auth_service.py` — update login to call `verify_password()` instead of comparing hashed strings; update signup to call new `hash_password()`
* `backend/pyproject.toml` — add `bcrypt` dependency
* `backend/app/api/routes/auth.py` — no query changes required; affected indirectly through service layer
* `backend/app/db/session.py` — no changes required

---

## Success Paths

### SP-BCRYPT-01: New User Registration

User submits valid signup form → `hash_password()` produces a bcrypt hash → hash is stored in the `users` table → user is redirected to `/login`.

### SP-BCRYPT-02: Login with bcrypt-Hashed Password

User submits valid credentials → `verify_password(plain, stored_hash)` returns `True` → session is established → user is redirected to `/welcome`.

### SP-BCRYPT-03: Incorrect Password Rejected

User submits wrong password → `verify_password()` returns `False` → 401 response returned → no session created.

### SP-BCRYPT-04: Two Identical Passwords Produce Different Hashes

Two separate registrations with the same password → bcrypt generates a unique salt each time → the stored hashes differ → both accounts authenticate correctly with that password.

---

## Edge Cases

### EC-BCRYPT-01: Legacy MD5 Hash in Database

A user account whose password column contains an MD5 hash attempts to log in. `verify_password()` will return `False` because the stored value is not a valid bcrypt hash. The user must reset their password. The system SHALL return the standard invalid-credentials 401 response and SHALL NOT crash.

### EC-BCRYPT-02: Empty Password Submission

A login or signup request arrives with a blank password field. The existing null-check guard in `auth_service.py` fires before `hash_password()` or `verify_password()` is called → appropriate error response returned, no hashing attempted.

### EC-BCRYPT-03: Very Long Password Input

bcrypt truncates input at 72 bytes. Passwords longer than 72 bytes SHALL still produce a valid hash and authenticate correctly for the truncated portion. This is a known bcrypt limitation and is acceptable for this application's scope.

### EC-BCRYPT-04: Database Contains Corrupted Hash

The stored hash value is malformed (not a valid bcrypt string). `verify_password()` SHALL catch the resulting exception and return `False`, producing a standard 401 response without exposing internal error details.

### EC-BCRYPT-05: Concurrent Registrations with Same Username

Two simultaneous signup requests for the same username → the `UNIQUE` constraint on the `users` table rejects the second insert → the existing duplicate-username error response is returned. bcrypt does not affect this path.

---

## Acceptance Criteria

### AC-BCRYPT-01

Given a new registration, when the record is written to the database, then the `password` column SHALL contain a string beginning with `$2b$` and SHALL NOT contain the original plaintext or its MD5 equivalent.

### AC-BCRYPT-02

Given valid credentials matching a bcrypt-hashed record, when the login form is submitted, then the session SHALL be established and the user SHALL be redirected to `/welcome`.

### AC-BCRYPT-03

Given an incorrect password, when the login form is submitted, then a 401 response SHALL be returned and no session SHALL be created.

### AC-BCRYPT-04

Given an account whose stored hash is an MD5 value, when the user attempts to log in with the correct original password, then a 401 response SHALL be returned (not a crash or unhandled exception).

### AC-BCRYPT-05

Given two accounts registered with the same password, when their stored hashes are compared directly, then the hashes SHALL differ from each other (salt uniqueness).

### AC-BCRYPT-06

Given a blank password field on the login form, when the form is submitted, then a 401 response SHALL be returned before any hashing or database query is executed.

---

## Test Cases

| ID | Scenario | Input | Expected Result |
|----|----------|-------|-----------------|
| TC-BCRYPT-01 | Register new account | Valid username, email, password | Hash stored starts with `$2b$`; redirect to `/login` |
| TC-BCRYPT-02 | Login with correct password | Credentials matching bcrypt record | Session created; redirect to `/welcome` |
| TC-BCRYPT-03 | Login with wrong password | Correct username, wrong password | 401 returned; no session |
| TC-BCRYPT-04 | Login with MD5 legacy hash in DB | Correct original password, MD5-stored account | 401 returned; no crash |
| TC-BCRYPT-05 | Same password registered twice | Two accounts, identical passwords | Stored hashes are different strings |
| TC-BCRYPT-06 | Empty password on login | Username provided, password blank | 401 returned before hashing |
| TC-BCRYPT-07 | Empty password on signup | Username and email provided, password blank | Error response; no record created |
| TC-BCRYPT-08 | Password not stored in plaintext | Any registration | Database row contains no plaintext or MD5 value |
| TC-BCRYPT-09 | Corrupted hash in database | Manually set password column to garbage string | 401 returned; no unhandled exception |
| TC-BCRYPT-10 | Logout and re-login | User logs out, logs back in with correct password | Session re-established successfully |
