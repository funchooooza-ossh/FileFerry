from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from loguru import logger
from pydantic import ValidationError

from api.rest.context import ApplicationDI
from api.rest.schemas.models import UploadFileResponse
from api.rest.schemas.responses import Error, Response
from shared.exceptions.application import DomainRejectedError, StatusFailedError
from shared.io.upload_stream import file_to_iterator

file_router = APIRouter()


@file_router.post("/create", tags=["files"])
async def create_file(
    service: ApplicationDI,
    file: Annotated[UploadFile, File()] = ...,
    name: Annotated[str, Form()] = ...,
) -> Response[UploadFileResponse]:
    error = None
    data = None
    stream = file_to_iterator(file)
    try:
        data = await service.create(name=name, stream=stream)
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


@file_router.post("/retrieve", tags=["files"])
async def retrieve_file(
    service: ApplicationDI,
    file_id: Annotated[str, Form()] = ...,
) -> StreamingResponse:
    meta, stream = await service.get(file_id=file_id)

    return StreamingResponse(
        content=stream,
        media_type=meta.content_type.value,
        headers={"X-Filename": meta.name.value, "X-FileSize": str(meta.size.value), "X-FileId": meta.id.value},
    )
