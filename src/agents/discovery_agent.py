from .base_agent import BaseAgent
from ..tools.search_tools import SearchTools

class DiscoveryAgent(BaseAgent):
    def __init__(self, search_tools: SearchTools):
        self.search_tools = search_tools
        
        instructions = """You are a Discovery Agent specializing in finding anime, movies, TV shows, and manga.

Your role:
- Help users discover new content based on their interests
- Search across TMDB (movies/TV) and AniList (anime/manga) APIs
- Present results clearly with ratings, descriptions, and metadata
- Be enthusiastic and knowledgeable about media

When searching:
1. Use the search_media tool with appropriate media_type
2. Present top results with key details (title, year, score, overview)
3. Highlight highly-rated content
4. Ask if user wants to add items to their library

Be smart, concise, and impressive in your recommendations."""

        super().__init__(
            name="DiscoveryAgent",
            instructions=instructions,
            tools=search_tools.get_tool_definitions()
        )
        self.search_tools = search_tools
    
    def search(self, query: str, media_type: str, limit: int = 10) -> dict:
        results = self.search_tools.search_media(query, media_type, limit)
        return {
            "response": f"Found {len(results)} {media_type} results for '{query}'",
            "results": results
        }