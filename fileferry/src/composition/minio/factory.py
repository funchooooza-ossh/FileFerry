from miniopy_async import Minio

from composition.minio.config import KnownMinioClients, minio_clients


def create_minio_client(_type: KnownMinioClients) -> Minio:
    creds = minio_clients.get(_type)
    if creds is None:
        raise ValueError(f"Unknown Minio client type: {_type}")

    return Minio(
        access_key=creds["access"],
        secret_key=creds["secret"],
        endpoint=creds["endpoint"],
        secure=creds["secure"],
    )
