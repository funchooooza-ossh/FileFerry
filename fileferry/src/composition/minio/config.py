from typing import Literal

from infrastructure.config.minio import MinioDefaultCredentials
from shared.types.minio_creds import MinioCreds

minio_default = MinioDefaultCredentials()


KnownMinioClients = Literal["default", "archive", "private"]

minio_clients: dict[KnownMinioClients, MinioCreds] = {
    "default": minio_default.to_typed_dict()
}
