
import hashlib
import secrets

from database import create_user, get_user_by_email


def hash_password(password):
    """Securely hash a password using PBKDF2."""
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        600000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_hash):
    """Verify a password against its stored hash."""
    try:
        salt, original_hash = stored_hash.split("$")

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            600000
        ).hex()

        return secrets.compare_digest(new_hash, original_hash)

    except (ValueError, AttributeError):
        return False


def register_user(name, email, password):
    """Register a new citizen."""
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "Please fill in all fields."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if get_user_by_email(email):
        return False, "This email is already registered."

    password_hash = hash_password(password)

    success = create_user(name, email, password_hash)

    if success:
        return True, "Registration successful!"

    return False, "Registration failed. Please try again."


def login_user(email, password):
    """Authenticate a citizen."""
    email = email.strip().lower()

    user = get_user_by_email(email)

    if user and verify_password(password, user["password_hash"]):
        return True, dict(user)

    return False, None
