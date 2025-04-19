from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from loguru import logger
from pydantic import ValidationError

from api.rest.schemas.models import UploadFileResponse
from api.rest.schemas.responses import Error, Response
from application.di.bootstrap.upload_minio_sqla import bootstrap_minio_sqla_upload
from application.services.file import ApplicationFileService
from shared.exceptions.application import DomainRejectedError, StatusFailedError
from shared.io.upload_stream import file_to_iterator

file_router = APIRouter()


@file_router.post("/create", tags=["files"])
async def create_file(
    file: Annotated[UploadFile, File()] = ...,
    name: Annotated[str, Form()] = ...,
    service: Annotated[ApplicationFileService, Depends(bootstrap_minio_sqla_upload)] = ...,
) -> Response[UploadFileResponse]:
    error = None
    data = None
    stream = file_to_iterator(file)
    try:
        data = await service.create_file(name=name, stream=stream)
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

    return Response[UploadFileResponse](data=data, error=error)
