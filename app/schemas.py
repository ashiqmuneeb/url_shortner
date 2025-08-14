from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime

class ShortenRequest(BaseModel):
    url: HttpUrl = Field(..., description="URL to shorten (http/https)")
    custom_alias: Optional[str] = Field(None, pattern=r"^[A-Za-z0-9_-]{3,64}$")

class ShortenResponse(BaseModel):
    code: str
    short_url: str
    original_url: str

class ExpandResponse(BaseModel):
    code: str
    original_url: str
    clicks: int
    created_at: datetime
    last_accessed: Optional[datetime]
