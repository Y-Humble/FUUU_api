from core.db import SQlAlchemyRepo
from app.user.auth.models import RefreshSessionModel


class RefreshSessionRepo[RS: RefreshSessionModel](SQlAlchemyRepo):
    _model: RS = RefreshSessionModel
