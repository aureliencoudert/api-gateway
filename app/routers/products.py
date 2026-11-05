
from fastapi import APIRouter, Request
from app.proxy import proxy_request

router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.api_route(
    "",
    methods=["GET", "POST", "PATCH", "DELETE", "HEAD", "OPTIONS"]
)
async def products_root(request: Request):
    return await proxy_request("products", "", request)


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PATCH", "DELETE", "HEAD", "OPTIONS"]
)
async def products_path(path: str, request: Request):
    return await proxy_request("products", path, request)
