from pydantic import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str
    SECRET_KEY: str
    TWITTER_API_KEY: str
    TWITTER_API_SECRET: str
    TWITTER_ACCESS_TOKEN: str
    TWITTER_ACCESS_TOKEN_SECRET: str
    NOTION_API_KEY: str
    NOTION_DATABASE_ID: str
    OPENAI_API_KEY: Optional[str]
    TWEET_POPULARITY_THRESHOLD: int
    AI_TOOLS_KEYWORDS: List[str]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()