"""
Eventbrite API scraper
"""

from typing import List, Optional
from datetime import datetime
import json

from app.services.base_scraper import BaseScraper, Event


class EventbriteScraper(BaseScraper):
    """Scraper for Eventbrite events using their API"""
    
    BASE_URL = "https://www.eventbriteapi.com/v3"
    
    async def scrape_events(
        self, 
        location: str = "San Francisco, CA",
        category: Optional[str] = None,
        max_events: int = 50
    ) -> List[Event]:
        """Scrape events from Eventbrite API"""
        
        if not self.api_key:
            # Return mock events if no API key
            return await self._get_mock_events()
        
        # Build API URL
        url = f"{self.BASE_URL}/events/search/"
        params = {
            "location.address": location,
            "location.within": "25km",
            "expand": "venue,organizer,format,category",
            "sort_by": "date",
            "page_size": min(max_events, 50),
            "token": self.api_key
        }
        
        if category:
            # Map category to Eventbrite category ID
            category_mapping = {
                "technology": "102",
                "business": "101",
                "art": "105",
                "music": "103",
                "sports": "108"
            }
            if category in category_mapping:
                params["categories"] = category_mapping[category]
        
        try:
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            events = []
            for event_data in data.get("events", []):
                event = await self._parse_eventbrite_event(event_data)
                if event:
                    events.append(event)
            
            return events
        
        except Exception as e:
            print(f"Error scraping Eventbrite: {e}")
            return await self._get_mock_events()
    
    async def _parse_eventbrite_event(self, event_data: dict) -> Optional[Event]:
        """Parse Eventbrite event data"""
        
        try:
            # Extract basic info
            title = event_data.get("name", {}).get("text", "")
            description = event_data.get("description", {}).get("text", "")
            url = event_data.get("url", "")
            source_id = event_data.get("id", "")
            
            # Parse date
            start_time = event_data.get("start", {}).get("utc", "")
            date = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            
            # Extract venue info
            venue = event_data.get("venue", {})
            location = venue.get("name", "")
            if venue.get("address"):
                address = venue["address"]
                location += f", {address.get('localized_area_display', '')}"
            
            # Get coordinates
            latitude = float(venue.get("latitude", 0)) or 37.7749
            longitude = float(venue.get("longitude", 0)) or -122.4194
            
            # Extract category
            category = "other"
            if event_data.get("category"):
                category = event_data["category"].get("short_name", "other").lower()
            
            # Extract image
            image_url = None
            if event_data.get("logo"):
                image_url = event_data["logo"].get("url")
            
            return Event(
                title=title,
                description=description,
                date=date,
                location=location,
                latitude=latitude,
                longitude=longitude,
                category=category,
                source="eventbrite",
                source_id=source_id,
                url=url,
                image_url=image_url
            )
        
        except Exception as e:
            print(f"Error parsing Eventbrite event: {e}")
            return None
    
    async def _get_mock_events(self) -> List[Event]:
        """Return mock Eventbrite events for testing"""
        
        return [
            Event(
                title="Tech Startup Networking Night",
                description="Connect with fellow entrepreneurs and tech enthusiasts in the heart of Silicon Valley.",
                date=datetime(2025, 9, 15, 18, 0),
                location="San Francisco, CA",
                latitude=37.7849,
                longitude=-122.4094,
                category="technology",
                source="eventbrite",
                source_id="mock_eb_1",
                url="https://eventbrite.com/mock-event-1",
                image_url="https://via.placeholder.com/300x150?text=Tech+Networking"
            ),
            Event(
                title="Digital Marketing Workshop",
                description="Learn the latest strategies in digital marketing and social media.",
                date=datetime(2025, 9, 18, 14, 0),
                location="San Francisco, CA",
                latitude=37.7749,
                longitude=-122.4194,
                category="business",
                source="eventbrite",
                source_id="mock_eb_2",
                url="https://eventbrite.com/mock-event-2",
                image_url="https://via.placeholder.com/300x150?text=Marketing+Workshop"
            )
        ]
