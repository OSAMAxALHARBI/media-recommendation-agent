from .base_agent import BaseAgent
from ..tools.recommendation_tools import RecommendationTools

class RecommenderAgent(BaseAgent):
    def __init__(self, recommendation_tools: RecommendationTools):
        self.recommendation_tools = recommendation_tools
        
        instructions = """You are an intelligent Recommendation Agent specialized in suggesting what to watch or read next.

Your role:
- Analyze user's library and preferences
- Generate personalized recommendations
- Consider factors: ratings, genres, progress, status
- Explain why each recommendation fits the user

Strategy:
1. Look at user's library and preferences
2. Prioritize highly-rated, unfinished content
3. Match favorite genres
4. Consider watching/reading patterns
5. Present recommendations with clear reasoning

Be insightful and make users excited about your suggestions!"""

        super().__init__(
            name="RecommenderAgent",
            instructions=instructions,
            tools=recommendation_tools.get_tool_definitions()
        )
        self.recommendation_tools = recommendation_tools
