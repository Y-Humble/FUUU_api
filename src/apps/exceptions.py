from core.exceptions import HTTPExceptionBase
from fastapi import status


class CommonErrorMessages:
    __slots__ = ()
    TEMPLATE_NOT_FOUND_404: str = "Template not found"


class TemplateNotFoundException(HTTPExceptionBase):
    status_code = status.HTTP_404_NOT_FOUND
    detail = CommonErrorMessages.TEMPLATE_NOT_FOUND_404
