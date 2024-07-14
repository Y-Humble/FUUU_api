from sqlalchemy.ext.asyncio import AsyncSession

from apps.user.exceptions import UserExistException
from apps.user.repositories import UserRepo
from apps.user.schemas import UserCreateDB
from apps.user.telegram.repositories import TelegramUserRepo
from apps.user.telegram.schemas import TgUserCreate, TgUserSchema
from apps.user.utils import hash_password


class TelegramUserService:
    _repository = TelegramUserRepo
    _create_model = TgUserCreate
    _response_model = TgUserSchema

    @classmethod
    async def register_new_tg_user(
        cls, session: AsyncSession, user: TgUserCreate
    ):
        if await cls._repository.get_one_or_none(session, tg_id=user.tg_id):
            raise UserExistException

        elif await UserRepo.get_one_or_none(session, email=user.user_email):
            await cls._repository.add_one(
                session=session,
                **user.model_dump(),
            )
        else:
            username = user.user_email.split("@")[0]
            schema = UserCreateDB(
                username=username,
                email=user.user_email,
                hashed_password=hash_password(user.password),
            )
            await UserRepo.add_one(
                session=session,
                **schema.model_dump(),
            )
            await cls._repository.add_one(
                session=session,
                **user.model_dump(
                    exclude={
                        "password",
                    }
                ),
            )

        return cls._response_model(**user.model_dump())

    @classmethod
    async def get_user_by_tg_id(cls, session: AsyncSession, tg_id: int):
        user = await cls._repository.get_user_or_none(session, tg_id=tg_id)
        return cls._response_model.model_validate(user)
