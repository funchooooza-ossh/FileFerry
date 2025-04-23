class EmptyAsyncIterator:
    def __aiter__(self):
        return self

    async def __anext__(self):
        raise StopAsyncIteration


class SimpleAsyncIterator:
    def __init__(self, data: bytes):
        self.data = data
        self.index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index < len(self.data):
            chunk = self.data[self.index : self.index + 5]
            self.index += 5
            return chunk
        raise StopAsyncIteration
