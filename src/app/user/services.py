from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.user.models import User
from app.user.exceptions import (
    EmptyCredentialsException,
    InvalidCredentialsException,
    UserExistException,
    UserNotFoundException,
)
from app.user.repositories import UserRepo
from app.user.schemas import (
    UserCreate,
    UserCreateDB,
    UserSchema,
    UserUpdate,
    UserUpdateDB,
)
from app.user.utils import hash_password, is_valid_password


class UserService:
    @classmethod
    async def register_new_user(
        cls, session: AsyncSession, user: UserCreate
    ) -> UserSchema:
        """
        Add user to database
        :return: UserSchema(
            id: UUID,
            username: str MaxLen(32)
            email: EmailStr
            active: bool
            status: Status("admin", "enjoyer", "banned")
        """

        if await UserRepo.get_one_or_none(session, email=user.email):
            raise UserExistException

        schema: UserCreateDB = UserCreateDB(
            **user.model_dump(),
            hashed_password=hash_password(user.password),
        )
        db_user: User = await UserRepo.add_one(
            session,
            **schema.model_dump(),
        )
        return UserSchema.model_validate(db_user)

    @classmethod
    async def authenticate_user(
        cls,
        session: AsyncSession,
        password: str,
        username: str | None = None,
        email: str | None = None,
    ) -> UserSchema:
        """
        Get User from database, check password, check that user is active
        :return: UserSchema(
            id: UUID,
            username: Annotated[str, MaxLen(32)]
            email: EmailStr | None = None
            active: bool
            status: Status("admin", "enjoyer", "banned")
        )
        """
        filters: dict[str, str] = {}
        if username is not None:
            filters.update({"username": username})
        elif email is not None:
            filters.update({"email": email})
        else:
            raise EmptyCredentialsException

        if user := await UserRepo.get_one_or_none(session, **filters):
            if is_valid_password(password, user.hashed_password):
                if user.active:
                    return UserSchema.model_validate(user)
        raise InvalidCredentialsException

    @classmethod
    async def _get_user(cls, session: AsyncSession, user_id: UUID) -> User:
        if db_user := await UserRepo.get_one_or_none(session, id=user_id):
            return db_user
        raise UserNotFoundException

    @classmethod
    async def update_user(
        cls, session: AsyncSession, user_id: UUID, user_data: UserUpdate
    ) -> UserSchema:
        db_user: User = await cls._get_user(session, user_id)
        if user_data.password:
            user_in: UserUpdateDB = UserUpdateDB(
                **user_data.model_dump(exclude_unset=True),
                hashed_password=hash_password(user_data.password),
            )
        else:
            user_in: UserUpdateDB = UserUpdateDB(**user_data.model_dump())

        user_update: User = await UserRepo.update_one(
            session, db_user, **user_in.model_dump()
        )
        updated_user: UserSchema = UserSchema.model_validate(user_update)

        return updated_user

    @classmethod
    async def delete_user(cls, session: AsyncSession, user_id: UUID) -> None:
        db_user: User = await cls._get_user(session, user_id)
        await UserRepo.update_one(session, db_user, active=False)
