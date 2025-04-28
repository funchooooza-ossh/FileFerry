from fastapi import APIRouter, File, Form, Query, UploadFile
from fastapi.responses import StreamingResponse

from composition.di import AdapterDI
from shared.io.upload_stream import file_to_iterator
from transport.rest.dependencies import BucketDI
from transport.rest.dto.base import Response
from transport.rest.dto.models import DeleteFileResponse, UploadFileResponse

file_router = APIRouter(prefix="/files")


@file_router.post("/upload")
async def upload_file(
    adapter: AdapterDI,
    bucket: BucketDI,
    file: UploadFile = File(...),
    name: str = Form(...),
) -> Response[UploadFileResponse]:
    stream = file_to_iterator(file=file)
    meta = await adapter.upload(name=name, stream=stream, bucket=bucket)
    data = UploadFileResponse.from_domain(meta)

    return Response[UploadFileResponse].success(data)


@file_router.get("/retrieve")
async def retrieve_file(
    adapter: AdapterDI, bucket: BucketDI, file_id: str = Query(..., alias="file_id")
) -> StreamingResponse:
    meta, stream = await adapter.retrieve(file_id=file_id, bucket=bucket)
    return StreamingResponse(
        content=stream,
        media_type=meta.content_type.value,
        headers={
            "X-Filename": meta.name.value,
            "X-FileSize": str(meta.size.value),
            "X-FileID": meta.id.value,
        },
    )


@file_router.post("/delete")
async def delete_file(
    adapter: AdapterDI, bucket: BucketDI, file_id: str = Query(..., alias="file_id")
) -> Response[DeleteFileResponse]:
    await adapter.delete(file_id=file_id, bucket=bucket)
    return Response[DeleteFileResponse].success(data=DeleteFileResponse.success())
