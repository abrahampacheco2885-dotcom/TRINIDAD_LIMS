from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Compare role case-insensitively and tolerate missing attribute
        if not current_user.is_authenticated or getattr(current_user, 'rol', '').lower() != 'admin':
            abort(403) # Prohibido
        return f(*args, **kwargs)
    return decorated_function


def roles_required(*roles):
    """Decorator to require one of the provided roles (case-insensitive)."""
    roles_normalized = [r.lower() for r in roles]
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            user_role = getattr(current_user, 'rol', '') or ''
            if user_role.lower() not in roles_normalized:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator