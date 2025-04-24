from starlette import status

from api.rest.schemas.responses import Error, Response

retrieve_file_responses = {
    status.HTTP_200_OK: {
        "description": "Файл успешно возвращён как поток",
        "content": {"application/octet-stream": {"example": b"binary file content"}},
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": Response[Error],
        "description": "Некорректный ID файла или имя bucket",
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
    status.HTTP_404_NOT_FOUND: {
        "model": Response[Error],
        "description": "Файл не найден в хранилище или базе данных",
        "content": {
            "application/json": {
                "example": {
                    "data": None,
                    "error": {
                        "msg": "Файл не найден в хранилище.",
                        "type": "STORAGE_NOT_FOUND",
                    },
                }
            }
        },
    },
    status.HTTP_502_BAD_GATEWAY: {
        "model": Response[Error],
        "description": "Ошибка получения файла из хранилища",
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
