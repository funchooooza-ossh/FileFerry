from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiohttp
from aiohttp import ClientSession, TCPConnector
from aiohttp_retry import ExponentialRetry, RetryClient


@asynccontextmanager
async def create_client_session() -> AsyncGenerator[RetryClient, None]:
    """
    Фабрика создания aiohttp RetryClient.
    Используется для явного управления сессией в функциях работы с API MiniO
    Вынесение этой функции - явно позволяет знать, что мы не копим не закрытые сессии,
    которые передаем например Minio.get_object(..., session=<ClientSession | RetryClient>)
    """
    session = RetryClient(
        ClientSession(
            connector=TCPConnector(limit=10, ssl=False),
            timeout=aiohttp.ClientTimeout(total=60),
        ),
        retry_options=ExponentialRetry(attempts=3),
    )
    try:
        yield session
    finally:
        await session.close()
