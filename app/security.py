from fastapi import Request


MAX_BODY_BYTES = 1_000_000  # ~1MB


async def limit_body_size(request: Request):
    body = await request.body()
    if len(body) > MAX_BODY_BYTES:
        from fastapi import HTTPException

        raise HTTPException(status_code=413, detail="payload too large")


