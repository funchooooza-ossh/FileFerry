from fastapi import APIRouter, File, Form, UploadFile

from composition.di import AdapterDI
from shared.io.upload_stream import file_to_iterator
from transport.rest.dependencies import BucketDI
from transport.rest.dto.base import Response
from transport.rest.dto.models import UploadFileResponse

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
