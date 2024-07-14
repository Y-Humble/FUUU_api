from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.user.admin.schemas import UserUpdateAdmin
from core.db.sidekick import db_sidekick
from apps.user.dependencies import get_user_admin
from apps.user.messages import UserResponseMessage
from apps.user.schemas import UserSchema
from apps.user.admin.services import AdminService

router: APIRouter = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_user_admin)],
)


@router.get("/list")
async def get_users_list(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> list[UserSchema]:
    """Get users as Admin"""
    return await AdminService.get_users_list(
        session, offset=offset, limit=limit
    )


@router.post("/ban")
async def ban_user(
    user_id: str,
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> dict[str, str]:
    """Set ban for user"""
    await AdminService.ban_user(session, UUID(user_id))
    return UserResponseMessage.BANNED_USER


@router.get("/user-username/{username}")
async def get_user_by_username(
    username: str,
    session: AsyncSession = Depends(db_sidekick.session_getter),
):
    """Get user by username"""
    return await AdminService.get_user_by_username(session, username)


@router.get("/user-email/{email}")
async def get_user_by_email(
    email: str,
    session: AsyncSession = Depends(db_sidekick.session_getter),
):
    """Get user by email"""
    return await AdminService.get_user_by_email(session, email)


@router.get("/user/{user_id}")
async def get_user_by_id(
    user_id: str,
    session: AsyncSession = Depends(db_sidekick.session_getter),
):
    """Get user by id"""
    return await AdminService.get_user(session, UUID(user_id))


@router.put("/user/{user_id}")
async def update_user(
    user_id: str,
    user_update: UserUpdateAdmin,
    session: AsyncSession = Depends(db_sidekick.session_getter),
):
    """Update user as Admin"""
    return await AdminService.update_user(
        session,
        UUID(user_id),
        user_update,
    )


@router.delete("/user/{user_id}")
async def delete_user(
    user_id: str,
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> dict[str, str]:
    """Delete user as Admin"""
    await AdminService.delete_user(session, UUID(user_id))
    return UserResponseMessage.DELETED_USER
