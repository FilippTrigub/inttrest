# Event Discovery App

A Python-based event discovery application that scrapes events from various platforms and displays them on an interactive map.

## Features

- 🗺️ Interactive Google Maps integration with event pins
- 🎫 Event data from Eventbrite, Meetup, and social platforms
- 🖼️ Image previews on hover
- 🔍 Search and filter events by category, date, and location
- 📱 Responsive web interface

## Tech Stack

- **Backend**: FastAPI + Python 3.9+
- **Frontend**: HTML/CSS/JavaScript with Folium maps
- **Data Scraping**: BeautifulSoup, Selenium, APIs
- **Database**: SQLAlchemy + PostgreSQL/SQLite
- **Task Queue**: Celery + Redis
- **Package Manager**: uv

## Quick Start

### Prerequisites

- Python 3.9+
- uv package manager
- Redis (for task queue)

### Installation

1. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone and setup the project:
```bash
git clone <your-repo-url>
cd event-discovery-app
uv sync
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Run the application:
```bash
uv run python -m app.main
```

Visit `http://localhost:8000` to see the application.

## Development

### Run in development mode:
```bash
uv run uvicorn app.main:app --reload
```

### Run tests:
```bash
uv run pytest
```

### Format code:
```bash
uv run black .
uv run ruff check .
```

## Configuration

Copy `.env.example` to `.env` and configure:

- API keys for event platforms
- Google Maps API key
- Database settings
- Redis connection

## License

MIT License - see LICENSE file for details.
