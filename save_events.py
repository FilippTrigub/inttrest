"""
Helper to save MCP data to MongoDB
"""

from mongo_connector import MongoConnector

def save_mcp_events(mcp_events, platform, password):
    """Save MCP events to MongoDB"""
    
    if not mcp_events:
        print("No events to save")
        return 0
    
    mongo = MongoConnector(password)
    
    # Convert MCP format to your schema
    converted_events = []
    for event in mcp_events:
        converted = {
            "event_id": f"{platform}_{event.get('id', 'unknown')}",
            "title": event.get('title', event.get('name', 'Unknown Event')),
            "description": event.get('description', ''),
            "start_datetime": event.get('start_datetime', event.get('date', '')),
            "platform": platform.title(),
            "latitude": float(event.get('latitude', 0)),
            "longitude": float(event.get('longitude', 0)),
            "city": event.get('city', ''),
            "category": event.get('category', 'Other'),
            "event_url": event.get('url', ''),
            "image_url": event.get('image_url', ''),
            "venue_name": event.get('location', ''),
            "source_site": f"{platform}.com"
        }
        converted_events.append(converted)
    
    # Insert to MongoDB
    inserted = mongo.insert_many_events(converted_events)
    mongo.close()
    
    return inserted

# Example usage:
# events = [{"id": "123", "title": "Test Event", "latitude": 48.8566, "longitude": 2.3522}]
# count = save_mcp_events(events, "eventbrite", "your_password")
# print(f"Saved {count} events")
