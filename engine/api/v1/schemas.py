from datetime import datetime
from typing import Any, List, Optional

from ninja import Schema

####################################################################
####################################################################
# Standard Responses Schemas #######################################
####################################################################
####################################################################


class MetaSchema(Schema):
    page: Optional[int] = None
    page_size: Optional[int] = None
    total: Optional[int] = None


class ErrorDetail(Schema):
    field: Optional[str] = None
    message: str


class ErrorResponse(Schema):
    status: str
    code: str
    message: str
    errors: List[ErrorDetail] = []
    http_status: int
    retry_after: Optional[int] = None


####################################################################
####################################################################
# Auth Responses Schemas ###########################################
####################################################################
####################################################################


class TokenRequest(Schema):
    email: str
    password: str


class RefreshRequest(Schema):
    refresh: str


class TokenResponse(Schema):
    access: str
    refresh: str


class RefreshResponse(Schema):
    access: str


class TokenSuccessResponse(Schema):
    status: str
    data: TokenResponse
    meta: Optional[MetaSchema] = None


class RefreshSuccessResponse(Schema):
    status: str
    data: RefreshResponse
    meta: Optional[MetaSchema] = None


####################################################################
####################################################################
# Project Responses Schemas ########################################
####################################################################
####################################################################


class ProjectSchema(Schema):
    id: str
    name: str
    owner_id: int
    created_at: datetime


class ProjectSuccessResponse(Schema):
    status: str
    data: List[ProjectSchema]
    meta: Optional[MetaSchema] = None


class ProjectCreateSchema(Schema):
    name: str


class ProjectUpdateSchema(Schema):
    name: str
