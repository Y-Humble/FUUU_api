from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .messages import TemplateResponseMessage
from .schemas import (
    MemeTemplateUpdate,
    MemeTemplateUpdatePartial,
    MemeTemplateResponse,
)
from core.db import db_sidekick
from core.cache import CacheData, check_template_cache
from apps.user.dependencies import get_user_admin
from apps.user.schemas import UserSchema
from apps.meme.templates.services import MemeTemplateService
from apps.meme.templates.models import MemeTemplate


router: APIRouter = APIRouter(prefix="/template", tags=["Templates"])


@router.get("/list", response_model_exclude={"path"})
async def get_images(
    session: AsyncSession = Depends(db_sidekick.session_getter),
    offset: int = 0,
    limit: int = 100,
    category: str | None = None,
) -> list:
    filter_by: dict[str, str] = {"category": category} if category else {}
    return await MemeTemplateService.get(
        session=session, offset=offset, limit=limit, **filter_by
    )


@router.get("/categories")
async def get_categories(
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> list[str]:
    return await MemeTemplateService.get_categories(session=session)


@router.get("/{img_id}", response_class=FileResponse)
async def get_one_image(
    img_id: int, session: AsyncSession = Depends(db_sidekick.session_getter)
) -> FileResponse:
    cache_data: CacheData = CacheData[MemeTemplateService](
        key=str(img_id),
        model_id=img_id,
        session=session,
        service=MemeTemplateService,
    )
    img: MemeTemplateResponse = await check_template_cache(
        cache_data, MemeTemplateResponse.model_validate
    )
    return FileResponse(img.path, media_type="image/jpeg")


@router.post("", status_code=201)
async def post_image(
    image: UploadFile,
    title: str = Form(f"image-{uuid4()}.jpg"),
    category: str = Form("other"),
    admin: UserSchema = Depends(get_user_admin),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> dict[str, str | int]:
    result: MemeTemplate = await MemeTemplateService.add_one(
        session=session, image=image, title=title, category=category
    )
    return {"template": result.title, "category": result.category}


@router.put("/{img_id}", response_model_exclude={"path"})
async def update_image(
    img_id: int,
    img_data: MemeTemplateUpdate,
    admin: UserSchema = Depends(get_user_admin),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> MemeTemplateResponse:
    return await MemeTemplateService.update_one(
        session=session, img_id=img_id, **img_data.model_dump()
    )


@router.patch("/{img_id}", response_model_exclude={"path"})
async def update_image_partial(
    img_id: int,
    img_data: MemeTemplateUpdatePartial,
    admin: UserSchema = Depends(get_user_admin),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> MemeTemplateResponse:
    return await MemeTemplateService.update_one(
        session=session,
        img_id=img_id,
        **img_data.model_dump(exclude_unset=True),
    )


@router.delete("/{img_id}")
async def delete_image(
    img_id: int,
    admin: UserSchema = Depends(get_user_admin),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> dict[str, str]:
    await MemeTemplateService.delete_one(session, img_id)
    return TemplateResponseMessage.DELETED_TEMPLATE
