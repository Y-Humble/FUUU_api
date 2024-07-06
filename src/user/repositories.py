from core.db import SQlAlchemyRepo
from user.models import User


class UserRepo[ModelT: User](SQlAlchemyRepo):
    _model: ModelT = User
