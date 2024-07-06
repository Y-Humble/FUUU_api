from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_sidekick
from user.schemas import UserCreate, UserSchema
from user.services import UserService

router: APIRouter = APIRouter(prefix="/user", tags=["User"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_new_user(
    user: UserCreate,
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> UserSchema:
    """New user registration"""
    return await UserService.register_new_user(session, user)
