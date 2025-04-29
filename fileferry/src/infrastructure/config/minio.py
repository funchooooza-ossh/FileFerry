from pydantic_settings import BaseSettings


class MinioConfig(BaseSettings):
    access: str
    secret: str
    endpoint: str
    secure: bool

    class Config:
        env_file = "minio.env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __repr__(self) -> str:
        return "<MiniOCredentials [secure]>"
