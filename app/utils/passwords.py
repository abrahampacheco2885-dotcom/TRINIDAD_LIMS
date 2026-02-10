import secrets
import string
import re

# Policy:
# - Minimum total length: 8
# - At least 6 digits
# - At least 1 uppercase letter
# - At least 1 lowercase letter

DIGIT_MIN = 6
MIN_LENGTH = 8

_digit_re = re.compile(r"\d")
_upper_re = re.compile(r"[A-Z]")
_lower_re = re.compile(r"[a-z]")


def validate_password(pw: str):
    if not pw or len(pw) < MIN_LENGTH:
        return False, f"La contraseña debe tener al menos {MIN_LENGTH} caracteres."
    digits = len(_digit_re.findall(pw))
    if digits < DIGIT_MIN:
        return False, f"La contraseña debe contener al menos {DIGIT_MIN} dígitos (números)."
    if not _upper_re.search(pw):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    if not _lower_re.search(pw):
        return False, "La contraseña debe contener al menos una letra minúscula."
    return True, "OK"


def generate_password():
    # Build a password satisfying the rules
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_"
    while True:
        # ensure required digits and cases
        digits = ''.join(secrets.choice(string.digits) for _ in range(DIGIT_MIN))
        upper = secrets.choice(string.ascii_uppercase)
        lower = secrets.choice(string.ascii_lowercase)
        # fill to at least MIN_LENGTH
        remaining_len = max(0, MIN_LENGTH - (DIGIT_MIN + 2))
        rest = ''.join(secrets.choice(alphabet) for _ in range(remaining_len))
        # shuffle
        candidate = list(digits + upper + lower + rest)
        secrets.SystemRandom().shuffle(candidate)
        pw = ''.join(candidate)
        ok, _ = validate_password(pw)
        if ok:
            return pw
