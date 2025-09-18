from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from .routers import router as api_router
from .security import limit_body_size
from .auth import basic_auth_guard
from .retrieval import BaseRetrieval
from .logging_sqlite import log_chat


REQUEST_COUNTER = Counter("http_requests_total", "Total HTTP requests", ["path", "method", "status"])
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "HTTP request latency", ["path", "method"])


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        import time

        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        path = request.url.path
        method = request.method
        try:
            REQUEST_COUNTER.labels(path=path, method=method, status=str(response.status_code)).inc()
            REQUEST_LATENCY.labels(path=path, method=method).observe(elapsed)
        except Exception:
            pass
        return response


def create_app() -> FastAPI:
    app = FastAPI(title="Torob Turbo Assistant")

    app.add_middleware(MetricsMiddleware)
    app.middleware("http")(limit_body_size)
    app.middleware("http")(basic_auth_guard)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=False,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/metrics")
    async def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    app.include_router(api_router)

    # attach retrieval and logger to app state
    @app.on_event("startup")
    async def _startup():
        app.state.retrieval = BaseRetrieval()
        app.state.log_chat = log_chat
    return app


app = create_app()


