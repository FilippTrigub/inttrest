"""
Events API routes
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db, Event

router = APIRouter()


class EventResponse(BaseModel):
    """Event response model"""
    id: int
    title: str
    description: Optional[str] = None
    date: datetime
    location: str
    latitude: float
    longitude: float
    category: Optional[str] = None
    source: str
    url: Optional[str] = None
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True


@router.get("/search", response_model=List[EventResponse])
async def search_events(
    search: Optional[str] = Query(None, description="Search term"),
    category: Optional[str] = Query(None, description="Event category"),
    date: Optional[str] = Query(None, description="Event date (YYYY-MM-DD)"),
    location: Optional[str] = Query(None, description="Location"),
    db: Session = Depends(get_db)
):
    """Search for events with filters"""
    
    query = db.query(Event)
    
    # Apply filters
    if search:
        query = query.filter(
            Event.title.contains(search) | 
            Event.description.contains(search)
        )
    
    if category:
        query = query.filter(Event.category == category)
    
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(Event.date >= date_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if location:
        query = query.filter(Event.location.contains(location))
    
    # Limit results
    events = query.limit(100).all()
    
    return events


@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get available event categories"""
    
    categories = db.query(Event.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get specific event by ID"""
    
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return event


@router.post("/scrape")
async def trigger_scraping():
    """Trigger event scraping from various sources"""
    
    # This would typically trigger a Celery task
    # For now, return a simple response
    return {"message": "Scraping task triggered", "status": "pending"}
