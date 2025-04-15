from fastapi import FastAPI, Form, UploadFile, File
from application.services.file import ApplicationFileService

app = FastAPI()


@app.post("/test")
async def create_file(name: str = Form(...), file: UploadFile = File(...)):
    return await ApplicationFileService.create_file(name=name, file=file)
