from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from infrastructure.exceptions.mappers.infra_errors import InfraErrorMapper

problem_router = APIRouter(prefix="/problems")


@problem_router.get(
    "/{error_code}", tags=["Problems"], summary="Problem Details by Error Code"
)
async def problem_detail(error_code: str, request: Request) -> JSONResponse:
    """
    Возвращает описание проблемы по коду ошибки.
    """
    normalized_code = error_code.lower()
    if "error" not in normalized_code:
        normalized_code = normalized_code + "error"
    matching_code = next(
        (
            code
            for code in InfraErrorMapper.get_str_type_to_code()
            if code.lower() == normalized_code
        ),
        "Unknown",  # Если не найдено, возвращаем None
    )
    matching_code = InfraErrorMapper.get_str_type_to_code().get(matching_code)
    if not matching_code:
        return JSONResponse(
            status_code=404,
            content={
                "type": "https://http.cat/404",
                "title": "Undocummented error",
                "status": 404,
                "detail": "Unknown error",
                "instance": None,  # Примерно указываем путь запроса, если нужно
            },
        )
    message = InfraErrorMapper.get_code_to_message().get(matching_code)
    status = InfraErrorMapper.get_code_to_http_status().get(matching_code, 500)
    return JSONResponse(
        status_code=status,
        content={
            "type": f"https://http.cat/{status}",
            "title": matching_code.value,
            "status": status,
            "detail": message,
            "instance": None,  # Примерно указываем путь запроса, если нужно
        },
    )
