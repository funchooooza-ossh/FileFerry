from fastapi import APIRouter
from api.rest.routers.files import file_router


root_router = APIRouter(prefix="/api/v1")

root_router.include_router(router=file_router, prefix="/files")
