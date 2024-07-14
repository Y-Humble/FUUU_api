from pydantic import BaseModel, ConfigDict, FilePath, computed_field
from core.config import settings


class MemeTemplateBase(BaseModel):
    title: str
    category: str


class MemeTemplateCreate(MemeTemplateBase):
    path: str | FilePath


class MemeTemplateUpdate(MemeTemplateBase):
    pass


class MemeTemplateUpdatePartial(MemeTemplateBase):
    title: str | None = None
    category: str | None = None


class MemeTemplateResponse(MemeTemplateBase):
    id: int
    path: str | FilePath

    @computed_field
    @property
    def url(self) -> str:
        return f"{settings.run.url}/meme/template/{self.id}"

    model_config = ConfigDict(from_attributes=True)
