from base64 import b64decode
from fastapi import Request, HTTPException
from .config import BASIC_AUTH_ENABLE, BASIC_AUTH_USER, BASIC_AUTH_PASS


async def basic_auth_guard(request: Request, call_next):
    # bypass for health and metrics
    if request.url.path in ("/health", "/metrics"):
        return await call_next(request)

    if BASIC_AUTH_ENABLE and BASIC_AUTH_USER and BASIC_AUTH_PASS:
        auth = request.headers.get("authorization")
        if not auth or not auth.lower().startswith("basic "):
            raise HTTPException(status_code=401, detail="auth required")
        try:
            raw = b64decode(auth.split(" ", 1)[1]).decode("utf-8")
            user, pwd = raw.split(":", 1)
        except Exception:
            raise HTTPException(status_code=401, detail="invalid auth")
        if user != BASIC_AUTH_USER or pwd != BASIC_AUTH_PASS:
            raise HTTPException(status_code=401, detail="invalid credentials")
    return await call_next(request)


