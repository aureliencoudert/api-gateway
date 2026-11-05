import secrets

from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

from app.config import API_KEY


api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


async def verify_api_key(api_key: str = Security(api_key_header)):

    if not api_key or not secrets.compare_digest(api_key, API_KEY):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key"
        )

    return api_key
