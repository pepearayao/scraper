ERROR_CODES = {
    # Auth
    "UNAUTHORIZED": "Authentication required",
    "FORBIDDEN": "Permission denied",
    "TOKEN_EXPIRED": "Authentication token has expired",
    "INVALID_CREDENTIALS": "Invalid username or password",
    "INVALID_REFRESH_TOKEN": "Invalid refresh token",
    # Resources
    "NOT_FOUND": "Resource not found",
    "ALREADY_EXISTS": "Resource already exists",
    "INVALID_INPUT": "Invalid input provided",
    "VALIDATION_ERROR": "Validation failed",
    # Limits
    "RATE_LIMIT_EXCEEDED": "Too many requests",
    "THROTTLED": "You are being throttled due to excessive requests",
    "USER_LOCKED": "Your account is locked due to repeated abuse",
    # System
    "INTERNAL_ERROR": "An unexpected error occurred",
    "SERVICE_UNAVAILABLE": "Service temporarily unavailable",
}
