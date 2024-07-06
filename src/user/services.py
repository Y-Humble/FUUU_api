from sqlalchemy.ext.asyncio import AsyncSession

from user.models import User
from user.exceptions import UserExistException
from user.repositories import UserRepo
from user.schemas import UserCreate, UserCreateDB, UserSchema
from user.utils import hash_password


class UserService:
    @classmethod
    async def register_new_user(
        cls, session: AsyncSession, user: UserCreate
    ) -> UserSchema:
        """
        Add user to database
        :return: UserSchema(
            id: UUID,
            username: Annotated[str, MaxLen(32)]
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
