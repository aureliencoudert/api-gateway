
import httpx
from fastapi import Request, HTTPException
from fastapi.responses import Response


SERVICES = {
    "users": "http://127.0.0.1:8001/api/users",
    "products": "http://127.0.0.1:8002/api/products",
    "orders": "http://127.0.0.1:8003/api/orders",
}


async def proxy_request(service: str, path: str, request: Request):

    target_url = SERVICES[service]

    if path:
        target_url += "/" + path

    excluded_headers = {
        "host", "connection", "content-length", "transfer-encoding"
    }

    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in excluded_headers
    }

    try:
        client = request.app.state.http_client

        upstream_response = await client.request(
            method=request.method,
            url=target_url,
            params=request.query_params,
            content=await request.body(),
            headers=headers,
        )

        response_headers = {
            key: value
            for key, value in upstream_response.headers.items()
            if key.lower() not in {
                "connection",
                "transfer-encoding",
                "content-length",
                "content-encoding",
            }
        }

        return Response(
            content=upstream_response.content,
            status_code=upstream_response.status_code,
            headers=response_headers,
        )

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Gateway Timeout")

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: upstream service unavailable"
        )
