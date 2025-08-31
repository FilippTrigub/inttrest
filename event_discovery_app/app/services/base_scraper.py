"""
Base scraper class and common utilities
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
import httpx
from bs4 import BeautifulSoup


class Event:
    """Event data class"""
    
    def __init__(
        self,
        title: str,
        description: str,
        date: datetime,
        location: str,
        latitude: float,
        longitude: float,
        category: str,
        source: str,
        source_id: str,
        url: Optional[str] = None,
        image_url: Optional[str] = None,
    ):
        self.title = title
        self.description = description
        self.date = date
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.category = category
        self.source = source
        self.source_id = source_id
        self.url = url
        self.image_url = image_url


class BaseScraper(ABC):
    """Base class for event scrapers"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = httpx.AsyncClient()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.aclose()
    
    @abstractmethod
    async def scrape_events(
        self, 
        location: str = "San Francisco, CA",
        category: Optional[str] = None,
        max_events: int = 50
    ) -> List[Event]:
        """Scrape events from the source"""
        pass
    
    async def get_html(self, url: str) -> str:
        """Fetch HTML content from URL"""
        response = await self.session.get(url)
        response.raise_for_status()
        return response.text
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, 'html.parser')
    
    async def geocode_address(self, address: str) -> tuple[float, float]:
        """Convert address to coordinates (mock implementation)"""
        # In production, use Google Maps Geocoding API
        # For now, return San Francisco coordinates
        return 37.7749, -122.4194
