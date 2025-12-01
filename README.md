# Media Recommendation & Tracking Agent

A multi-agent system for discovering and tracking anime, movies, TV shows, and manga with personalized recommendations.

## Table of Contents

- [Problem](#problem)
- [Solution](#solution)
- [Architecture](#architecture)
- [Technical Implementation](#technical-implementation)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Evaluation](#evaluation)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [License](#license)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

---

## Problem

Managing media consumption across different platforms is fragmented. Searching for content requires visiting multiple sites like TMDB for movies and AniList for anime. Tracking progress manually in spreadsheets is tedious. Generic recommendations on streaming platforms do not account for personal preferences.

This project consolidates search, tracking, and recommendations into a single system with natural language interaction.

## Solution

The system uses four specialized agents coordinated by Google Gemini 2.0 Flash:

- **Orchestrator Agent**: Routes requests to sub-agents and manages conversation state
- **Discovery Agent**: Searches TMDB API for movies/TV and AniList GraphQL for anime/manga
- **Library Agent**: Manages user collection and tracks progress
- **Recommender Agent**: Generates suggestions based on library and preferences

Each agent handles a specific task. This separation makes the code modular and easier to extend.

## Architecture
```
Orchestrator Agent
├── Discovery Agent (TMDB + AniList APIs)
├── Library Agent (User data storage)
└── Recommender Agent (Scoring algorithm)
```

The orchestrator interprets user input and delegates to appropriate sub-agents. Agents communicate by passing structured data. Session state persists across conversations using in-memory storage.

## Technical Implementation

**Tools**: 7 custom tools for search, library management, and recommendations
- search_media, add_to_library, update_progress, list_library, get_recommendations

**Services**:
- SessionService: Manages conversation sessions
- MemoryService: Stores library and preferences
- ObservabilityService: Logs agent calls and metrics

**Data Model**: Unified MediaItem structure works across all media types regardless of API source

**Agent Communication**: Orchestrator calls sub-agents directly and passes context as needed

## Installation

Requirements: Python 3.11+, Google API Key, TMDB API Key
```bash
git clone https://github.com/OSAMAxALHARBI/media-recommendation-agent.git
cd media-recommendation-agent
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create `.env` file:
```env
GOOGLE_API_KEY=your_key_here
TMDB_API_KEY=your_key_here
```

Get API keys:
- Google Gemini: https://ai.google.dev/
- TMDB: https://www.themoviedb.org/settings/api

## Usage

Run automated tests:
```bash
python main.py
```

Interactive CLI:
```bash
python -m src.api.server --cli
```

REST API server:
```bash
python -m src.api.server
```

API documentation: http://localhost:8000/docs

Example API call:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "search for demon slayer anime"}'
```

## Project Structure
```
src/
├── config.py              # Environment configuration
├── models.py              # MediaItem and UserPreferences models
├── clients/
│   ├── tmdb_client.py    # TMDB API client
│   └── anilist_client.py # AniList GraphQL client
├── tools/
│   ├── search_tools.py
│   ├── library_tools.py
│   └── recommendation_tools.py
├── agents/
│   ├── base_agent.py     # Base agent with Gemini integration
│   ├── orchestrator.py
│   ├── discovery_agent.py
│   ├── library_agent.py
│   └── recommender_agent.py
├── services/
│   ├── session_service.py
│   ├── memory_service.py
│   └── observability.py
├── evaluation/
│   └── evaluation_scenarios.py
└── api/
    └── server.py         # FastAPI server
```

## Evaluation

The automated test suite validates:
- Discovery Agent searches external APIs
- Library Agent adds and retrieves items
- Recommender Agent generates suggestions
- Session state persists across turns

Run with `python main.py`. All four tests should pass.

## Features

- Multi-agent system with specialized roles
- External API integration (TMDB, AniList)
- Custom tool calling with structured schemas
- Session and memory management
- Logging and metrics
- REST API with FastAPI
- CLI interface

## Tech Stack

- Python 3.11
- Google Gemini 2.0 Flash (google-generativeai SDK)
- FastAPI
- TMDB API
- AniList GraphQL API

## License

MIT License

## Author

OSAMA ALJAGHTHAMI  
Kaggle: @osamaaljaghthami

Built for Kaggle + Google Agents Intensive Capstone Project

## Acknowledgments

Google for the Agents Intensive course, TMDB and AniList for their APIs.