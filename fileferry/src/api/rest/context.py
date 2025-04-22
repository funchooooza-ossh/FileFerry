from typing import Annotated

from fastapi import Depends, Header, HTTPException

from composition.resolver import di_resolver
from contracts.composition import DependencyContext, FileAPIAdapterContract


def resolve_context_from_headers(
    x_scenario: str = Header(..., alias="X-Scenario"),
    x_bucket: str = Header("default-bucket", alias="X-Bucket"),
    x_action: str = Header(..., alias="X-Action"),
) -> DependencyContext:
    try:
        ctx = DependencyContext(
            scenario=x_scenario,
            bucket_name=x_bucket,
            action=x_action,
        )
        return di_resolver(ctx)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid header value: {exc}") from exc


ApplicationDI = Annotated[FileAPIAdapterContract, Depends(resolve_context_from_headers)]
