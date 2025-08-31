"""
FastAPI application entry point
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

from app.core.config import settings
from app.api.routes import events, maps
from app.core.database import init_db

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


# Create FastAPI app
app = FastAPI(
    title="Event Discovery App",
    description="Discover events on an interactive map",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(maps.router, prefix="/api/maps", tags=["maps"])


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Event Discovery App</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            body { margin: 0; font-family: Arial, sans-serif; }
            .header { background: #333; color: white; padding: 1rem; text-align: center; }
            .controls { padding: 1rem; background: #f5f5f5; display: flex; gap: 1rem; flex-wrap: wrap; }
            .controls input, .controls select, .controls button { 
                padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; 
            }
            .controls button { background: #007bff; color: white; cursor: pointer; }
            .controls button:hover { background: #0056b3; }
            #map { height: 600px; width: 100%; }
            .event-popup { max-width: 300px; }
            .event-popup img { width: 100%; height: 150px; object-fit: cover; border-radius: 4px; }
            .event-popup h3 { margin: 0.5rem 0; color: #333; }
            .event-popup p { margin: 0.25rem 0; color: #666; font-size: 0.9rem; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🗺️ Event Discovery App</h1>
            <p>Discover events happening around you</p>
        </div>
        
        <div class="controls">
            <input type="text" id="search" placeholder="Search events..." />
            <select id="category">
                <option value="">All Categories</option>
                <option value="technology">Technology</option>
                <option value="business">Business</option>
                <option value="art">Art & Culture</option>
                <option value="music">Music</option>
                <option value="sports">Sports</option>
            </select>
            <input type="date" id="date" />
            <input type="text" id="location" placeholder="Location (e.g., San Francisco)" />
            <button onclick="searchEvents()">Search Events</button>
            <button onclick="loadSampleEvents()">Load Sample Events</button>
        </div>
        
        <div id="map"></div>
        
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Initialize map
            const map = L.map('map').setView([37.7749, -122.4194], 12); // San Francisco
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);
            
            let eventMarkers = [];
            
            function clearMarkers() {
                eventMarkers.forEach(marker => map.removeLayer(marker));
                eventMarkers = [];
            }
            
            function addEventMarker(event) {
                const marker = L.marker([event.latitude, event.longitude])
                    .bindPopup(`
                        <div class="event-popup">
                            ${event.image_url ? `<img src="${event.image_url}" alt="${event.title}" />` : ''}
                            <h3>${event.title}</h3>
                            <p><strong>📅 ${event.date}</strong></p>
                            <p><strong>📍 ${event.location}</strong></p>
                            <p>${event.description}</p>
                            ${event.url ? `<p><a href="${event.url}" target="_blank">View Event</a></p>` : ''}
                        </div>
                    `)
                    .addTo(map);
                    
                eventMarkers.push(marker);
            }
            
            async function searchEvents() {
                const search = document.getElementById('search').value;
                const category = document.getElementById('category').value;
                const date = document.getElementById('date').value;
                const location = document.getElementById('location').value;
                
                const params = new URLSearchParams();
                if (search) params.append('search', search);
                if (category) params.append('category', category);
                if (date) params.append('date', date);
                if (location) params.append('location', location);
                
                try {
                    const response = await fetch(`/api/events/search?${params}`);
                    const events = await response.json();
                    
                    clearMarkers();
                    events.forEach(addEventMarker);
                    
                    if (events.length > 0) {
                        const group = new L.featureGroup(eventMarkers);
                        map.fitBounds(group.getBounds().pad(0.1));
                    }
                } catch (error) {
                    console.error('Error fetching events:', error);
                    alert('Error fetching events. Please try again.');
                }
            }
            
            function loadSampleEvents() {
                // Sample events for demonstration
                const sampleEvents = [
                    {
                        title: "Tech Meetup: AI & Machine Learning",
                        latitude: 37.7849,
                        longitude: -122.4094,
                        date: "2025-09-15",
                        location: "Downtown San Francisco",
                        description: "Join us for an exciting discussion about the latest in AI and ML technologies.",
                        image_url: "https://via.placeholder.com/300x150?text=AI+Meetup",
                        url: "https://example.com/event1"
                    },
                    {
                        title: "Art Gallery Opening",
                        latitude: 37.7649,
                        longitude: -122.4194,
                        date: "2025-09-20",
                        location: "Mission District",
                        description: "Contemporary art exhibition featuring local artists.",
                        image_url: "https://via.placeholder.com/300x150?text=Art+Gallery",
                        url: "https://example.com/event2"
                    },
                    {
                        title: "Startup Pitch Competition",
                        latitude: 37.7749,
                        longitude: -122.4094,
                        date: "2025-09-25",
                        location: "SOMA",
                        description: "Watch innovative startups pitch their ideas to investors.",
                        image_url: "https://via.placeholder.com/300x150?text=Startup+Pitch",
                        url: "https://example.com/event3"
                    }
                ];
                
                clearMarkers();
                sampleEvents.forEach(addEventMarker);
                
                const group = new L.featureGroup(eventMarkers);
                map.fitBounds(group.getBounds().pad(0.1));
            }
            
            // Load sample events on page load
            document.addEventListener('DOMContentLoaded', loadSampleEvents);
        </script>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
