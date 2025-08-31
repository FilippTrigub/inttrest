"""
Application configuration settings
"""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    HOST: str = "localhost"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./events.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API Keys
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    EVENTBRITE_API_KEY: Optional[str] = None
    MEETUP_API_KEY: Optional[str] = None
    FACEBOOK_ACCESS_TOKEN: Optional[str] = None
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = None
    
    # Scraping settings
    SELENIUM_HEADLESS: bool = True
    SCRAPING_DELAY_SECONDS: int = 1
    MAX_EVENTS_PER_SOURCE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
