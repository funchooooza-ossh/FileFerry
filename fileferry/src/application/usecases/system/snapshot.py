from contracts.application import SnapshotUseCaseContract
from contracts.infrastructure import ImportantTaskManagerContract
from monitoring.cache_background import (
    important_tasks_active,
    important_tasks_age,
    important_tasks_total,
)
from shared.types.task_manager import ManagerSnapshot


class SnapShotUseCase(SnapshotUseCaseContract):
    def __init__(self, manager: ImportantTaskManagerContract) -> None:
        self._manager = manager

    def execute(self) -> ManagerSnapshot:
        snapshot: ManagerSnapshot = self._manager.snapshot()

        important_tasks_active.set(snapshot["active_task_count"])
        important_tasks_total.set(snapshot["total_task_count"])

        important_tasks_age.clear()
        for key, age in snapshot["task_ages"].items():
            important_tasks_age.labels(key=key).set(age)

        return snapshot
