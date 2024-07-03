import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.lifespan import lifespan


def app() -> FastAPI:
    """Set functionality for API"""

    app: FastAPI = FastAPI(
        title=settings.run.app_title,
        lifespan=lifespan,
        settings=settings,
    )

    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=True,
        allow_methods=settings.cors.methods,
        allow_headers=settings.cors.headers,
    )

    return app


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        factory=True,
    )
