from typing import Any, List, Optional

from ninja import Schema

from .error_codes import ERROR_CODES

# IMPORTANT: These functions return dictionaries, NOT HttpResponse objects
#
# Usage patterns:
# 1. Regular Django Ninja endpoints: Return these dicts directly
#    Django Ninja automatically converts them to JSON responses
#    Example: return success({"user": "john"})
#
# 2. Exception handlers: Must wrap in JsonResponse
#    Django middleware expects HttpResponse objects, not dicts
#    Example: return JsonResponse(fail("ERROR_CODE", status=400), status=400)
#
# This design keeps response formatting consistent while working with
# Django Ninja's automatic serialization for regular endpoints.


def success(data: Any, meta: dict = None):
    """Return standardized success response as dict (for Django Ninja endpoints)"""
    return {"status": "ok", "data": data, "meta": meta}


def fail(
    code: str,
    message: str = None,
    errors: List[dict] = None,
    status: int = 400,
    retry_after: int = None,
):
    """Return standardized error response as dict (for Django Ninja endpoints)"""
    if code not in ERROR_CODES:
        raise ValueError(f"Invalid error code: {code}")
    return {
        "status": "error",
        "message": message or ERROR_CODES[code],
        "code": code,
        "errors": errors or [],
        "http_status": status,
        "retry_after": retry_after,
    }
