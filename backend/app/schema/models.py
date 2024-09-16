from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Tweet(BaseModel):
    id: str
    account_handle: str
    followers_count: int
    likes_count: int
    timestamp: datetime
    content: str
    media_urls: List[str]
    quoted_tweet_content: Optional[str]
    doubt_rating: float
    ai_tools_mentioned: List[str]

class Response(BaseModel):
    id: str
    tweet_id: str
    content: str
    generated_at: datetime
    status: str
    generated_by: str

class Context(BaseModel):
    id: str
    name: str
    content: str
    created_at: datetime
    updated_at: datetime

class Prompt(BaseModel):
    id: str
    name: str
    content: str
    created_at: datetime
    updated_at: datetime

class User(BaseModel):
    id: str
    username: str
    email: str
    role: str
    last_login: datetime