from composition.bootstrap.upload_minio_sqla import bootstrap_minio_sqla
from composition.contracts import ApplicationFileService, DependencyContext


def di_resolver(ctx: DependencyContext) -> ApplicationFileService:
    match ctx.scenario:
        case "minio-sqla":
            return bootstrap_minio_sqla(ctx)
        case "sftp-mongo":
            raise NotImplementedError("SFTP-Mongo bootstrap not implemented")
        case _:
            raise ValueError(f"Unknown DI scenario: {ctx.scenario}")
