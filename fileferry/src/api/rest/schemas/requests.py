import uuid

from pydantic import BaseModel, field_validator


class FileRetrieve(BaseModel):
    file_id: str

    @field_validator("file_id")
    @classmethod
    def validate_file_id(cls, value: str) -> str:
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("file_id должен быть валидным UUID") from None
        return value
