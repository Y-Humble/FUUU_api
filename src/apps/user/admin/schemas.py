from pydantic import BaseModel

from apps.user import Status
from apps.user.schemas import UserCreate, UserPartialUpdate


class Admin(BaseModel):
    active: bool = True
    status: Status | None = None


class UserCreateAdmin(UserCreate, Admin):
    pass


class UserUpdateAdmin(UserPartialUpdate, Admin):
    pass
