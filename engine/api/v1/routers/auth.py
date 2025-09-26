import json

from django.contrib.auth import authenticate
from ninja import Router
from ninja.errors import HttpError
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
    response={
        200: TokenSuccessResponse,
        401: ErrorResponse,
        400: ErrorResponse,
        404: ErrorResponse,
    },
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

    raise HttpError(401, json.dumps(fail("INVALID_CREDENTIALS")))


@router.post(
    "/refresh",
    response={
        200: RefreshSuccessResponse,
        401: ErrorResponse,
        400: ErrorResponse,
        404: ErrorResponse,
    },
)
def refresh_token(request, data: RefreshRequest):
    try:
        refresh_token = RefreshToken(data.refresh)
        data = {
            "access": str(refresh_token.access_token),
        }
        return success(data)
    except Exception:
        raise HttpError(401, json.dumps(fail("INVALID_REFRESH_TOKEN")))
