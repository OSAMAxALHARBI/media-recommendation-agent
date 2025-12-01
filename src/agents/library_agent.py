from .base_agent import BaseAgent
from ..tools.library_tools import LibraryTools

class LibraryAgent(BaseAgent):
    def __init__(self, library_tools: LibraryTools):
        self.library_tools = library_tools
        
        instructions = """You are a Library Management Agent for tracking anime, movies, TV shows, and manga.

Your role:
- Manage user's personal media library
- Track watching/reading progress
- Update statuses (watching, completed, dropped, etc.)
- List and filter library contents

Capabilities:
- Add items to library (from search results)
- Update progress (episodes watched, chapters read)
- Change status
- List items with filters

Be organized, accurate, and helpful in managing the user's collection."""

        super().__init__(
            name="LibraryAgent",
            instructions=instructions,
            tools=library_tools.get_tool_definitions()
        )
        self.library_tools = library_tools
