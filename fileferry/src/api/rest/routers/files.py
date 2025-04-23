from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from loguru import logger
from pydantic import ValidationError

from api.rest.context import make_di_resolver
from api.rest.schemas.models import UploadFileResponse
from api.rest.schemas.responses import Error, Response
from contracts.composition import FileAPIAdapterContract
from shared.exceptions.application import DomainRejectedError, FileRetrieveFailedError, FileUploadFailedError
from shared.io.upload_stream import file_to_iterator

file_router = APIRouter()


@file_router.post("/create", tags=["files"])
async def create_file(
    service: Annotated[FileAPIAdapterContract, Depends(make_di_resolver("upload"))] = ...,
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
        logger.warning(f"Incorrect result from service: {exc}")
    except FileUploadFailedError as exc:
        logger.warning(f"Upload file failed: {exc.type}")
        error = Error(msg="Upload failed", type=exc.type)

    except DomainRejectedError as exc:
        logger.warning("Upload rejected")
        error = Error(msg="File rejected", type=exc.type)

    return Response[UploadFileResponse](data=data, error=error)


@file_router.post("/retrieve", tags=["files"])
async def retrieve_file(
    service: Annotated[FileAPIAdapterContract, Depends(make_di_resolver("get"))] = ...,
    file_id: Annotated[str, Form()] = ...,
) -> StreamingResponse:
    try:
        meta, stream = await service.get(file_id=file_id)
    except FileRetrieveFailedError as exc:
        logger.warning(f"Retrieve file failed: {exc.type}")
        error = Error(msg="Retrieve Failed", type=exc.type)
        return Response(data=None, error=error)
    return StreamingResponse(
        content=stream,
        media_type=meta.content_type.value,
        headers={"X-Filename": meta.name.value, "X-FileSize": str(meta.size.value), "X-FileId": meta.id.value},
    )
