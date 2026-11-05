
from fastapi import APIRouter, Request
from app.proxy import proxy_request

router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)


@router.api_route(
    "",
    methods=["GET", "POST", "PATCH", "DELETE", "HEAD", "OPTIONS"]
)
async def orders_root(request: Request):
    return await proxy_request("orders", "", request)


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PATCH", "DELETE", "HEAD", "OPTIONS"]
)
async def orders_path(path: str, request: Request):
    return await proxy_request("orders", path, request)
