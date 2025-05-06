from typing import TypedDict


class ManagerSnapshot(TypedDict):
    active_task_count: int
    total_task_count: int
    task_keys: list[str]
    task_ages: dict[str, float]
