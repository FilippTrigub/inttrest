"""
Simple MongoDB connector for event data
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing import Dict, List, Optional
from datetime import datetime

class MongoConnector:
    """Simple MongoDB connector"""
    
    def __init__(self, password: str):
        """Initialize MongoDB connection"""
        self.uri = f"mongodb+srv://reetikagautam127:{password}@democluster.c5lpr.mongodb.net/?retryWrites=true&w=majority&appName=democluster"
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client.events_db
        self.collection = self.db.events
        
        # Test connection
        try:
            self.client.admin.command('ping')
            print("✅ Connected to MongoDB!")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            raise
    
    def insert_event(self, event_data: Dict) -> bool:
        """Insert a single event"""
        try:
            # Add timestamp if not present
            if 'scraped_at' not in event_data:
                event_data['scraped_at'] = datetime.now().isoformat()
            
            self.collection.insert_one(event_data)
            print(f"✅ Event inserted: {event_data.get('title', 'Unknown')}")
            return True
        except Exception as e:
            print(f"❌ Insert failed: {e}")
            return False
    
    def insert_many_events(self, events_list: List[Dict]) -> int:
        """Insert multiple events"""
        if not events_list:
            return 0
        
        # Add timestamps
        for event in events_list:
            if 'scraped_at' not in event:
                event['scraped_at'] = datetime.now().isoformat()
        
        try:
            result = self.collection.insert_many(events_list, ordered=False)
            inserted_count = len(result.inserted_ids)
            print(f"✅ Inserted {inserted_count} events")
            return inserted_count
        except Exception as e:
            print(f"❌ Batch insert failed: {e}")
            return 0
    
    def find_events(self, city: str = None, category: str = None, limit: int = 100) -> List[Dict]:
        """Find events with optional filters"""
        query = {}
        
        if city:
            query['city'] = {'$regex': city, '$options': 'i'}
        if category:
            query['category'] = {'$regex': category, '$options': 'i'}
        
        try:
            events = list(self.collection.find(query).limit(limit))
            # Convert ObjectId to string
            for event in events:
                event['_id'] = str(event['_id'])
            return events
        except Exception as e:
            print(f"❌ Find failed: {e}")
            return []
    
    def count_events(self) -> int:
        """Count total events"""
        try:
            return self.collection.count_documents({})
        except Exception as e:
            print(f"❌ Count failed: {e}")
            return 0
    
    def close(self):
        """Close connection"""
        self.client.close()
        print("🔐 MongoDB connection closed")
