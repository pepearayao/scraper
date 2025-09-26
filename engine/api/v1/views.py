from ninja import NinjaAPI
from ninja.errors import AuthenticationError

from ..auth import JWTAuth
from ..exception_handlers import global_exception_handler
from ..responses import fail
from .routers import auth, jobs, projects, results, runs

api_v1 = NinjaAPI(
    auth=JWTAuth(), version="1.0.0", title="Scraper Engine API v1", urls_namespace="v1"
)

# Register global exception handler
api_v1.exception_handler(Exception)(global_exception_handler)


# Specifically handle authentication errors
# NOTE: Exception handlers MUST return HttpResponse objects (like JsonResponse),
# not dictionaries. This is different from regular endpoints which return dicts
# that Django Ninja automatically converts to JSON responses.
@api_v1.exception_handler(AuthenticationError)
def auth_exception_handler(request, exc):
    from django.http import JsonResponse

    # Get our standardized error format as a dict
    error_response = fail("UNAUTHORIZED", status=401)
    # Convert to JsonResponse because Django middleware expects HttpResponse objects
    return JsonResponse(error_response, status=401)


api_v1.add_router("/auth", auth.router, auth=None)
api_v1.add_router("/projects", projects.router)
api_v1.add_router("/jobs", jobs.router)
api_v1.add_router("/runs", runs.router)
api_v1.add_router("/results", results.router)


@api_v1.get("/hello")
def hello_v1(request, name: str = "world"):
    return {"message": "Hello from v1!", "version": "1.0.0"}
