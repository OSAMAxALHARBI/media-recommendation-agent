from typing import List, Dict, Any, Optional
from ..services.memory_service import MemoryService
from ..models import MediaItem

class RecommendationTools:
    def __init__(self, memory_service: MemoryService):
        self.memory = memory_service
    
    def get_recommendations(self, session_id: str, media_type: Optional[str] = None, 
                          count: int = 5) -> List[Dict[str, Any]]:
        library = self.memory.get_library(session_id, media_type)
        prefs = self.memory.get_preferences(session_id)
        
        recommendations = []
        for item in library:
            if item.status in ["completed", "dropped"]:
                continue
                
            score = 0.0
            
            if item.score:
                score += item.score * 10
            
            for genre in item.genres:
                if genre in prefs.favorite_genres:
                    score += 15
            
            if item.status == "planned":
                score += 10
            
            if item.type in ["anime", "tv"] and item.total_episodes:
                progress_ratio = item.progress_episodes / item.total_episodes
                if progress_ratio > 0.3:
                    score += 20 * progress_ratio
            
            recommendations.append({
                "item": item.to_dict(),
                "recommendation_score": round(score, 2),
                "reason": self._generate_reason(item, prefs, score)
            })
        
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return recommendations[:count]
    
    def _generate_reason(self, item: MediaItem, prefs, score: float) -> str:
        reasons = []
        if item.score and item.score >= 8:
            reasons.append(f"highly rated ({item.score}/10)")
        if any(g in prefs.favorite_genres for g in item.genres):
            reasons.append("matches your favorite genres")
        if item.status == "planned":
            reasons.append("in your plan to watch/read")
        return ", ".join(reasons) if reasons else "good match for you"
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [{
            "name": "get_recommendations",
            "description": "Get personalized recommendations from the user's library based on preferences and watching/reading patterns",
            "parameters": {
                "type": "object",
                "properties": {
                    "media_type": {
                        "type": "string",
                        "enum": ["anime", "movie", "tv", "manga"],
                        "description": "Filter recommendations by type (optional)"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of recommendations (default: 5)",
                        "default": 5
                    }
                }
            }
        }]
