from typing import Iterable
from sqlalchemy import Select, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import SQlAlchemyRepo
from apps.meme.templates import MemeTemplate


class MemeTemplateRepo[MT: MemeTemplate](SQlAlchemyRepo):
    _model: MT = MemeTemplate

    @classmethod
    async def get_categories(cls, session: AsyncSession) -> list[str]:
        stmt: Select = select(cls._model.category).distinct()
        result: Result = await session.execute(stmt)
        rows: Iterable = result.scalars().all()
        return list(rows)
