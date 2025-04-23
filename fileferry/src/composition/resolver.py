from collections.abc import Callable

from composition.bootstrap.minio_sqla import bootstrap_minio_sqla
from contracts.composition import DependencyContext, FileAPIAdapterContract, ScenarioName

_BOOTSTRAP_REGISTRY: dict[ScenarioName, Callable[[DependencyContext], FileAPIAdapterContract]] = {
    ScenarioName.MINIO_SQLA: bootstrap_minio_sqla,
    # ScenarioName.SFTP_MONGO: bootstrap_sftp_mongo,
}


def di_resolver(ctx: DependencyContext) -> FileAPIAdapterContract:
    try:
        return _BOOTSTRAP_REGISTRY[ctx.scenario](ctx)
    except KeyError:
        raise ValueError(f"Unknown DI scenario: {ctx.scenario}") from None
