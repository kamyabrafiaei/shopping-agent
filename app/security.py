from fastapi import Request
from fastapi import HTTPException


MAX_BODY_BYTES = 1_000_000  # ~1MB


async def limit_body_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length is not None:
        try:
            if int(content_length) > MAX_BODY_BYTES:
                raise HTTPException(status_code=413, detail="payload too large")
        except ValueError:
            pass

    if request.method in {"POST", "PUT", "PATCH"} and content_length is None:
        body = await request.body()
        if len(body) > MAX_BODY_BYTES:
            raise HTTPException(status_code=413, detail="payload too large")
    return await call_next(request)


