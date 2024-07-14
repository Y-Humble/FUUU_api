from core.db import SQlAlchemyRepo
from apps.user.auth.models import RefreshSession


class RefreshSessionRepo[RS: RefreshSession](SQlAlchemyRepo):
    _model: RS = RefreshSession
