"""
Example usage of MongoDB connector
"""

from mongo_connector import MongoConnector

def test_mongo():
    """Test MongoDB operations"""
    
    # Replace with your actual password
    password = "Ranjeeta1234!"
    
    try:
        # Connect
        mongo = MongoConnector(password)
        
        # Sample event data matching your schema
        sample_event = {
            "event_id": "test_001",
            "title": "Test Event",
            "description": "This is a test event",
            "start_datetime": "2025-09-15T18:00:00",
            "timezone": "Europe/Paris",
            "event_url": "https://example.com/event",
            "platform": "Test",
            "is_online": False,
            "price": 25.0,
            "currency": "EUR",
            "venue_name": "Test Venue",
            "address": "123 Test Street",
            "city": "Paris",
            "postal_code": "75001",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "organizer_name": "Test Organizer",
            "category": "Technology",
            "tags": ["test", "demo"],
            "image_url": "https://example.com/image.jpg",
            "source_site": "test.com"
        }
        
        # Insert single event
        print("📝 Inserting single event...")
        mongo.insert_event(sample_event)
        
        # Insert multiple events
        print("\n📝 Inserting multiple events...")
        events_batch = [
            {
                "event_id": "batch_001",
                "title": "Batch Event 1",
                "start_datetime": "2025-09-16T19:00:00",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "city": "Paris",
                "category": "Technology",
                "platform": "Batch"
            },
            {
                "event_id": "batch_002", 
                "title": "Batch Event 2",
                "start_datetime": "2025-09-17T20:00:00",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "city": "Lyon",
                "category": "Business",
                "platform": "Batch"
            }
        ]
        
        inserted_count = mongo.insert_many_events(events_batch)
        print(f"Inserted {inserted_count} events")
        
        # Find events
        print("\n🔍 Finding events...")
        all_events = mongo.find_events(limit=5)
        for event in all_events:
            print(f"- {event['title']} in {event.get('city', 'Unknown')}")
        
        # Count total
        total = mongo.count_events()
        print(f"\n📊 Total events in database: {total}")
        
        # Close connection
        mongo.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_mongo()
