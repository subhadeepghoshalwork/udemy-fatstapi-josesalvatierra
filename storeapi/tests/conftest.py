from typing import AsyncGenerator, Generator
import pytest, pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient

from storeapi.main import app
from storeapi.routers.post import comments_table, post_table

@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest_asyncio.fixture(autouse=True)
async def db() -> AsyncGenerator:
    post_table.clear()
    comments_table.clear()
    yield

@pytest_asyncio.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=client.base_url,
    ) as ac:
        yield ac
