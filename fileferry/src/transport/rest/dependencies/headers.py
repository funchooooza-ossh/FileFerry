from typing import Annotated

from fastapi import Depends, Header, HTTPException

from shared.enums import Buckets


def extract_bucket_from_headers(
    bucket: str = Header(
        ...,
        alias="X-Bucket",
    ),
) -> Buckets:
    try:
        return Buckets(bucket)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid bucket value") from None


BucketDI = Annotated[Buckets, Depends(extract_bucket_from_headers)]
