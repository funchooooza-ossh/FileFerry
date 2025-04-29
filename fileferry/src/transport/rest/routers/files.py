from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import StreamingResponse

from composition.di import AdapterDI
from shared.io.upload_stream import file_to_iterator
from transport.rest.dependencies import (
    BucketDI,
    FormFilenameDI,
    PathFileIdDI,
    QueryFilenameDI,
)
from transport.rest.docs.generate_docs import ALL_RESPONSES, NON_SPECIFIED_RESPONSES
from transport.rest.dto.base import Response
from transport.rest.dto.models import DeleteFileResponse, UploadFileResponse

file_router = APIRouter(prefix="/files")


@file_router.post(
    "/",
    response_model=Response[UploadFileResponse],
    status_code=201,
    summary="Upload a new file",
    description="Uploads a file into the specified bucket and returns its metadata.",
    tags=["rest"],
    responses=NON_SPECIFIED_RESPONSES,
)
async def upload_file(
    adapter: AdapterDI,
    bucket: BucketDI,
    name: FormFilenameDI,
    file: UploadFile = File(..., description="Binary file to be uploaded"),
) -> Response[UploadFileResponse]:
    stream = file_to_iterator(file=file)
    meta = await adapter.upload(name=name, stream=stream, bucket=bucket)
    data = UploadFileResponse.from_domain(meta)

    return Response[UploadFileResponse].success(data)


@file_router.get(
    "/{file_id}",
    response_class=StreamingResponse,
    summary="Retrieve a file",
    description="Streams a file from the storage by its ID.",
    tags=["rest"],
    responses=ALL_RESPONSES,
)
async def retrieve_file(
    adapter: AdapterDI,
    bucket: BucketDI,
    file_id: PathFileIdDI,
) -> StreamingResponse:
    meta, stream = await adapter.retrieve(file_id=file_id, bucket=bucket)
    return StreamingResponse(
        content=stream,
        media_type=meta.get_content_type(),
        headers={
            "X-Filename": meta.get_name(),
            "X-FileSize": str(meta.get_size()),
            "X-FileID": meta.get_id(),
        },
    )


@file_router.delete(
    "/{file_id}",
    response_model=Response[DeleteFileResponse],
    status_code=200,
    summary="Delete a file",
    description="Deletes a file from the storage by its ID.",
    tags=["rest"],
    responses=ALL_RESPONSES,
)
async def delete_file(
    adapter: AdapterDI,
    bucket: BucketDI,
    file_id: PathFileIdDI,
) -> Response[DeleteFileResponse]:
    await adapter.delete(file_id=file_id, bucket=bucket)
    return Response[DeleteFileResponse].success(data=DeleteFileResponse.success())


@file_router.patch(
    "/{file_id}",
    response_model=Response[UploadFileResponse],
    status_code=200,
    summary="Update a file",
    description="Updates file metadata or replaces file content.",
    tags=["rest"],
    responses=ALL_RESPONSES,
)
async def update_file(
    adapter: AdapterDI,
    name: FormFilenameDI,
    bucket: BucketDI,
    file_id: PathFileIdDI,
    file: UploadFile = File(
        None, description="New file content to replace the existing one"
    ),
) -> Response[UploadFileResponse]:
    stream = file_to_iterator(file) if file else None
    meta = await adapter.update(
        file_id=file_id, name=name, stream=stream, bucket=bucket
    )
    data = UploadFileResponse.from_domain(meta)
    return Response[UploadFileResponse].success(data)


@file_router.post(
    "/stream",
    response_model=Response[UploadFileResponse],
    status_code=201,
    summary="Upload a new file via streaming",
    description="Uploads a file to the storage via a streamed request and returns its metadata.",
    tags=["integration"],
    responses=NON_SPECIFIED_RESPONSES,
)
async def stream_upload(
    request: Request,
    adapter: AdapterDI,
    bucket: BucketDI,
    name: QueryFilenameDI,
) -> Response[UploadFileResponse]:
    stream = request.stream()
    meta = await adapter.upload(name=name, stream=stream, bucket=bucket)
    data = UploadFileResponse.from_domain(meta)
    return Response[UploadFileResponse].success(data)


@file_router.patch(
    "/{file_id}/stream",
    response_model=Response[UploadFileResponse],
    status_code=200,
    summary="Update file content via streaming",
    description="Updates the content of an existing file using a streamed request.",
    tags=["integration"],
    responses=ALL_RESPONSES,
)
async def stream_update(
    request: Request,
    adapter: AdapterDI,
    bucket: BucketDI,
    file_id: PathFileIdDI,
    name: QueryFilenameDI,
) -> Response[UploadFileResponse]:
    stream = request.stream()
    meta = await adapter.update(
        file_id=file_id, name=name, stream=stream, bucket=bucket
    )
    data = UploadFileResponse.from_domain(meta)
    return Response[UploadFileResponse].success(data)
