from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator


class Message(BaseModel):
    type: Literal["text", "image"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    chat_id: str = Field(min_length=1, max_length=128)
    messages: List[Message] = Field(min_items=1, max_items=50)


class ChatResponse(BaseModel):
    message: Optional[str] = None
    base_random_keys: Optional[List[str]] = None
    member_random_keys: Optional[List[str]] = None

    @field_validator("base_random_keys", "member_random_keys")
    @classmethod
    def _limit_length(cls, v):
        if v is not None and len(v) > 10:
            raise ValueError("max 10 keys allowed")
        return v


