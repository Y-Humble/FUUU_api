from fastapi import status
from core.exceptions import HTTPExceptionBase


class MemeNotFoundException(HTTPExceptionBase):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Meme not found!"
