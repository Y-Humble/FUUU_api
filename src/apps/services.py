import os
import aiofiles.os as aos
from aiofiles import open as async_open
from fastapi import UploadFile
from pathlib import Path

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from apps.exceptions import TemplateNotFoundException
from core.db import Base, SQlAlchemyRepo as SQLRepo


class TemplateServiceBase[ModelT: Base, SchemeT: BaseModel, RepoT: SQLRepo]:
    _model: ModelT
    _base_model: SchemeT
    _response_model: SchemeT
    _create_model: SchemeT
    _repository: RepoT
    _path_to_templates: str | Path | None = None

    @classmethod
    async def get(
        cls,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        **filter_by,
    ) -> list[SchemeT]:
        result: list[ModelT] = await cls._repository.get(
            session=session, offset=offset, limit=limit, **filter_by
        )
        return [
            cls._response_model.model_validate(template) for template in result
        ]

    @classmethod
    async def get_one(cls, session: AsyncSession, model_id: int) -> ModelT:
        template: ModelT = await cls._repository.get_one_or_none(
            session=session, id=model_id
        )
        if template is None:
            raise TemplateNotFoundException
        return template

    @classmethod
    async def add_one(cls, session: AsyncSession, **data) -> SchemeT:
        image: UploadFile = data.pop("image")
        title: str = cls.__validate_title(data.get("title"))
        category: str = data.get("category")
        path: str = await cls.__add_template(image, title, category)
        data.update(title=title, category=category, path=path)
        result: ModelT = await cls._repository.add_one(session, **data)
        return cls._response_model.model_validate(result)

    @classmethod
    async def update_one(
        cls, session: AsyncSession, img_id: int, **data
    ) -> SchemeT:
        if db_image := await cls._repository.get_one_or_none(
            session, id=img_id
        ):
            image: bytes = Path(db_image.path).read_bytes()
            title: str = cls.__validate_title(
                data.get("title") or db_image.title
            )
            category: str = data.get("category") or db_image.category
            path: str = await cls.__add_template(image, title, category)
            await cls.__delete_by_path(db_image.path)

            result: ModelT = await cls._repository.update_one(
                session, db_image, title=title, category=category, path=path
            )
            return cls._response_model.model_validate(result)
        raise TemplateNotFoundException

    @classmethod
    async def delete_one(cls, session: AsyncSession, img_id) -> None:
        if (
            image := await cls._repository.get_one_or_none(session, id=img_id)
        ) is not None:
            await cls.__delete_by_path(image.path)
            await cls._repository.delete_one(session, image)

    @classmethod
    async def __add_template(
        cls, image: UploadFile | bytes, title: str, category: str
    ) -> str:

        img_path: Path = cls._path_to_templates / category / title
        image: UploadFile | bytes = image

        await cls.__create_folder_if_not_exists(img_path.parent)
        await cls.__write_template(path=img_path, data=image)
        return str(img_path)

    @staticmethod
    async def __create_folder_if_not_exists(path: str | Path) -> None:
        if not os.path.exists(path):
            await aos.makedirs(path)

    @staticmethod
    def __validate_title(title: str) -> str:
        if title.endswith(".jpg") or title.endswith(".jpeg"):
            return title
        else:
            return f"{title}.jpg"

    @staticmethod
    async def __write_template(path: Path, data: UploadFile | bytes) -> None:
        async with async_open(path, "wb") as img:
            if isinstance(data, bytes):
                await img.write(data)
            else:
                content: bytes = await data.read()
                await img.write(content)

    @staticmethod
    async def __delete_by_path(str_path: str) -> None:
        path: Path = Path(str_path)
        if not path.is_file():
            raise ValueError(f"Path must be a file - Path: {path}")
        await aos.remove(path)
        dir_path: Path = path.parent
        if dir_path.is_dir():
            if len(list(dir_path.iterdir())) == 0:
                await aos.rmdir(dir_path)
