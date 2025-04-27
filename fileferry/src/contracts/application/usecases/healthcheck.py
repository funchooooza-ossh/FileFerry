from typing import Any, Protocol


class HealthCheckUseCaseContract(Protocol):
    # TODO return type
    async def execute(self) -> dict[str, Any]: ...
