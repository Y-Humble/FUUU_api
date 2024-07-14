from core.db import Base
from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from core.db.mixins import IdIntegerMixin


class MemeTemplate(Base, IdIntegerMixin):
    title: Mapped[str] = mapped_column(VARCHAR(100))
    category: Mapped[str] = mapped_column(VARCHAR(100))
    path: Mapped[str] = mapped_column(VARCHAR)
