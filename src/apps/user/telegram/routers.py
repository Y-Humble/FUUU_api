from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.sidekick import db_sidekick
from apps.user.telegram.schemas import TgUserCreate
from apps.user.telegram.services import TelegramUserService

router: APIRouter = APIRouter(prefix="/tg", tags=["Telegram User"])


@router.get("/id/{tg_id}")
async def get_tg_user_by_tg_id(
    tg_id: int,
    session: AsyncSession = Depends(db_sidekick.session_getter),
):
    """Get tg_id and email of user or None"""
    return await TelegramUserService.get_user_by_tg_id(session, tg_id)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_tg_user(
    tg_user: TgUserCreate,
    session: AsyncSession = Depends(db_sidekick.session_getter),
):
    """Add new user with telegram id and email"""
    return await TelegramUserService.register_new_tg_user(session, tg_user)
