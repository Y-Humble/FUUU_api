from uuid import UUID
from pydantic import BaseModel, ConfigDict, FilePath, computed_field

from core.config import settings


class UserTemplateBase(BaseModel):
    title: str
    category: str
    path: str | FilePath | None = None


class UserTemplateCreate(UserTemplateBase):
    user_id: UUID


class UserTemplateUpdate(UserTemplateBase):
    pass


class UserTemplateUpdatePartial(UserTemplateBase):
    title: str | None = None
    category: str | None = None


class UserTemplateResponse(UserTemplateBase):
    id: int
    path: str | FilePath

    @computed_field
    @property
    def url(self) -> str:
        return f"{settings.run.url}/user/template/{self.id}"

    model_config = ConfigDict(from_attributes=True)
