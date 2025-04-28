from collections.abc import Awaitable, Callable

from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response as StarletteResponse

from shared.exceptions.exc_classes.application import (
    ApplicationRunTimeError,
    DomainRejectedError,
    FileOperationFailed,
    InvalidFileParameters,
    InvalidValueError,
)
from shared.exceptions.mappers.infra_errors import InfraErrorMapper
from shared.exceptions.mappers.s3_errors import S3ErrorCode
from transport.rest.dto.base import Response


class ApplicationErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[StarletteResponse]],
    ) -> StarletteResponse:
        try:
            # Обрабатываем основной запрос
            response = await call_next(request)
            return response

        except DomainRejectedError as exc:
            # Обрабатываем ошибки доменных правил
            logger.warning(f"[DOMAIN] Ошибка доменных правил: {exc}")
            return self._create_json_response(
                status_code=400,
                msg="Not allowed data",
                error_type="Policy violation",
            )

        except (InvalidFileParameters, InvalidValueError) as exc:
            # Обрабатываем ошибки валидации
            logger.warning(f"[VALIDATION] Ошибка валидации: {exc}")
            return self._create_json_response(
                status_code=400,
                msg="Invalid data",
                error_type="Validation Error",
            )

        except ApplicationRunTimeError as exc:
            # Обрабатываем ошибки времени выполнения
            logger.exception(f"[CRITICAL] Нарушение логики работы: {exc}")
            return self._create_json_response(
                status_code=500,
                msg="Internal server Error",
                error_type="Runtime error",
            )

        except FileOperationFailed as exc:
            # Обрабатываем инфраструктурные ошибки
            logger.warning(f"[INFRA] Ошибка инфраструктуры: {exc}")
            return self._handle_infrastructure_error(exc, request)

    def _create_json_response(
        self, status_code: int, msg: str, error_type: str
    ) -> JSONResponse:
        """Универсальная функция для создания JSONResponse с ошибкой."""
        return JSONResponse(
            status_code=status_code,
            content=Response.failure(msg=msg, type=error_type).model_dump(),
            media_type="application/json",
        )

    def _handle_infrastructure_error(
        self, exc: FileOperationFailed, request: Request
    ) -> JSONResponse:
        """Обработка инфраструктурных ошибок с использованием InfraErrorMapper."""
        # Получаем код ошибки через InfraErrorMapper
        code = InfraErrorMapper.get_str_type_to_code().get(
            exc.type, S3ErrorCode.UNKNOWN
        )
        http_status = InfraErrorMapper.get_code_to_http_status().get(code, 400)
        message = InfraErrorMapper.get_code_to_message().get(code, "Unknown error")

        # Определяем формат ответа, основываясь на заголовке Accept
        if "application/problem+json" in request.headers.get("accept", ""):
            return JSONResponse(
                status_code=http_status,
                content={
                    "type": f"http://{request.base_url}/problems/{exc.type.lower()}",
                    "title": code.value,
                    "status": http_status,
                    "detail": message,
                    "instance": str(request.url.path),
                },
                media_type="application/problem+json",
            )
        else:
            return JSONResponse(
                status_code=http_status,
                content=Response.failure(msg=message, type=code.value).model_dump(),
                media_type="application/json",
            )
