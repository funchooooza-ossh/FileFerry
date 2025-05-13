from collections.abc import AsyncIterator
from types import TracebackType
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import ClientResponse
from miniopy_async import Minio
from miniopy_async.datatypes import Bucket
from multidict import CIMultiDict, CIMultiDictProxy


@pytest.fixture
async def mock_client_response(stream: AsyncIterator[bytes]) -> ClientResponse:
    mock_response = AsyncMock(spec=ClientResponse)
    mock_response.status = 200
    mock_response.reason = "OK"
    mock_response.version = "1.1"
    mock_response._headers = CIMultiDictProxy(
        CIMultiDict({"Content-Type": "application/octet-stream"})
    )
    mock_response._raw_headers = ((b"Content-Type", b"application/octet-stream"),)
    mock_response._body = None
    mock_response.content = MagicMock()
    mock_response.content.iter_chunked = MagicMock(return_value=stream)

    async def async_enter():
        return mock_response

    async def async_exit(
        exc_type: type[Exception], exc_val: Any, exc_tb: TracebackType
    ):
        pass

    mock_response.__aenter__.side_effect = async_enter
    mock_response.__aexit__.side_effect = async_exit

    return mock_response


@pytest.fixture(scope="function")
async def mock_minio_client(mock_client_response: ClientResponse) -> Minio:
    client = AsyncMock(spec=Minio)
    client.put_object = AsyncMock()
    client.get_object = AsyncMock(return_value=mock_client_response)
    client.remove_object = AsyncMock()
    client.list_buckets = AsyncMock(
        return_value=[Bucket(name="test_bucket", creation_date=None)]
    )

    return client
