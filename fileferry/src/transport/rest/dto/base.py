from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

from shared.types.system_health import SystemHealthReport

DataT = TypeVar("DataT", bound=BaseModel)


class Error(BaseModel):
    msg: str
    type: str


class Response(GenericModel, Generic[DataT]):
    data: Optional[DataT]
    error: Optional[Error]

    @classmethod
    def success(cls, data: DataT) -> "Response[DataT]":
        return cls(data=data, error=None)

    @classmethod
    def failure(cls, msg: str, type: str) -> "Response[DataT]":
        return cls(data=None, error=Error(msg=msg, type=type))


class HealthCheck(BaseModel):
    uptime: int
    components: SystemHealthReport

    @classmethod
    def from_domain(cls, uptime: int, report: SystemHealthReport) -> "HealthCheck":
        return HealthCheck(uptime=uptime, components=report)
