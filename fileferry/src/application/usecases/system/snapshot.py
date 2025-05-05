from contracts.application import SnapshotUseCaseContract
from contracts.infrastructure import ImportantTaskManagerContract
from shared.types.task_manager import ManagerSnapshot


class SnapShotUseCase(SnapshotUseCaseContract):
    def __init__(self, manager: ImportantTaskManagerContract) -> None:
        self._manager = manager

    def execute(self) -> ManagerSnapshot:
        return self._manager.snapshot()
