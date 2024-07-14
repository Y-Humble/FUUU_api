from sqlalchemy import Result, Row, Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from apps.user.telegram.models import TelegramUser
from core.db import SQlAlchemyRepo


class TelegramUserRepo[TU: TelegramUser](SQlAlchemyRepo):
    _model: TU = TelegramUser

    @classmethod
    async def get_user_or_none(
        cls, session: AsyncSession, **filters
    ) -> Row | None:
        stmt: Select = (
            select(cls._model)
            .options(joinedload(cls._model.user))
            .filter_by(**filters)
        )
        result: Result = await session.execute(stmt)
        row = result.scalars().one_or_none()
        return row
