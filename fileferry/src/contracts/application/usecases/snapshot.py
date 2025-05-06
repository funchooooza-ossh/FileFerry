from typing import Protocol

from shared.types.task_manager import ManagerSnapshot


class SnapshotUseCaseContract(Protocol):
    def execute(self) -> ManagerSnapshot: ...
