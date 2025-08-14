from sqlalchemy import Column, Integer, String, DateTime, func, Index
from sqlalchemy.orm import validates
from .database import Base

class ShortURL(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(64), unique=True, index=True, nullable=False)
    original_url = Column(String(2048), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    clicks = Column(Integer, default=0)
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    # Optional owner or notes fields could be added for multi-user

    @validates("code")
    def validate_code(self, key, value):
        # Allow a-z A-Z 0-9 - _
        import re
        if not value or not re.fullmatch(r"[A-Za-z0-9_-]{3,64}", value):
            raise ValueError("Code must be 3-64 chars: letters, digits, '-' or '_'")
        return value

Index("ix_short_urls_code_unique", ShortURL.code, unique=True)
