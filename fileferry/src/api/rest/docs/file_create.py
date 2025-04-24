from starlette import status

from api.rest.schemas.models import UploadFileResponse
from api.rest.schemas.responses import Error, Response

create_file_responses = {
    status.HTTP_200_OK: {
        "model": Response[UploadFileResponse],
        "description": "Файл успешно загружен",
        "content": {
            "application/json": {
                "example": {
                    "data": {"id": "abc123", "name": "example.png"},
                    "error": None,
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": Response[Error],
        "description": "Неверные параметры запроса или некорректное имя bucket",
        "content": {
            "application/json": {
                "example": {
                    "data": None,
                    "error": {
                        "msg": "Имя bucket недопустимо.",
                        "type": "INVALID_BUCKET_NAME",
                    },
                }
            }
        },
    },
    status.HTTP_409_CONFLICT: {
        "model": Response[Error],
        "description": "Конфликт в базе данных (нарушение ограничений)",
        "content": {
            "application/json": {
                "example": {
                    "data": None,
                    "error": {
                        "msg": "Нарушение ограничений целостности БД.",
                        "type": "REPO_INTEGRITY",
                    },
                }
            }
        },
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": Response[Error],
        "description": "Файл отклонён по политике",
        "content": {
            "application/json": {
                "example": {
                    "data": None,
                    "error": {
                        "msg": "File rejected by policy",
                        "type": "FilePolicyViolationEror",
                    },
                }
            }
        },
    },
    status.HTTP_502_BAD_GATEWAY: {
        "model": Response[Error],
        "description": "Ошибка взаимодействия с хранилищем",
        "content": {
            "application/json": {
                "example": {
                    "data": None,
                    "error": {
                        "msg": "Ошибка взаимодействия с хранилищем.",
                        "type": "STORAGE",
                    },
                }
            }
        },
    },
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        "model": Response[Error],
        "description": "База данных недоступна",
        "content": {
            "application/json": {
                "example": {
                    "data": None,
                    "error": {
                        "msg": "Ошибка соединения или таймаут при работе с БД.",
                        "type": "REPO_OPERATIONAL",
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": Response[Error],
        "description": "Внутренняя ошибка сервиса",
        "content": {
            "application/json": {
                "example": {
                    "data": None,
                    "error": {
                        "msg": "Низкоуровневая инфраструктурная ошибка.",
                        "type": "INFRA",
                    },
                }
            }
        },
    },
}
