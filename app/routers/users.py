
from fastapi import APIRouter, Request
from app.proxy import proxy_request

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.api_route(
    "",
    methods=["GET", "POST", "PATCH", "DELETE", "HEAD", "OPTIONS"]
)
async def users_root(request: Request):
    return await proxy_request("users", "", request)


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PATCH", "DELETE", "HEAD", "OPTIONS"]
)
async def users_path(path: str, request: Request):
    return await proxy_request("users", path, request)
