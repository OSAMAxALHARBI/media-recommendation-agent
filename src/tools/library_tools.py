from typing import List, Dict, Any, Optional
from ..models import MediaItem
from ..services.memory_service import MemoryService

class LibraryTools:
    def __init__(self, memory_service: MemoryService):
        self.memory = memory_service
    
    def add_to_library(self, session_id: str, media_item: Dict[str, Any]) -> Dict[str, Any]:
        item = MediaItem.from_dict(media_item)
        self.memory.add_media_item(session_id, item)
        return {"success": True, "message": f"Added '{item.title}' to library", "item": item.to_dict()}
    
    def update_progress(self, session_id: str, item_id: str, episodes: Optional[int] = None, 
                       chapters: Optional[int] = None, status: Optional[str] = None) -> Dict[str, Any]:
        success = self.memory.update_progress(session_id, item_id, episodes, chapters, status)
        if success:
            return {"success": True, "message": "Progress updated"}
        return {"success": False, "message": "Item not found"}
    
    def list_library(self, session_id: str, media_type: Optional[str] = None, 
                    status: Optional[str] = None) -> List[Dict[str, Any]]:
        items = self.memory.get_library(session_id, media_type, status)
        return [item.to_dict() for item in items]
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "add_to_library",
                "description": "Add a media item (anime/movie/TV/manga) to the user's library. Use search results to get the complete media_item object.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "media_item": {
                            "type": "object",
                            "description": "Complete media item object from search results"
                        }
                    },
                    "required": ["media_item"]
                }
            },
            {
                "name": "update_progress",
                "description": "Update watching/reading progress for a library item",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item_id": {"type": "string", "description": "Media item ID"},
                        "episodes": {"type": "integer", "description": "Episodes watched (for anime/TV)"},
                        "chapters": {"type": "integer", "description": "Chapters read (for manga)"},
                        "status": {
                            "type": "string",
                            "enum": ["watching", "reading", "completed", "dropped", "planned", "on_hold"],
                            "description": "New status"
                        }
                    },
                    "required": ["item_id"]
                }
            },
            {
                "name": "list_library",
                "description": "List all items in the user's library with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "media_type": {
                            "type": "string",
                            "enum": ["anime", "movie", "tv", "manga"],
                            "description": "Filter by media type (optional)"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["watching", "reading", "completed", "dropped", "planned", "on_hold"],
                            "description": "Filter by status (optional)"
                        }
                    }
                }
            }
        ]
