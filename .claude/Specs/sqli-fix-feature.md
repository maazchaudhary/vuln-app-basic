# SQL Injection Mitigation Feature

## Overview

Replace all raw string-concatenated SQL queries with parameterized queries to eliminate SQL injection vulnerabilities across the authentication and search subsystems.

## Purpose

Prevent attackers from injecting malicious SQL into user-controlled input fields, which currently allows complete authentication bypass, unauthorized data access, and potential database manipulation.

---

## Functional Requirements

### FR-SQLI-1: Parameterized Login Query

The system SHALL use a parameterized query for credential lookup during login. No user-supplied value SHALL be interpolated directly into a SQL string.

### FR-SQLI-2: Parameterized Signup Query

The system SHALL use a parameterized query for the `INSERT` statement during user registration. Username, email, and hashed password SHALL all be passed as bound parameters.

### FR-SQLI-3: Parameterized Search Query

The system SHALL use a parameterized `LIKE` query for the `/search` endpoint. The `q` parameter SHALL be bound, not concatenated.

### FR-SQLI-4: No Dynamic SQL Construction

The system SHALL NOT construct SQL strings using `+`, f-strings, `.format()`, or `%` interpolation anywhere user-supplied data is involved.

### FR-SQLI-5: Existing Behavior Preserved

All valid authentication, registration, and search operations SHALL continue to function correctly after the fix. No existing success paths SHALL be broken.

### FR-SQLI-6: Error Handling Preserved

Registration failures (duplicate username, missing fields) and login failures (wrong credentials) SHALL continue to return the same user-visible error responses as before.

---

## Non-Functional Requirements

### NFR-SQLI-1

The fix SHALL be isolated to `backend/app/services/auth_service.py` and `backend/app/api/routes/auth.py`. No other files require modification.

### NFR-SQLI-2

The fix SHALL not introduce any new dependencies. Python's built-in `sqlite3` parameterized query support (`?` placeholders) is sufficient.

### NFR-SQLI-3

The fix SHALL not alter the database schema, session structure, or response formats.

---

## Affected Files

* `backend/app/services/auth_service.py` — login and signup queries
* `backend/app/api/routes/auth.py` — search query

---

## Success Paths

### SP-SQLI-01: Normal Login Still Works

A user with valid credentials submits the login form → parameterized query executes → user row is found → session is established → redirect to `/welcome`.

### SP-SQLI-02: Normal Registration Still Works

A user submits a unique username, valid email, and password → parameterized `INSERT` executes → record is created → redirect to `/login`.

### SP-SQLI-03: Normal Search Still Works

A user submits a non-empty query string → parameterized `LIKE` query executes → matching users are returned → HTML results rendered.

---

## Edge Cases

### EC-SQLI-01: SQL Payload in Username Field

Input: `admin' OR '1'='1' --`
Expected: Treated as a literal string. No user matching that exact username exists → login fails with 401 → no session created.

### EC-SQLI-02: SQL Payload in Password Field

Input: `' OR '1'='1`
Expected: Hashed normally via `hash_password()` → the resulting MD5 string is bound as a parameter → no match → login fails.

### EC-SQLI-03: SQL Payload in Search Query

Input: `' UNION SELECT username, password FROM users --`
Expected: Entire string treated as a literal `LIKE` pattern → no union executes → zero or empty results returned.

### EC-SQLI-04: SQL Payload in Signup Username

Input: `'); DROP TABLE users; --`
Expected: Entire string inserted as the literal username value → table is not dropped → duplicate-username error returned if the value already exists, otherwise account created with that literal string as username.

### EC-SQLI-05: Empty or Null Inputs

Inputs with missing fields → existing null-check guards trigger before the query is reached → appropriate error response returned without executing any SQL.

### EC-SQLI-06: Special Characters in Legitimate Input

Username containing apostrophes, quotes, or backslashes (e.g., `O'Brien`) → parameterized query handles escaping automatically → account created and authenticated correctly.

---

## Acceptance Criteria

### AC-SQLI-01

Given a login attempt with `admin' OR '1'='1' --` as username and any password, the system SHALL return a 401 response and SHALL NOT establish a session.

### AC-SQLI-02

Given a login attempt with valid credentials, the system SHALL authenticate the user and redirect to `/welcome` as before.

### AC-SQLI-03

Given a registration attempt with a username containing SQL metacharacters (e.g., single quotes), the system SHALL either create the account with the literal username or reject it for a business rule violation — it SHALL NOT raise an unhandled database exception.

### AC-SQLI-04

Given a search request with `?q=' UNION SELECT username, password FROM users --`, the response SHALL NOT contain any password hashes or data from a UNION query. It SHALL return a normal (empty or matched) results page.

### AC-SQLI-05

Given a registration attempt with a duplicate username (including one that contains SQL characters), the system SHALL return the existing duplicate-username error response.

### AC-SQLI-06

Given any valid search query containing only ordinary alphanumeric text, the system SHALL return matching results as before.

---

## Test Cases

| ID | Scenario | Input | Expected Result |
|----|----------|-------|-----------------|
| TC-SQLI-01 | SQL injection login bypass | Username: `admin' OR '1'='1' --`, Password: `anything` | 401 returned, no session created |
| TC-SQLI-02 | SQL injection via password field | Username: `admin`, Password: `' OR '1'='1` | 401 returned, no session created |
| TC-SQLI-03 | Valid login after fix | Correct username and password | Session created, redirect to `/welcome` |
| TC-SQLI-04 | Valid registration after fix | New unique username, email, password | Record created, redirect to `/login` |
| TC-SQLI-05 | Duplicate username after fix | Existing username | `Error: Username already exists` returned |
| TC-SQLI-06 | UNION injection via search | `?q=' UNION SELECT username, password FROM users --` | Normal results page, no password data exposed |
| TC-SQLI-07 | Search with plain query after fix | `?q=admin` | Matching users returned normally |
| TC-SQLI-08 | Empty search after fix | `?q=` (missing or blank) | `Error: Query parameter required` returned |
| TC-SQLI-09 | Username with apostrophe | Username: `O'Brien`, valid email and password | Account created with literal username `O'Brien` |
| TC-SQLI-10 | Login with apostrophe username | Username: `O'Brien`, correct password | Authenticated successfully |
| TC-SQLI-11 | DROP TABLE injection via signup | Username: `'); DROP TABLE users; --` | Table intact, literal username stored or duplicate error returned |
| TC-SQLI-12 | Empty login fields after fix | Username and password both blank | 401 returned, no query executed |
