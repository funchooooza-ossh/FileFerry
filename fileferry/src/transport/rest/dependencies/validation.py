from typing import Annotated

from fastapi import Depends, Form, HTTPException, Path, Query, Request
from loguru import logger

from domain.models import FileId, FileName

logger = logger.bind(name="requests")


def filename_formdata(
    request: Request,
    name: str = Form(..., min_length=1, max_length=255, description="New file name"),
) -> FileName:
    try:
        return FileName(name)
    except ValueError:
        logger.warning("[REQUEST][ERROR] Validation error")
        raise HTTPException(status_code=400, detail="Invalid name value") from None


FormFilenameDI = Annotated[FileName, Depends(filename_formdata)]


def file_id_from_path(
    request: Request,
    file_id: str = Path(..., alias="file_id", description="Unique file identifier"),
) -> FileId:
    try:
        return FileId(file_id)
    except ValueError:
        logger.warning("[REQUEST][ERROR] Validation error")
        raise HTTPException(status_code=400, detail="Invalid id value") from None


PathFileIdDI = Annotated[FileId, Depends(file_id_from_path)]


def filename_from_query(
    request: Request,
    name: str = Query(
        ..., min_length=1, max_length=255, description="Original file name"
    ),
) -> FileName:
    try:
        return FileName(name)
    except ValueError:
        logger.warning("[REQUEST][ERROR] Validation error")
        raise HTTPException(status_code=400, detail="Invalid name value") from None


QueryFilenameDI = Annotated[FileName, Depends(filename_from_query)]
