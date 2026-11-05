
from contextlib import asynccontextmanager
from app.auth import verify_api_key

import httpx
from fastapi import FastAPI, Security

from app.routers import users, products, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=10.0)
    yield
    await app.state.http_client.aclose()


app = FastAPI(
    title="API Gateway",
    description="Gateway for Users, Products and Orders services",
    version="1.0.0",
    lifespan=lifespan,
    dependencies=[Security(verify_api_key)],
)


app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/")
async def root():
    return {"message": "API Gateway is running"}
