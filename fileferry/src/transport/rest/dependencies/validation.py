from typing import Annotated

from fastapi import Depends, Form, HTTPException, Path, Query

from domain.models import FileId, FileName


def filename_formdata(
    name: str = Form(..., min_length=1, max_length=255, description="New file name"),
) -> FileName:
    try:
        return FileName(name)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid name value") from None


FormFilenameDI = Annotated[FileName, Depends(filename_formdata)]


def file_id_from_path(
    file_id: str = Path(..., alias="file_id", description="Unique file identifier"),
) -> FileId:
    try:
        return FileId(file_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid id value") from None


PathFileIdDI = Annotated[FileId, Depends(file_id_from_path)]


def filename_from_query(
    name: str = Query(
        ..., min_length=1, max_length=255, description="Original file name"
    ),
) -> FileName:
    try:
        return FileName(name)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid name value") from None


QueryFilenameDI = Annotated[FileName, Depends(filename_from_query)]
