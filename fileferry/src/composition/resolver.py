from collections.abc import Callable

from composition.scenarios.minio_sqla import bootstrap_minio_sqla
from contracts.composition import DependencyContext, FileAPIAdapterContract, ScenarioName

BOOTSTRAP_FN = Callable[[DependencyContext], FileAPIAdapterContract]


_BOOTSTRAP_REGISTRY: dict[ScenarioName, BOOTSTRAP_FN] = {
    ScenarioName.MINIO_SQLA: bootstrap_minio_sqla,
    # ScenarioName.SFTP_MONGO: bootstrap_sftp_mongo,
}


def di_resolver(ctx: DependencyContext) -> FileAPIAdapterContract:
    try:
        return _BOOTSTRAP_REGISTRY[ctx.scenario](ctx)
    except KeyError:
        raise ValueError(f"Unknown DI scenario: {ctx.scenario}") from None
