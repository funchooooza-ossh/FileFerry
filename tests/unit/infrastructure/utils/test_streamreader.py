import asyncio
from typing import AsyncIterator

import pytest
from infrastructure.utils.stream_reader import AsyncStreamReader


async def async_byte_stream(
    chunks: list[bytes], delay: float = 0.01
) -> AsyncIterator[bytes]:
    for chunk in chunks:
        await asyncio.sleep(delay)
        yield chunk


@pytest.mark.asyncio
async def test_iterates_all_chunks():
    chunks = [b"chunk1", b"chunk2", b"chunk3", b"chunk4"]
    stream = async_byte_stream(chunks)
    reader = AsyncStreamReader(stream)
    result: list[bytes] = []
    async for chunk in reader:
        result.append(chunk)
    assert result == chunks


@pytest.mark.asyncio
async def test_read_full_stream():
    chunks = [b"chunk1", b"chunk2", b"chunk3", b"chunk4"]
    stream = async_byte_stream(chunks)
    reader = AsyncStreamReader(stream)
    data = await reader.read()
    expected = b"".join(chunks)
    assert data == expected


@pytest.mark.asyncio
async def test_read_partial_then_rest():
    chunks = [b"chunk1", b"chunk2", b"chunk3", b"chunk4"]
    stream = async_byte_stream(chunks)
    reader = AsyncStreamReader(stream)

    part1 = await reader.read(10)
    assert part1 == b"chunk1chun"

    part2 = await reader.read()
    assert part2 == b"k2chunk3chunk4"


@pytest.mark.asyncio
async def test_read_exact_length():
    chunks = [b"chunk1", b"chunk2", b"chunk3", b"chunk4"]
    stream = async_byte_stream(chunks)
    reader = AsyncStreamReader(stream)

    total_length = sum(len(c) for c in chunks)
    data = await reader.read(total_length)
    assert data == b"".join(chunks)

    remainder = await reader.read()
    assert remainder == b""


@pytest.mark.asyncio
async def test_read_past_end_returns_empty():
    chunks = [b"chunk1", b"chunk2", b"chunk3", b"chunk4"]
    stream = async_byte_stream(chunks)
    reader = AsyncStreamReader(stream)

    data = await reader.read(1000)
    assert data == b"".join(chunks)

    remainder = await reader.read()
    assert remainder == b""
