from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.user import User
from core.db import Base
from core.db.mixins import IdIntegerMixin

if TYPE_CHECKING:
    from apps.user import User


class TelegramUser(Base, IdIntegerMixin):
    tg_id: Mapped[int] = mapped_column(unique=True)
    user: Mapped["User"] = relationship("User", back_populates="tg")
    user_email: Mapped[str] = mapped_column(
        ForeignKey("users.email"), unique=True
    )
