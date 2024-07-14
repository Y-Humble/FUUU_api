from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.services import TemplateServiceBase
from apps.meme.templates.models import MemeTemplate
from apps.meme.templates.repositories import MemeTemplateRepo
from apps.meme.templates.schemas import (
    MemeTemplateBase,
    MemeTemplateResponse,
    MemeTemplateCreate,
)
from core.constants import Const


type ModelT = MemeTemplate
type SchemeT = MemeTemplateBase | MemeTemplateCreate | MemeTemplateResponse
type RepoT = MemeTemplateRepo


class MemeTemplateService[ModelT, SchemeT, RepoTo](TemplateServiceBase):
    _model: MemeTemplate = MemeTemplate
    _base_model: MemeTemplateBase = MemeTemplateBase
    _create_model: MemeTemplateCreate = MemeTemplateCreate
    _response_model: MemeTemplateResponse = MemeTemplateResponse
    _repository: MemeTemplateRepo = MemeTemplateRepo
    _path_to_templates: str | Path = Const.TEMPLATES_DIR

    @classmethod
    async def get_categories(cls, session: AsyncSession) -> list[str]:
        return await cls._repository.get_categories(session)
