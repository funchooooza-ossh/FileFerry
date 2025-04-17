from miniopy_async import Minio
from application.di.minio.registry import minio_clients, KnownMinioClients


def create_minio_client(_type: KnownMinioClients) -> Minio:
    creds = minio_clients.get(_type)
    return Minio(
        access_key=creds["access"],
        secret_key=creds["secret"],
        endpoint=creds["endpoint"],
        secure=creds["secure"],
    )
