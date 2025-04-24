from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import StreamingResponse

from api.rest.di_context import make_di_resolver
from api.rest.docs.file_create import create_file_responses
from api.rest.docs.file_retrieve import retrieve_file_responses
from api.rest.schemas.models import UploadFileResponse
from api.rest.schemas.requests import FileRetrieve
from api.rest.schemas.responses import Response
from api.rest.utils.handler import api_response
from contracts.composition import FileAPIAdapterContract
from shared.io.upload_stream import file_to_iterator

file_router = APIRouter()


@file_router.post(
    "/create",
    tags=["files"],
    response_model=Response[UploadFileResponse],
    responses=create_file_responses,
)
@api_response(expected_type=UploadFileResponse)
async def create_file(
    service: Annotated[FileAPIAdapterContract, Depends(make_di_resolver("upload"))],
    file: Annotated[UploadFile, File()],
    name: Annotated[str, Form()],
) -> UploadFileResponse:
    stream = file_to_iterator(file)
    result = await service.create(name=name, stream=stream)
    return UploadFileResponse.from_domain(result)


@file_router.post("/retrieve", tags=["files"], responses=retrieve_file_responses)
@api_response(expected_type=None)
async def retrieve_file(
    service: Annotated[FileAPIAdapterContract, Depends(make_di_resolver("retrieve"))],
    request: FileRetrieve,
) -> StreamingResponse:
    meta, stream = await service.get(file_id=request.file_id)
    return StreamingResponse(
        content=stream,
        media_type=meta.content_type.value,
        headers={
            "X-Filename": meta.name.value,
            "X-FileSize": str(meta.size.value),
            "X-FileId": meta.id.value,
        },
    )
