# MongoDB Event Connector

Simple MongoDB connector for event data storage.

## Usage

```python
from mongo_connector import MongoConnector

# Connect to MongoDB
mongo = MongoConnector("your_password")

# Insert event
event = {"event_id": "test_001", "title": "My Event"}
mongo.insert_event(event)

# Close connection
mongo.close()
```

## Installation

```bash
uv sync
```
