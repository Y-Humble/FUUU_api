from functools import lru_cache
from fastapi import FastAPI
from sqladmin import Admin, ModelView

from apps.meme import MemeTemplate
from apps.user import User, UserMemeTemplate, RefreshSession, TelegramUser
from core.config import settings
from core.db import db_sidekick


@lru_cache(maxsize=1)
def setup_admin(app: FastAPI) -> Admin:
    admin: Admin = Admin(
        app=app,
        engine=db_sidekick._engine,
        title=f"{settings.run.app_title} Admin",
    )
    admin.add_view(UserAdmin)
    admin.add_view(UserMemeTemplateAdmin)
    admin.add_view(RefreshSessionAdmin)
    admin.add_view(MemeTemplateAdmin)
    admin.add_view(TelegramUserAdmin)
    return admin


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.status,
        User.active,
    ]


class UserMemeTemplateAdmin(ModelView, model=UserMemeTemplate):
    column_list = "__all__"


class RefreshSessionAdmin(ModelView, model=RefreshSession):
    column_list = "__all__"


class MemeTemplateAdmin(ModelView, model=MemeTemplate):
    column_list = "__all__"


class TelegramUserAdmin(ModelView, model=TelegramUser):
    column_list = "__all__"
