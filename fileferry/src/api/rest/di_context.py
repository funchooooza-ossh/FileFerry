from collections.abc import Callable

from fastapi import Header, HTTPException

from composition.resolver import di_resolver
from contracts.composition import (
    DependencyContext,
    ExistingBuckets,
    FileAction,
    FileAPIAdapterContract,
    HealthCheckAPIAdapterContract,
    ScenarioName,
)


def resolve_headers(
    action: FileAction,
) -> Callable[..., DependencyContext]:
    def _resolver(
        x_scenario: ScenarioName = Header(..., alias="X-Scenario"),
        x_bucket: ExistingBuckets = Header("default-bucket", alias="X-Bucket"),
    ) -> DependencyContext:
        try:
            return DependencyContext(
                action=action, scenario=x_scenario, bucket_name=x_bucket
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid header value") from exc

    return _resolver


def make_di_resolver(action: FileAction) -> Callable[..., FileAPIAdapterContract]:
    def _resolver(
        x_scenario: ScenarioName = Header(..., alias="X-Scenario"),
        x_bucket: ExistingBuckets = Header("default-bucket", alias="X-Bucket"),
    ) -> FileAPIAdapterContract:
        try:
            ctx = DependencyContext(
                scenario=ScenarioName(x_scenario),
                bucket_name=ExistingBuckets(x_bucket),
                action=action,
            )
            return di_resolver(ctx)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid header value") from exc

    return _resolver


def make_healtcheck_resolver(scenario: ScenarioName) -> HealthCheckAPIAdapterContract:
    try:
        action = FileAction.HEALTH
        ctx = DependencyContext(
            scenario=scenario, action=action, bucket_name=ExistingBuckets.DEFAULT
        )
        return di_resolver(ctx=ctx)  # type: ignore
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid healtcheck value") from exc
