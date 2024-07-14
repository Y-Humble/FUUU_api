from typing import Any

from pydantic import (
    PlainSerializer,
    BaseModel,
    WithJsonSchema,
    GetCoreSchemaHandler,
)
from pydantic_core import CoreSchema, core_schema
from typing_extensions import Annotated


class HashValue(bytes):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Returns a schema that calls a validator function before validation"""
        return core_schema.with_info_before_validator_function(
            cls.validate,
            handler(bytes),
        )

    @classmethod
    def validate(cls, value: Any, x: Any) -> bytes:
        result: bytes
        if isinstance(value, str):
            result = bytes.fromhex(value)
        elif isinstance(value, bytes):
            result = value
        else:
            raise TypeError()

        return result


type HexBytes = Annotated[
    HashValue,
    PlainSerializer(lambda b: b.hex()),
    WithJsonSchema({"type": "string"}),
]


class LinesInfo(BaseModel):
    top_text: str | None
    bottom_text: str | None


class Template(LinesInfo):
    img_id: int | str


class Meme(BaseModel):
    top_text: str
    bottom_text: str
    image: HexBytes


class MemeURLResponse(BaseModel):
    meme_id: int
    url: str | None = None
    home_url: str | None = None
