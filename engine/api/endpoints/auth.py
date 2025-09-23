from django.contrib.auth import authenticate
from ninja import Router, Schema
from rest_framework_simplejwt.tokens import RefreshToken

router = Router()


class TokenRequest(Schema):
    username: str
    password: str


class RefreshRequest(Schema):
    refresh: str


class TokenResponse(Schema):
    access: str
    refresh: str


class RefreshResponse(Schema):
    access: str


class ErrorResponse(Schema):
    error: str


@router.post("/token", response={200: TokenResponse, 401: ErrorResponse})
def obtain_token(request, data: TokenRequest):
    user = authenticate(username=data.username, password=data.password)
    if user:
        refresh = RefreshToken.for_user(user)
        return 200, {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    return 401, {"error": "Invalid credentials"}


@router.post("/refresh", response={200: RefreshResponse, 401: ErrorResponse})
def refresh_token(request, data: RefreshRequest):
    try:
        refresh_token = RefreshToken(data.refresh)
        return 200, {
            "access": str(refresh_token.access_token),
        }
    except Exception:
        return 401, {"error": "Invalid refresh token"}
