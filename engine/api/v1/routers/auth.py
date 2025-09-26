from django.contrib.auth import authenticate
from ninja import Router
from rest_framework_simplejwt.tokens import RefreshToken

from ...responses import fail, success
from ..schemas import (
    ErrorResponse,
    RefreshRequest,
    RefreshSuccessResponse,
    TokenRequest,
    TokenSuccessResponse,
)

router = Router()


@router.post(
    "/token",
    response={200: TokenSuccessResponse, 400: ErrorResponse, 404: ErrorResponse},
)
def obtain_token(request, data: TokenRequest):
    user = authenticate(email=data.email, password=data.password)
    if user:
        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return success(data)

    return fail("INVALID_CREDENTIALS", status=401)


@router.post(
    "/refresh",
    response={200: RefreshSuccessResponse, 400: ErrorResponse, 404: ErrorResponse},
)
def refresh_token(request, data: RefreshRequest):
    try:
        refresh_token = RefreshToken(data.refresh)
        data = {
            "access": str(refresh_token.access_token),
        }
        return success(data)
    except Exception:
        return fail("INVALID_REFRESH_TOKEN", status=401)
