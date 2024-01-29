import datetime
# from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from src.database.models import Role


class ChatBase(BaseModel):
    title_chat: str = Field(max_length=500)
    file_url: str | None
    chat_data: str | None



class ChatModel(ChatBase):
    id: int
    # file_url: str | None
    # chat_data: str = Field()
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    user_id: int

    class Config:
        from_attributes = True


class ChatUpdate(ChatModel):
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class ChatHistoryBase(BaseModel):
    message: str = Field(max_length=5000)


class ChatHistoryModel(ChatHistoryBase):
    id: int
    created_at: datetime.datetime | None
    user_id: int
    chat_id: int

    class Config:
        from_attributes = True