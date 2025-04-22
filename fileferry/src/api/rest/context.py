from fastapi import Header, HTTPException

from composition.resolver import di_resolver
from contracts.composition import DependencyContext, FileAPIAdapterContract


def make_di_resolver(action: str) -> FileAPIAdapterContract:
    def _resolver(
        x_scenario: str = Header(..., alias="X-Scenario"),
        x_bucket: str = Header("default-bucket", alias="X-Bucket"),
    ) -> FileAPIAdapterContract:
        try:
            ctx = DependencyContext(
                scenario=x_scenario,
                bucket_name=x_bucket,
                action=action,
            )
            return di_resolver(ctx)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=f"Invalid header value: {exc}") from exc

    return _resolver
