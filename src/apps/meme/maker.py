import io
import textwrap
from pathlib import Path
from typing import Any
from PIL import Image, ImageFont, ImageDraw
from PIL.Image import Image as ImageType
from PIL.ImageFont import FreeTypeFont
from PIL.ImageDraw import ImageDraw as ImageDrawType

from apps.meme.schemas import Meme
from core.constants import Const


class MemeMaker:
    """Create meme with method 'create'"""

    def __init__(self, image_path: str | Path):
        self.width: int = Const.DEFAULT_SIZE[0]
        self.height: int = Const.DEFAULT_SIZE[1]
        self.template = image_path

    @property
    def template(self) -> ImageType:
        return self._template

    @template.setter
    def template(self, image_path: str | Path) -> None:
        with Image.open(image_path) as image:
            image: ImageType = self.resize_template(
                image, self.width, self.height
            )
            self._template: ImageType = image

    def resize_template(self, image: ImageType, width, height) -> ImageType:
        ratio: float = image.width / image.height

        if image.width > image.height:
            size: tuple[int, int] = width, int(width / ratio)
        elif image.width < image.height:
            size: tuple[int, int] = int(width * ratio), height
        else:
            size: tuple[int, int] = width, height

        return image.resize(size=size)

    def __get_data_for_creation(
        self, top_text: str, bottom_text: str
    ) -> dict[str, str | FreeTypeFont | int | list[str] | ImageDrawType]:
        font: FreeTypeFont = ImageFont.truetype(
            Const.FONTS_DIR / "impact.ttf",
            size=self.template.height // 12,
        )
        char_size: float = font.size
        chars_per_line: int = int(self.template.width // (char_size // 1.75))
        top_lines: list[str] = textwrap.wrap(top_text, width=chars_per_line)
        bottom_lines: list[str] = textwrap.wrap(
            bottom_text, width=chars_per_line
        )
        draw_text: ImageDrawType = ImageDraw.Draw(self.template)

        return {
            "top_text": top_text.upper(),
            "bottom_text": bottom_text.upper(),
            "font": font,
            "char_size": font.size,
            "chars_per_line": chars_per_line,
            "top_lines": top_lines,
            "bottom_lines": bottom_lines,
            "draw_text": draw_text,
        }

    def __write_text(
        self,
        template: ImageDraw,
        lines: list[str],
        font: ImageFont,
        y: int,
        char_size: int,
    ) -> None:
        for line in lines:  # type: str
            line_width: int = template.textlength(line, font)
            template.text(
                ((self.template.width - line_width) // 2, y),
                line,
                fill="white",
                font=font,
                stroke_fill="black",
                stroke_width=2,
            )
            y += char_size

    def create(self, top_text: str, bottom_text: str) -> Meme:
        data_for_creation: dict[str, Any] = self.__get_data_for_creation(
            top_text.upper(), bottom_text.upper()
        )

        self.__write_text(
            template=data_for_creation["draw_text"],
            lines=data_for_creation["top_lines"],
            font=data_for_creation["font"],
            y=10,
            char_size=data_for_creation["char_size"],
        )
        y: int = (
            self.template.height
            - data_for_creation["char_size"]
            * len(data_for_creation["bottom_lines"])
            - 17
        )
        self.__write_text(
            template=data_for_creation["draw_text"],
            lines=data_for_creation["bottom_lines"],
            font=data_for_creation["font"],
            y=y,
            char_size=data_for_creation["char_size"],
        )
        if self.template.mode != "RGB":
            self.template = self.template.convert("RGB")
        out: io.BytesIO = io.BytesIO()
        self.template.seek(0)
        self.template.save(out, format="JPEG")

        return Meme(
            top_text=data_for_creation["top_text"],
            bottom_text=data_for_creation["bottom_text"],
            image=out.getvalue(),
        )
