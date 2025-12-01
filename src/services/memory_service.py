from typing import Dict, List, Optional
from ..models import MediaItem, UserPreferences

class MemoryService:
    def __init__(self):
        self.libraries: Dict[str, List[MediaItem]] = {}
        self.preferences: Dict[str, UserPreferences] = {}
    
    def add_media_item(self, session_id: str, item: MediaItem):
        if session_id not in self.libraries:
            self.libraries[session_id] = []
        
        existing_ids = [i.id for i in self.libraries[session_id]]
        if item.id not in existing_ids:
            self.libraries[session_id].append(item)
            self._update_preferences(session_id, item)
    
    def get_library(self, session_id: str, media_type: Optional[str] = None, 
                   status: Optional[str] = None) -> List[MediaItem]:
        items = self.libraries.get(session_id, [])
        
        if media_type:
            items = [i for i in items if i.type == media_type]
        if status:
            items = [i for i in items if i.status == status]
        
        return items
    
    def update_progress(self, session_id: str, item_id: str, 
                       episodes: Optional[int], chapters: Optional[int], 
                       status: Optional[str]) -> bool:
        items = self.libraries.get(session_id, [])
        for item in items:
            if item.id == item_id:
                if episodes is not None:
                    item.progress_episodes = episodes
                if chapters is not None:
                    item.progress_chapters = chapters
                if status:
                    item.status = status
                return True
        return False
    
    def get_preferences(self, session_id: str) -> UserPreferences:
        if session_id not in self.preferences:
            self.preferences[session_id] = UserPreferences()
        return self.preferences[session_id]
    
    def _update_preferences(self, session_id: str, item: MediaItem):
        prefs = self.get_preferences(session_id)
        
        if item.score and item.score >= 8:
            for genre in item.genres:
                if genre not in prefs.favorite_genres:
                    prefs.favorite_genres.append(genre)
    
    def get_context_summary(self, session_id: str) -> str:
        library = self.get_library(session_id)
        prefs = self.get_preferences(session_id)
        
        summary = f"Library: {len(library)} items\n"
        
        types = {}
        statuses = {}
        for item in library:
            types[item.type] = types.get(item.type, 0) + 1
            statuses[item.status] = statuses.get(item.status, 0) + 1
        
        summary += f"Types: {types}\n"
        summary += f"Statuses: {statuses}\n"
        summary += f"Favorite genres: {', '.join(prefs.favorite_genres[:5])}\n"
        
        return summary