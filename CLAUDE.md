# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is an interest-based location discovery application with a Next.js frontend and MCP (Model Context Protocol) backend integration. The application provides an interactive map with AI-powered chat for finding points of interest.

**Frontend Structure:**
- Next.js 15 with App Router (`frontend/app/`)
- React 19 with TypeScript
- Mapbox GL integration for 3D maps centered on Paris
- AI SDK React integration for chat interface
- Tailwind CSS for styling

**Backend Structure:**
- MCP servers in `mcp_servers/` directory
- Eventbrite integration (currently in development)
- Demo search functionality via MCP adapter

**Key Components:**
- `frontend/components/Chat.tsx`: Main chat interface with category filters and AI integration
- `frontend/components/Map.tsx`: 3D Mapbox map component with terrain visualization
- `frontend/app/api/chat/route.ts`: AI SDK route for OpenAI integration
- `frontend/app/api/mcp/route.ts`: MCP tool handler for place searches

## Development Commands

**Frontend Development:**
```bash
cd frontend
npm run dev        # Start development server with Turbopack
npm run build      # Build for production with Turbopack
npm start          # Start production server
```

**Environment Setup:**
- Frontend requires `NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN` for map functionality
- Chat API uses OpenAI GPT-4o model
- MCP server integration runs on `/api/mcp` endpoint

## Key Technical Details

**Frontend Tech Stack:**
- Next.js 15 with Turbopack enabled for faster builds
- AI SDK for streaming chat responses and tool calling
- React Map GL for Mapbox integration with 3D terrain
- MCP SDK for client-side tool execution
- TypeScript with strict type checking

**Chat Functionality:**
- Supports category filtering (Restaurants, Parcs, Musées, Cafés, Shopping, Hôtels)
- Date-based event searching
- Tool calling via MCP for `search_places` functionality
- Streaming responses with real-time UI updates

**Map Features:**
- 3D terrain visualization with 60-degree pitch
- Centered on Paris coordinates (48.8566, 2.3522)
- Mapbox Standard style with terrain exaggeration
- Responsive layout with chat sidebar

## File Organization

```
frontend/
├── app/
│   ├── api/
│   │   ├── chat/route.ts     # AI chat endpoint
│   │   └── mcp/route.ts      # MCP tool handler
│   ├── layout.tsx            # App layout
│   └── page.tsx              # Main page component
├── components/
│   ├── Chat.tsx              # Chat interface
│   └── Map.tsx               # Map component
└── package.json              # Dependencies and scripts

mcp_servers/                  # MCP server implementations
temp/                         # Temporary scripts (meetup scraper)
```

## Testing & Linting

No specific test or lint commands are currently configured in the package.json. When implementing tests, use Jest or Vitest for unit testing and consider adding ESLint and Prettier for code quality.