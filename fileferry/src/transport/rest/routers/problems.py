from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

from shared.exceptions.mappers.infra_errors import (
    InfrastructureErrorCode,
    InfrastructureErrorMapper,
    map_code_to_http_status,
)

problem_router = APIRouter(prefix="/problems")


@problem_router.get(
    "/{error_code}", tags=["Problems"], summary="Problem Details by Error Code"
)
async def problem_detail(error_code: str, request: Request):  # noqa: ANN201
    """
    Возвращает описание проблемы по коду ошибки.
    """
    normalized_error_code = error_code.lower()

    # Пытаемся найти в InfrastructureErrorCode
    matching_code = next(
        (
            code
            for code in InfrastructureErrorCode
            if code.value.lower() == normalized_error_code
        ),
        None,
    )

    if not matching_code:
        return JSONResponse(
            status_code=404,
            content={
                "type": f"https://example.com/problems/{normalized_error_code}",
                "title": "Unknown Problem",
                "status": 404,
                "detail": "Problem type not recognized.",
                "instance": str(request.url.path),
            },
        )

    description = InfrastructureErrorMapper._code_to_message.get(matching_code, "Неизвестная ошибка инфраструктуры.")  # type: ignore
    status_code = map_code_to_http_status(matching_code)

    accept = request.headers.get("accept", "")

    if "text/html" in accept:
        # HTML для браузеров
        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head><title>{description}</title></head>
            <body>
                <h1>{description}</h1>
                <p><strong>Код ошибки:</strong> {matching_code.value}</p>
                <p><strong>Статус HTTP:</strong> {status_code}</p>
            </body>
            </html>
        """,
            status_code=status_code,
        )

    # JSON для API клиентов
    return JSONResponse(
        status_code=status_code,
        content={
            "type": f"https://example.com/problems/{normalized_error_code}",
            "title": description,
            "status": status_code,
            "detail": description,
            "instance": str(request.url.path),
        },
    )
