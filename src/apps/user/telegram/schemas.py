from pydantic import BaseModel, ConfigDict, EmailStr


class TgUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tg_id: int
    user_email: EmailStr


class TgUserCreate(TgUserSchema):
    password: str
