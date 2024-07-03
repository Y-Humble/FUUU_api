from typing import TYPE_CHECKING
from dataclasses import dataclass
from uuid import UUID as UUIDType
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.user.models import User


@dataclass
class UserRelationMixin:
    _user_id_unique: bool = False
    _user_id_nullable: bool = False
    _on_delete: str | None = None
    _user_back_populates: str | None = None


    @declared_attr
    def user(self) -> Mapped["User"]:
        return relationship(
            "User",
            back_populates=self._user_back_populates,
        )


    @declared_attr
    def user_id(self) -> Mapped[UUIDType]:
        return mapped_column(
            ForeignKey("users.id", ondelete=self._on_delete),
            unique=self._user_id_unique,
            nullable=self._user_id_nullable,
        )