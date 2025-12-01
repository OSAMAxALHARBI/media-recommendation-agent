from typing import List, Dict, Any
from ..clients.tmdb_client import TMDBClient
from ..clients.anilist_client import AniListClient
from ..models import MediaItem

class SearchTools:
    def __init__(self):
        self.tmdb = TMDBClient()
        self.anilist = AniListClient()
    
    def search_media(self, query: str, media_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        results = []
        
        if media_type == "movie":
            results = self.tmdb.search_movies(query, limit)
        elif media_type == "tv":
            results = self.tmdb.search_tv(query, limit)
        elif media_type == "anime":
            results = self.anilist.search_anime(query, limit)
        elif media_type == "manga":
            results = self.anilist.search_manga(query, limit)
        
        return [item.to_dict() for item in results]
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [{
            "name": "search_media",
            "description": "Search for anime, movies, TV shows, or manga. Returns detailed information including title, overview, score, and metadata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (title or keywords)"
                    },
                    "media_type": {
                        "type": "string",
                        "enum": ["anime", "movie", "tv", "manga"],
                        "description": "Type of media to search for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["query", "media_type"]
            }
        }]
