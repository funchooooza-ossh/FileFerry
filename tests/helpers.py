from typing import AsyncIterator, TypeVar

T = TypeVar("T")


class aiter:
    def __init__(self, items: list[T]):
        self._items = iter(items)

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        try:
            return next(self._items)
        except StopIteration:
            raise StopAsyncIteration
