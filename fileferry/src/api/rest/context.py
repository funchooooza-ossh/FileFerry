from fastapi import Header, HTTPException

from composition.contracts import DependencyContext


def resolve_context_from_headers(
    x_scenario: str = Header(..., alias="X-Scenario"),
    x_bucket: str = Header("default-bucket", alias="X-Bucket"),
    x_action: str = Header(..., alias="X-Action"),
) -> DependencyContext:
    try:
        return DependencyContext(
            scenario=x_scenario,
            bucket_name=x_bucket,
            action=x_action,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid header value: {exc}") from exc
