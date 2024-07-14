from functools import lru_cache
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from core.admin import setup_admin
from core.config import settings
from core.lifespan import lifespan
from apps.user import user_router
from apps.meme import meme_router


@lru_cache(maxsize=1)
def setup_app() -> FastAPI:
    """Set functionality for API"""

    app: FastAPI = FastAPI(
        default_response_class=ORJSONResponse,
        title=settings.run.app_title,
        lifespan=lifespan,
        settings=settings,
    )
    admin: Admin = setup_admin(app)

    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=True,
        allow_methods=settings.cors.methods,
        allow_headers=settings.cors.headers,
    )

    app.include_router(router=user_router)
    app.include_router(router=meme_router)

    return app
