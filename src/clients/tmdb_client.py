import requests
from typing import List, Dict, Any, Optional
from ..config import config
from ..models import MediaItem

class TMDBClient:
    def __init__(self):
        self.api_key = config.TMDB_API_KEY
        self.base_url = config.TMDB_BASE_URL
        
    def search_movies(self, query: str, limit: int = 10) -> List[MediaItem]:
        try:
            url = f"{self.base_url}/search/movie"
            params = {"api_key": self.api_key, "query": query, "page": 1}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            items = []
            for result in data.get("results", [])[:limit]:
                items.append(MediaItem(
                    id=f"tmdb_movie_{result['id']}",
                    source="tmdb",
                    type="movie",
                    title=result.get("title", "Unknown"),
                    overview=result.get("overview", ""),
                    year=int(result.get("release_date", "")[:4]) if result.get("release_date") else None,
                    genres=[],
                    score=result.get("vote_average"),
                    poster_url=f"https://image.tmdb.org/t/p/w500{result.get('poster_path')}" if result.get('poster_path') else None
                ))
            return items
        except Exception as e:
            print(f"TMDB movie search error: {e}")
            return []
    
    def search_tv(self, query: str, limit: int = 10) -> List[MediaItem]:
        try:
            url = f"{self.base_url}/search/tv"
            params = {"api_key": self.api_key, "query": query, "page": 1}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            items = []
            for result in data.get("results", [])[:limit]:
                tv_id = result['id']
                detail = self._get_tv_details(tv_id)
                
                items.append(MediaItem(
                    id=f"tmdb_tv_{tv_id}",
                    source="tmdb",
                    type="tv",
                    title=result.get("name", "Unknown"),
                    overview=result.get("overview", ""),
                    year=int(result.get("first_air_date", "")[:4]) if result.get("first_air_date") else None,
                    genres=[],
                    score=result.get("vote_average"),
                    total_episodes=detail.get("number_of_episodes"),
                    poster_url=f"https://image.tmdb.org/t/p/w500{result.get('poster_path')}" if result.get('poster_path') else None
                ))
            return items
        except Exception as e:
            print(f"TMDB TV search error: {e}")
            return []
    
    def _get_tv_details(self, tv_id: int) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/tv/{tv_id}"
            params = {"api_key": self.api_key}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except:
            return {}