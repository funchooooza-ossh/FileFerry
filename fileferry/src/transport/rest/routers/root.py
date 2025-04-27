from fastapi import APIRouter

from transport.rest.routers.files import file_router

root_router = APIRouter()
root_router.include_router(file_router)
