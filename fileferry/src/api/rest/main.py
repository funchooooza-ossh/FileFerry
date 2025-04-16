from fastapi import FastAPI, Form, UploadFile, File
from application.services.file import ApplicationFileService
from shared.io.upload_stream import file_to_iterator

app = FastAPI()


@app.post("/test")
async def create_file(name: str = Form(...), file: UploadFile = File(...)):
    stream = file_to_iterator(file)
    return await ApplicationFileService.create_file(name=name, stream=stream)
