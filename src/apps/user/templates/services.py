from sqlalchemy.ext.asyncio import AsyncSession

from apps.services import TemplateServiceBase
from apps.user.templates.models import UserMemeTemplate
from apps.user.templates.repositories import UserTemplateRepo
from apps.user.templates.schemas import (
    UserTemplateBase,
    UserTemplateCreate,
    UserTemplateResponse,
)
from core.constants import Const


class UserTemplateService(TemplateServiceBase):
    _model: UserMemeTemplate = UserMemeTemplate
    _base_model: UserTemplateBase = UserTemplateBase
    _create_model: UserTemplateCreate = UserTemplateCreate
    _response_model: UserTemplateResponse = UserTemplateResponse
    _repository: UserTemplateRepo = UserTemplateRepo
    _path_to_templates = Const.USER_TEMPLATES_DIR

    @classmethod
    async def add_one(
        cls,
        session: AsyncSession,
        **data,
    ) -> UserTemplateResponse:
        user_id: str = str(data.get("user_id"))
        if cls._path_to_templates.name != user_id:
            cls._path_to_templates /= user_id

        return await super().add_one(session, **data)

    @classmethod
    async def update_one(
        cls, session: AsyncSession, img_id, **data
    ) -> UserTemplateResponse:
        user_id: str = str(data.get("user_id"))
        if cls._path_to_templates.name != user_id:
            cls._path_to_templates /= user_id

        return await super().update_one(session, img_id, **data)
