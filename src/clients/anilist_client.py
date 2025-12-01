import requests
from typing import List, Dict, Any
from ..config import config
from ..models import MediaItem

class AniListClient:
    def __init__(self):
        self.api_url = config.ANILIST_API_URL
        
    def search_anime(self, query: str, limit: int = 10) -> List[MediaItem]:
        query_gql = """
        query ($search: String, $perPage: Int) {
          Page(page: 1, perPage: $perPage) {
            media(search: $search, type: ANIME) {
              id
              title { romaji english }
              description
              seasonYear
              genres
              averageScore
              episodes
              coverImage { large }
            }
          }
        }
        """
        return self._execute_query(query_gql, query, limit, "anime")
    
    def search_manga(self, query: str, limit: int = 10) -> List[MediaItem]:
        query_gql = """
        query ($search: String, $perPage: Int) {
          Page(page: 1, perPage: $perPage) {
            media(search: $search, type: MANGA) {
              id
              title { romaji english }
              description
              startDate { year }
              genres
              averageScore
              chapters
              coverImage { large }
            }
          }
        }
        """
        return self._execute_query(query_gql, query, limit, "manga")
    
    def _execute_query(self, query_gql: str, search: str, limit: int, media_type: str) -> List[MediaItem]:
        try:
            variables = {"search": search, "perPage": limit}
            response = requests.post(
                self.api_url,
                json={"query": query_gql, "variables": variables},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            items = []
            for result in data.get("data", {}).get("Page", {}).get("media", []):
                title = result.get("title", {}).get("english") or result.get("title", {}).get("romaji", "Unknown")
                year = result.get("seasonYear") or (result.get("startDate", {}).get("year") if result.get("startDate") else None)
                
                item = MediaItem(
                    id=f"anilist_{media_type}_{result['id']}",
                    source="anilist",
                    type=media_type,
                    title=title,
                    overview=result.get("description", "")[:500] if result.get("description") else "",
                    year=year,
                    genres=result.get("genres", []),
                    score=result.get("averageScore", 0) / 10 if result.get("averageScore") else None,
                    poster_url=result.get("coverImage", {}).get("large")
                )
                
                if media_type == "anime":
                    item.total_episodes = result.get("episodes")
                else:
                    item.total_chapters = result.get("chapters")
                    
                items.append(item)
            return items
        except Exception as e:
            print(f"AniList {media_type} search error: {e}")
            return []
