from dataclasses import dataclass
from typing import Any, TypedDict


class RepoHealthStatus(TypedDict):
    ok: bool
    details: dict[str, Any]


class BucketInfo(TypedDict):
    name: str
    description: str


class StorageHealthStatus(TypedDict):
    ok: bool
    details: dict[str, Any]


@dataclass(slots=True, frozen=True)
class ServiceHealthStatus:
    ok: bool
    details: dict[str, Any]

    @classmethod
    def from_infrastructure(
        cls, storage_status: StorageHealthStatus, repo_status: RepoHealthStatus
    ) -> "ServiceHealthStatus":
        ok = storage_status["ok"] and repo_status["ok"]
        details = {"storage": storage_status["details"], "repo": repo_status["details"]}
        return cls(ok=ok, details=details)
