"""
security.py
Provides password hashing utilities used during user registration and authentication.
Uses bcrypt with a minimum work factor of 12 for secure password storage.
"""
import bcrypt


def hash_password(password: str) -> str:
    """Return the bcrypt hash of the given password string with automatic salt generation.

    Uses a minimum work factor of 12 to provide adequate resistance to brute-force
    attacks on modern hardware.

    Args:
        password: The plaintext password to hash.

    Returns:
        A bcrypt hash string containing the salt, work factor, and hashed password.
        The hash begins with '$2b$' indicating bcrypt format.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Verify that a plaintext password matches a stored bcrypt hash.

    Uses bcrypt's secure constant-time comparison mechanism to prevent timing attacks.
    Handles malformed hash strings (e.g., legacy MD5 values) by returning False.

    Args:
        plain: The plaintext password to verify.
        hashed: The stored bcrypt hash to compare against.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False