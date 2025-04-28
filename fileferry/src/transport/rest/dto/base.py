from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

from domain.models import ComponentStatuses, HealthReport
from shared.enums import HealthStatus

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
    status: HealthStatus
    components: ComponentStatuses

    @classmethod
    def from_domain(cls, report: HealthReport) -> "HealthCheck":
        return HealthCheck(status=report.status, components=report.components)
