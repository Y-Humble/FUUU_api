from src.core.db import SQlAlchemyRepo
from src.user.models import User


class UserRepo[ModelT: User](SQlAlchemyRepo):
    _model: ModelT = User
