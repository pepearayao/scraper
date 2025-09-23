from ninja import NinjaAPI

from .auth import JWTAuth
from .endpoints import auth, jobs, projects, results, runs

api = NinjaAPI(auth=JWTAuth())

api.add_router("/auth", auth.router, auth=None)
api.add_router("/projects", projects.router)
api.add_router("/jobs", jobs.router)
api.add_router("/runs", runs.router)
api.add_router("/results", results.router)


@api.get("/hello")
def hello(request, name: str = "world"):
    return {"message": "SAPA!"}
