# type: ignore
from typing import Any

from shared.exceptions.mappers.infra_errors import (
    InfrastructureErrorCode,
    InfrastructureErrorMapper,
    map_code_to_http_status,
)
from transport.rest.dto.base import Response


def generate_infrastructure_responses(
    include_codes: set[InfrastructureErrorCode] = frozenset(InfrastructureErrorCode),
    exclude_codes: set[InfrastructureErrorCode] | None = None,
) -> dict[int | str, dict[str, Any]] | None:
    """
    Генерация responses для FastAPI на основе InfrastructureErrorCode.

    - По умолчанию включены все ошибки.
    - Можно явно исключить через exclude_codes.
    """
    responses: dict[int, dict] = {}

    for error_code, description in InfrastructureErrorMapper._code_to_message.items():
        # Применяем фильтрацию
        if error_code not in include_codes:
            continue
        if exclude_codes and error_code in exclude_codes:
            continue

        http_status = map_code_to_http_status(error_code)

        # Чтобы не дублировать одинаковые коды
        if http_status not in responses:
            responses[http_status] = {
                "model": Response[None],
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
    return responses


COMMON_RESPONSES: dict[int | str, dict[str, Any]] | None = (
    generate_infrastructure_responses()
)
