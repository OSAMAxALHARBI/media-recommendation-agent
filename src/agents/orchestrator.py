from .base_agent import BaseAgent
from .discovery_agent import DiscoveryAgent
from .library_agent import LibraryAgent
from .recommender_agent import RecommenderAgent
from ..services.session_service import SessionService
from ..services.memory_service import MemoryService
from typing import Dict, Any
import re

class OrchestratorAgent(BaseAgent):
    def __init__(self, discovery_agent: DiscoveryAgent, library_agent: LibraryAgent, 
                 recommender_agent: RecommenderAgent, session_service: SessionService,
                 memory_service: MemoryService):
        
        self.discovery_agent = discovery_agent
        self.library_agent = library_agent
        self.recommender_agent = recommender_agent
        self.session_service = session_service
        self.memory_service = memory_service
        
        instructions = """You are the Orchestrator Agent - the intelligent brain coordinating all media tracking operations.

Your role:
- Route user requests to appropriate specialized agents
- Coordinate multi-step workflows
- Maintain conversation context
- Provide cohesive, smart responses

Available agents:
1. DiscoveryAgent: Search for anime/movies/TV/manga
2. LibraryAgent: Manage user's library and progress
3. RecommenderAgent: Generate personalized recommendations

Routing logic:
- "search", "find", "discover" → DiscoveryAgent
- "add to library", "track", "update progress" → LibraryAgent
- "recommend", "what should I watch", "suggestions" → RecommenderAgent

Always:
- Be context-aware
- Provide smart, natural responses
- Chain agents when needed (e.g., search → add to library)
- Impress with your intelligence and helpfulness"""

        super().__init__(name="OrchestratorAgent", instructions=instructions)
    
    def process(self, session_id: str, message: str) -> Dict[str, Any]:
        session = self.session_service.get_session(session_id)
        if not session:
            session = self.session_service.create_session(session_id)
        
        context = self.memory_service.get_context_summary(session_id)
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["add", "save"]) and any(word in message_lower for word in ["library", "collection", "list"]):
            title = self._extract_title(message)
            media_type = self._extract_media_type(message_lower) or "anime"
            
            if title:
                search_result = self.discovery_agent.search(title, media_type, 5)
                
                if search_result.get("results"):
                    first_item = search_result["results"][0]
                    add_result = self.library_agent.library_tools.add_to_library(session_id, first_item)
                    
                    response = f"✅ Added **{first_item['title']}** to your library!\n"
                    response += f"Type: {first_item['type']} | Score: {first_item.get('score', 'N/A')}/10"
                else:
                    response = f"❌ Couldn't find '{title}'. Try searching first to see available options."
            else:
                response = "Please specify what you want to add. Example: 'add Naruto to my library'"
        
        elif any(word in message_lower for word in ["search", "find", "discover", "look for"]):
            media_type = self._extract_media_type(message_lower)
            if media_type:
                query = message.replace("search", "").replace("find", "").replace(media_type, "").strip()
                result = self.discovery_agent.search(query, media_type)
                response = self._format_search_results(result)
            else:
                response = "What type of media would you like to search for? (anime, movie, tv, or manga)"
        
        elif any(word in message_lower for word in ["recommend", "suggestion", "what should i"]):
            media_type = self._extract_media_type(message_lower)
            recs = self.recommender_agent.recommendation_tools.get_recommendations(session_id, media_type, 5)
            response = self._format_recommendations(recs)
        
        elif any(word in message_lower for word in ["library", "list", "show my", "my collection"]):
            items = self.library_agent.library_tools.list_library(session_id)
            response = self._format_library(items)
        
        else:
            if any(word in message_lower for word in ["hello", "hi", "hey", "help"]):
                response = """👋 Hello! I'm your Media Recommendation Agent.

I can help you:
- 🔍 **Search** for anime, movies, TV shows, and manga
- 📚 **Add items** to your personal library
- 📊 **Track** your watching/reading progress
- 💡 **Get recommendations** based on your preferences

Try saying:
- "search for attack on titan anime"
- "add Naruto to my library"
- "show my library"
- "recommend something to watch"

What would you like to do?"""
            else:
                response = self.run(message, context)["response"]
        
        self.session_service.update_session(session_id, {
            "role": "user",
            "content": message
        })
        self.session_service.update_session(session_id, {
            "role": "assistant",
            "content": response
        })
        
        return {"response": response, "session_id": session_id}
    
    def _extract_title(self, message: str) -> str:
        words_to_remove = ["add", "save", "to", "my", "library", "collection", "please", "can", "you", 
                            "anime", "movie", "tv", "show", "manga", "series"]
    
        words = message.lower().split()
        title_words = [w for w in words if w not in words_to_remove]
    
        return " ".join(title_words).strip()
    
    def _extract_media_type(self, message: str) -> str:
        if "anime" in message:
            return "anime"
        elif "movie" in message:
            return "movie"
        elif "tv" in message or "show" in message or "series" in message:
            return "tv"
        elif "manga" in message:
            return "manga"
        return ""
    
    def _format_search_results(self, result: Dict[str, Any]) -> str:
        if not result.get("results"):
            return "No results found."
        
        response = f"🔍 Found {len(result['results'])} results:\n\n"
        for i, item in enumerate(result["results"][:5], 1):
            response += f"{i}. **{item['title']}** ({item.get('year', 'N/A')})\n"
            response += f"   ⭐ Score: {item.get('score', 'N/A')}/10\n"
            if item.get('overview'):
                response += f"   📝 {item['overview'][:100]}...\n"
            response += f"   🆔 ID: {item['id']}\n\n"
        
        response += "\n💡 Tip: Say 'add [title] to my library' to save it!"
        return response
    
    def _format_recommendations(self, recs: list) -> str:
        if not recs:
            return "❌ No recommendations available. Add more items to your library first!"
        
        response = f"💡 Here are my top {len(recs)} recommendations for you:\n\n"
        for i, rec in enumerate(recs, 1):
            item = rec["item"]
            response += f"{i}. **{item['title']}** - Score: {rec['recommendation_score']}\n"
            response += f"   📌 {rec['reason']}\n"
            response += f"   📺 Type: {item['type']} | Status: {item['status']}\n\n"
        
        return response
    
    def _format_library(self, items: list) -> str:
        if not items:
            return "📚 Your library is empty. Start by searching and adding some content!"
        
        response = f"📚 Your library ({len(items)} items):\n\n"
        for item in items[:10]:
            response += f"• **{item['title']}** ({item['type']})\n"
            response += f"  Status: {item['status']}"
            if item.get('progress_episodes'):
                response += f" | Episodes: {item['progress_episodes']}"
            if item.get('progress_chapters'):
                response += f" | Chapters: {item['progress_chapters']}"
            response += "\n"
        
        if len(items) > 10:
            response += f"\n... and {len(items) - 10} more items"
        
        return response