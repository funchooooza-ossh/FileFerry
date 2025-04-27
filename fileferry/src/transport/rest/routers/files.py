# from dependency_injector.wiring import Provide, inject
# from fastapi import APIRouter, Depends, File, Form, UploadFile

# from application.adapter import FileApplicationAdapter
# from composition.containers.application import ApplicationContainer
# from shared.io.upload_stream import file_to_iterator

# file_router = APIRouter(prefix="/files")


# @file_router.post("/upload")
# @inject
# async def upload_file(
#     file: UploadFile = File(...),
#     name: str = Form(...),
#     adapter: FileApplicationAdapter = Depends(
#         Provide[ApplicationContainer.adapters.file_application_adapter]
#     ),
# ):
#     stream = file_to_iterator(file=file)
#     meta = await adapter.upload(name=name, stream=stream, bucket="default-bucket")
#     return {
#         "file_id": meta.id.value,
#         "filename": meta.name.value,
#         "content_type": meta.content_type.value,
#         "size": meta.size.value,
#     }
