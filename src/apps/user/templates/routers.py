from uuid import uuid4
from fastapi import APIRouter, Depends, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import FileResponse

from core.db import db_sidekick
from core.cache import CacheData, check_template_cache
from apps.user.dependencies import get_current_user
from apps.user.schemas import UserSchema
from apps.user.templates.schemas import (
    UserTemplateResponse,
    UserTemplateUpdate,
    UserTemplateUpdatePartial,
)
from apps.user.templates.services import UserTemplateService

router: APIRouter = APIRouter(prefix="/template", tags=["User templates"])


@router.get("/list")
async def get_user_images(
    session: AsyncSession = Depends(db_sidekick.session_getter),
    offset: int = 0,
    limit: int = 100,
    category: str | None = None,
    current_user: UserSchema = Depends(get_current_user),
) -> list[UserTemplateResponse]:
    filter_by: dict = {"category": category} if category else {}
    return await UserTemplateService.get(
        session=session, offset=offset, limit=limit, **filter_by
    )


@router.get("/{img_id}", response_class=FileResponse)
async def get_one_user_image(
    img_id: int,
    # current_user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> FileResponse:
    cache_data: CacheData[UserTemplateService] = CacheData(
        key="user-" + str(img_id),
        model_id=img_id,
        session=session,
        service=UserTemplateService,
    )
    img: UserTemplateResponse = await check_template_cache(
        cache_data, UserTemplateResponse.model_validate
    )
    return FileResponse(img.path, media_type="image/jpeg")


@router.post("", status_code=201)
async def post_user_image(
    image: UploadFile,
    title: str = Form(f"image-{uuid4()}.jpg"),
    category: str = Form("other"),
    current_user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> dict[str, str | int]:
    result: UserTemplateResponse = await UserTemplateService.add_one(
        session=session,
        image=image,
        title=title,
        category=category,
        user_id=current_user.id,
    )
    return {
        "template": result.title,
        "category": result.category,
        "id": result.id,
    }


@router.put("/{img_id}")
async def update_user_image(
    img_id: int,
    img_data: UserTemplateUpdate,
    current_user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> UserTemplateResponse:
    return await UserTemplateService.update_one(
        session=session,
        img_id=img_id,
        user_id=current_user.id,
        **img_data.model_dump(),
    )


@router.patch("/{img_id}")
async def update_user_image_partial(
    img_id: int,
    img_data: UserTemplateUpdatePartial,
    current_user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> UserTemplateResponse:
    return await UserTemplateService.update_one(
        session=session,
        img_id=img_id,
        user_id=current_user.id,
        **img_data.model_dump(exclude_unset=True),
    )


@router.delete("/{img_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_image(
    img_id: int,
    current_user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> None:
    await UserTemplateService.delete_one(session, img_id)
