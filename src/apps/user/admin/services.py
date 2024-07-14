from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from apps.user.admin.schemas import UserUpdateAdmin
from apps.user.exceptions import UserNotFoundException, UsersNotFoundException
from apps.user.models import User, Status
from apps.user.repositories import UserRepo
from apps.user.schemas import UserSchema, UserUpdateDB
from apps.user.utils import hash_password
from apps.user.services import UserService


class AdminService(UserService):
    @classmethod
    async def get_users_list(
        cls,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        **filters,
    ) -> list[UserSchema]:
        users: list[User] = await UserRepo.get(
            session=session, offset=offset, limit=limit, **filters
        )
        if not users:
            raise UsersNotFoundException

        return [UserSchema.model_validate(db_user) for db_user in users]

    @classmethod
    async def get_user(cls, session: AsyncSession, user_id: UUID) -> User:
        return await cls._get_user(session, user_id)

    @classmethod
    async def get_user_by_username(
        cls, session: AsyncSession, username: str
    ) -> User:
        if db_user := await UserRepo.get_one_or_none(
            session, username=username
        ):
            return db_user
        raise UserNotFoundException

    @classmethod
    async def get_user_by_email(
        cls, session: AsyncSession, email: str
    ) -> User:
        if db_user := await UserRepo.get_one_or_none(session, email=email):
            return db_user
        raise UserNotFoundException

    @classmethod
    async def update_user(
        cls, session: AsyncSession, user_id: UUID, user_update: UserUpdateAdmin
    ) -> User:
        db_user: User = await cls._get_user(session, user_id)
        if user_update.password:
            user_in: UserUpdateDB = UserUpdateDB(
                **user_update.model_dump(exclude_unset=True),
                hashed_password=hash_password(user_update.password),
            )
        else:
            user_in: UserUpdateDB = UserUpdateDB(**user_update.model_dump())
        user_update: User = await UserRepo.update_one(
            session, db_user, **user_in.model_dump()
        )
        return user_update

    @classmethod
    async def delete_user(cls, session: AsyncSession, user_id: UUID) -> None:
        db_user: User = await cls._get_user(session, user_id)
        await UserRepo.delete_one(session, db_user)

    @classmethod
    async def ban_user(cls, session: AsyncSession, user_id: UUID) -> None:
        db_user: User = await cls._get_user(session, user_id)
        await UserRepo.update_one(session, db_user, status=Status.BANNED)
