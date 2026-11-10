from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def roles_required(*role_names):
    """Réserve une vue aux utilisateurs connectés ayant au moins un des rôles."""

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not any(current_user.has_role(name) for name in role_names):
                abort(403)
            return view(*args, **kwargs)

        return login_required(wrapped)

    return decorator
