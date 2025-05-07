from typing import Protocol

from infrastructure.types.task_snapshot import ManagerSnapshot


class SnapshotUseCaseContract(Protocol):
    def execute(self) -> ManagerSnapshot: ...
