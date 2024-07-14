import json
from fastapi import APIRouter, Depends, Response
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from apps.meme.templates import MemeTemplate
from apps.meme.exceptions import MemeNotFoundException
from apps.meme.maker import MemeMaker
from apps.meme.schemas import LinesInfo, Meme, Template, MemeURLResponse
from apps.meme.templates import MemeTemplateService, template_router
from apps.meme.templates.schemas import MemeTemplateResponse
from apps.user.dependencies import get_current_user
from apps.user.schemas import UserSchema
from apps.user.templates.services import UserTemplateService
from apps.user.templates.schemas import UserTemplateResponse
from core.cache import RedisCache
from core.config import settings
from core.db import db_sidekick

router: APIRouter = APIRouter(prefix="/meme", tags=["MEMES"])
router.include_router(template_router)


@router.post("", status_code=201)
async def create_meme(
    template: Template,
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> MemeURLResponse:
    text: int = sum(ord(i) for i in template.top_text + template.bottom_text)
    _key: str = f"{template.img_id}{text}"
    value_from_cache: str | None = await RedisCache.get(_key)

    if value_from_cache is None:
        img: MemeTemplate = await MemeTemplateService.get_one(
            session, template.img_id
        )
        meme: Meme = MemeMaker(img.path).create(
            template.top_text,
            template.bottom_text,
        )
        if err := await RedisCache.set(_key, meme.model_dump_json()):
            logger.error(err)

    return MemeURLResponse(
        meme_id=_key,
        url=f"{settings.run.url}{router.prefix}/{_key}",
    )


@router.post("/user/list", status_code=201)
async def create_user_list_memes(
    lines: LinesInfo,
    session: AsyncSession = Depends(db_sidekick.session_getter),
    offset: int = 0,
    limit: int = 100,
    category: str | None = None,
    current_user: UserSchema = Depends(get_current_user),
) -> list[MemeURLResponse]:
    filter_by: dict = {"category": category} if category else {}
    imgs: list[UserTemplateResponse] = await UserTemplateService.get(
        session=session, offset=offset, limit=limit, **filter_by
    )
    _keys: list[str] = []
    for img in imgs:
        concat: str = (
            lines.top_text + lines.bottom_text + current_user.username
        )
        _key: str = f"{img.id}{sum(ord(i) for i in concat)}"
        meme: Meme = MemeMaker(img.path).create(
            lines.top_text,
            lines.bottom_text,
        )
        if err := await RedisCache.set(_key, meme.model_dump_json()):
            logger.error(err)
        _keys.append(_key)

    return [
        MemeURLResponse(
            meme_id=key,
            url=rf"{settings.run.url}{router.prefix}/{key}",
        )
        for key in _keys
    ]


@router.post("/list", status_code=201)
async def create_list_memes(
    lines: LinesInfo,
    session: AsyncSession = Depends(db_sidekick.session_getter),
    offset: int = 0,
    limit: int = 100,
    category: str | None = None,
) -> list[MemeURLResponse]:
    filter_by: dict[str, str] = {"category": category} if category else {}
    imgs: list[MemeTemplateResponse] = await MemeTemplateService.get(
        session=session, offset=offset, limit=limit, **filter_by
    )
    _keys = []
    for img in imgs:
        text: int = sum(ord(i) for i in lines.top_text + lines.bottom_text)
        _key: str = f"{img.id}{text}"
        meme: Meme = MemeMaker(img.path).create(
            lines.top_text,
            lines.bottom_text,
        )
        if err := await RedisCache.set(_key, meme.model_dump_json()):
            logger.error(err)
        _keys.append(_key)

    return [
        MemeURLResponse(
            meme_id=key,
            url=rf"{settings.run.url}{router.prefix}/{key}",
        )
        for key in _keys
    ]


@router.get("/{title}")
async def get_meme(title: str) -> Response:
    meme = await RedisCache.get(title)

    if meme is None:
        raise MemeNotFoundException

    meme_str: dict = json.loads(meme.decode())
    meme: Meme = Meme.model_validate(meme_str)
    return Response(meme.image, media_type="image/jpeg")
