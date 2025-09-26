from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http import Http404, JsonResponse
from ninja.errors import AuthenticationError

from .responses import fail

# NOTE: Exception handlers MUST return HttpResponse objects (like JsonResponse),
# not dictionaries. This is different from regular endpoints which return dicts
# that Django Ninja automatically converts to JSON responses.


def global_exception_handler(request, exc):
    """Single global exception handler for all API errors"""

    if isinstance(exc, ValidationError):
        error_response = fail("VALIDATION_ERROR", status=400)
        return JsonResponse(error_response, status=400)

    elif isinstance(exc, (Http404, ObjectDoesNotExist)):
        error_response = fail("NOT_FOUND", status=404)
        return JsonResponse(error_response, status=404)

    elif isinstance(exc, PermissionDenied):
        error_response = fail("FORBIDDEN", status=403)
        return JsonResponse(error_response, status=403)

    else:
        # Catch-all for any other exception
        error_response = fail("INTERNAL_ERROR", status=500)
        return JsonResponse(error_response, status=500)
