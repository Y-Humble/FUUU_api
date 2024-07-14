from typing import TYPE_CHECKING
from uuid import UUID as UUID_T
from sqlalchemy import ForeignKey, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from core.db.mixins import IdIntegerMixin

if TYPE_CHECKING:
    from apps.user import User


class UserMemeTemplate(Base, IdIntegerMixin):
    title: Mapped[str] = mapped_column(VARCHAR(100))
    category: Mapped[str] = mapped_column(VARCHAR(100))
    path: Mapped[str] = mapped_column(VARCHAR)
    user: Mapped["User"] = relationship(
        "User",
        back_populates="templates",
    )
    user_id: Mapped[UUID_T] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
