from core.exceptions import HTTPExceptionBase, status


class UserErrorMessages:
    __slots__ = ()
    DENIED_403: str = "Access is denied"
    FORBIDDEN_403: str = "Inactive user"
    USER_NOT_FOUND_404: str = "User not found"
    USERS_NOT_FOUND_404: str = "Users not found"
    USER_EXIST_409: str = "User already exists"


class UserExistException(HTTPExceptionBase):
    status_code = status.HTTP_409_CONFLICT
    detail = UserErrorMessages.USER_EXIST_409
