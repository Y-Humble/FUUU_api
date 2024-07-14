from apps.user.templates.models import UserMemeTemplate
from core.db import SQlAlchemyRepo


class UserTemplateRepo(SQlAlchemyRepo):
    _model = UserMemeTemplate
