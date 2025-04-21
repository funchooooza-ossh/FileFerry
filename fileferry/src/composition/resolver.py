from composition.bootstrap.minio_sqla import bootstrap_minio_sqla
from contracts.composition import ApplicationFileService, DependencyContext, ScenarioName

_BOOTSTRAP_REGISTRY: dict[ScenarioName, callable] = {
    ScenarioName.MINIO_SQLA: bootstrap_minio_sqla,
    # ScenarioName.SFTP_MONGO: bootstrap_sftp_mongo,
}


def di_resolver(ctx: DependencyContext) -> ApplicationFileService:
    try:
        return _BOOTSTRAP_REGISTRY[ctx.scenario](ctx)
    except KeyError:
        raise ValueError(f"Unknown DI scenario: {ctx.scenario}") from None
