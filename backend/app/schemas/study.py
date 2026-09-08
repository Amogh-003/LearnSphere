from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.user import UserPublic


class TopicBase(BaseModel):
    name: str = Field(..., max_length=200)


class TopicCreate(TopicBase):
    pass


class TopicOut(TopicBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TagBase(BaseModel):
    name: str = Field(..., max_length=50)


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RoomBase(BaseModel):
    name: str = Field(..., max_length=200)
    description: str | None = None
    topic_id: int | None = None
    is_pinned: bool = False
    scheduled_for: datetime | None = None
    max_participants: int | None = None


class RoomCreate(RoomBase):
    tag_names: list[str] = []


class RoomUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    topic_id: int | None = None
    is_pinned: bool | None = None
    scheduled_for: datetime | None = None
    max_participants: int | None = None
    tag_names: list[str] | None = None


class RoomOut(RoomBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    host: UserPublic
    topic: TopicOut | None = None
    tags: list[TagOut] = []
    participant_count: int = 0
    like_count: int = 0
    is_liked: bool = False
    created_at: datetime
    updated_at: datetime


class MessageBase(BaseModel):
    body: str = Field(..., min_length=1)
    parent_id: int | None = None


class MessageCreate(MessageBase):
    pass


class MessageOut(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    user: UserPublic
    created_at: datetime
    replies: list["MessageOut"] = []