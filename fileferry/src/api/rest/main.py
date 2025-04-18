from fastapi import FastAPI

from api.rest.routers.root import root_router

app = FastAPI()

app.include_router(router=root_router)
