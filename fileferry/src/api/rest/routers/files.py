from pydantic import ValidationError
from loguru import logger
from fastapi import APIRouter, Form, UploadFile, File
from application.services.file import ApplicationFileService
from shared.io.upload_stream import file_to_iterator
from api.rest.schemas.responses import Response, Error
from api.rest.schemas.models import UploadFileResponse
from shared.exceptions.application import DomainRejectedError, StatusFailedError

file_router = APIRouter()


@file_router.post("/create", tags=["files"])
async def create_file(
    file: UploadFile = File(...), name: str = Form(...)
) -> Response[UploadFileResponse]:
    error = None
    data = None
    stream = file_to_iterator(file)
    try:
        data = await ApplicationFileService.create_file(name=name, stream=stream)
        data = UploadFileResponse.from_domain(data)
    except ValidationError as exc:
        error = Error(msg="Incorrect result from service", type="Internal Server Error")
        logger.exception(f"Incorrect result from service: {exc}")
    except StatusFailedError as exc:
        logger.exception(f"Upload file failed: {exc.type}")
        error = Error(msg="Upload failed", type=exc.type)

    except DomainRejectedError as exc:
        logger.warning("Upload rejected")
        error = Error(msg="File rejected", type=exc.type)

    finally:
        return Response[UploadFileResponse](data=data, error=error)
