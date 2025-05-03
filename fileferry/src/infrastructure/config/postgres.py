from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    user: str
    password: str
    db: str
    port: str
    host: str

    def __repr__(self) -> str:
        return "<DBSettings [secure]>"


class PostgresSettings(DBSettings):
    class Config:
        env_prefix = "POSTGRES_"
        env_file = "postgres.env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


pg_settings = PostgresSettings()  # type: ignore
