from ninja import NinjaAPI

from ..auth import JWTAuth
from ..exception_handlers import global_exception_handler

api_v2 = NinjaAPI(
    auth=JWTAuth(), version="2.0.0", title="Scraper Engine API v2", urls_namespace="v2"
)

# Register global exception handler
api_v2.exception_handler(Exception)(global_exception_handler)


@api_v2.get("/hello")
def hello_v2(request, name: str = "world"):
    return {"message": "Hello from v2!", "version": "2.0.0"}
