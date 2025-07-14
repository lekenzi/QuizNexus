import logging
from functools import wraps

from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request


def jwt_auth_required(f):
    """
    Custom JWT authentication wrapper that checks token validity
    and handles different authentication scenarios.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:

            verify_jwt_in_request()

            jwt_claims = get_jwt()
            current_user_id = get_jwt_identity()

            if not jwt_claims or not current_user_id:
                return {
                    "message": "Invalid token",
                    "redirect_to_login": True,
                    "error_code": "INVALID_TOKEN",
                }, 401

            if jwt_claims.get("exp", 0) < jwt_claims.get("iat", 0):
                return {
                    "message": "Token has expired",
                    "redirect_to_login": True,
                    "error_code": "TOKEN_EXPIRED",
                }, 401

            logging.info(f"User {current_user_id} authenticated successfully")
            return f(*args, **kwargs)

        except Exception as e:
            logging.error(f"JWT authentication error: {str(e)}")
            return {
                "message": "Authentication failed. Please login again.",
                "redirect_to_login": True,
                "error_code": "AUTH_ERROR",
                "details": str(e),
            }, 401

    return decorated_function


def role_required(required_roles):
    """
    Role-based access control decorator.
    Can be used in combination with jwt_auth_required.

    Usage: @role_required(['admin', 'user'])
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:

                jwt_claims = get_jwt()

                if not jwt_claims:
                    return {
                        "message": "No valid token found",
                        "redirect_to_login": True,
                        "error_code": "NO_TOKEN",
                    }, 401

                user_role = jwt_claims.get("role")

                if not user_role:
                    return {
                        "message": "No role found in token",
                        "redirect_to_login": True,
                        "error_code": "NO_ROLE",
                    }, 401

                if user_role not in required_roles:
                    return {
                        "message": f"Access denied. Required roles: {required_roles}, your role: {user_role}",
                        "redirect_to_login": False,
                        "error_code": "INSUFFICIENT_PERMISSIONS",
                    }, 403

                return f(*args, **kwargs)

            except Exception as e:
                logging.error(f"Role check error: {str(e)}")
                return {
                    "message": "Authorization failed",
                    "redirect_to_login": True,
                    "error_code": "AUTH_ERROR",
                    "details": str(e),
                }, 401

        return decorated_function

    return decorator


def optional_jwt_auth(f):
    """
    Optional JWT authentication - doesn't fail if no token provided.
    Useful for endpoints that work for both authenticated and non-authenticated users.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
            return f(*args, **kwargs)
        except Exception as e:
            logging.info(f"Optional JWT auth failed: {str(e)}")
            return f(*args, **kwargs)

    return decorated_function


class AuthMiddleware:
    """
    Class-based middleware for more complex authentication logic
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the middleware with Flask app"""
        app.before_request(self.check_auth_status)

    def check_auth_status(self):
        """
        Global middleware to check authentication status
        Can be used to log authentication attempts, rate limiting, etc.
        """
        pass
