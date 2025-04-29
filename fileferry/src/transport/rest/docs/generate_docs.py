from typing import Any, Union

from shared.exceptions.mappers.alchemy_errors import SQLAlchemyErrorCode
from shared.exceptions.mappers.infra_errors import InfraErrorMapper
from shared.exceptions.mappers.s3_errors import S3ErrorCode
from transport.rest.dto.base import Response


def generate_infrastructure_responses(
    include_codes: set[S3ErrorCode | SQLAlchemyErrorCode] = set(  # noqa: B006
        list(SQLAlchemyErrorCode) + list(S3ErrorCode)
    ),  # noqa: B006
    exclude_codes: set[S3ErrorCode | SQLAlchemyErrorCode] | None = None,
) -> dict[Union[int, str], dict[str, Any]] | None:
    """
    Генерация responses для FastAPI на основе S3ErrorCode и SQLAlchemyErrorCode.

    - По умолчанию включены все ошибки.
    - Можно явно исключить через exclude_codes.
    """
    responses: dict[int, dict[str, Any]] = {}

    # Обрабатываем ошибки S3 и SQLAlchemy
    for error_code, description in {
        **InfraErrorMapper.get_code_to_message(),
        **InfraErrorMapper.get_code_to_message(),
    }.items():
        # Применяем фильтрацию
        if error_code not in include_codes:
            continue
        if exclude_codes and error_code in exclude_codes:
            continue

        # Получаем HTTP статус через маппер
        http_status = InfraErrorMapper.get_code_to_http_status().get(error_code, 500)

        # Чтобы не дублировать одинаковые коды
        if http_status not in responses:
            responses[http_status] = {
                "model": Response,
                "description": description,
                "content": {
                    "application/json": {
                        "example": {
                            "data": None,
                            "error": {"msg": description, "type": error_code.value},
                        }
                    },
                    "application/problem+json": {
                        "example": {
                            "type": f"https://example.com/problems/{error_code.value.lower()}",
                            "title": description,
                            "status": http_status,
                            "detail": description,
                            "instance": "/files/12345",
                        }
                    },
                },
            }

    return responses  # type: ignore


ALL_RESPONSES: dict[int | str, dict[str, Any]] | None = (
    generate_infrastructure_responses()
)
NON_SPECIFIED_RESPONSES: dict[int | str, dict[str, Any]] | None = (
    generate_infrastructure_responses(
        exclude_codes={
            S3ErrorCode.NO_SUCH_KEY,
            S3ErrorCode.NO_SUCH_BUCKET,
            SQLAlchemyErrorCode.NO_RESULT,
        }
    )
)
