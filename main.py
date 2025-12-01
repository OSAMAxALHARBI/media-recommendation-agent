#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.orchestrator import OrchestratorAgent
from src.agents.discovery_agent import DiscoveryAgent
from src.agents.library_agent import LibraryAgent
from src.agents.recommender_agent import RecommenderAgent
from src.tools.search_tools import SearchTools
from src.tools.library_tools import LibraryTools
from src.tools.recommendation_tools import RecommendationTools
from src.services.session_service import SessionService
from src.services.memory_service import MemoryService
from src.evaluation.evaluation_scenarios import AgentEvaluator

def main():
    print("Initializing Media Recommendation Agent System...")
    
    session_service = SessionService()
    memory_service = MemoryService()
    
    search_tools = SearchTools()
    library_tools = LibraryTools(memory_service)
    recommendation_tools = RecommendationTools(memory_service)
    
    discovery_agent = DiscoveryAgent(search_tools)
    library_agent = LibraryAgent(library_tools)
    recommender_agent = RecommenderAgent(recommendation_tools)
    orchestrator = OrchestratorAgent(
        discovery_agent, library_agent, recommender_agent,
        session_service, memory_service
    )
    
    evaluator = AgentEvaluator(orchestrator)
    evaluator.run_evaluation()
    
    print("\n" + "=" * 80)
    print("System ready! Start the server with:")
    print("  python -m src.api.server")
    print("Or use CLI mode:")
    print("  python -m src.api.server --cli")
    print("=" * 80)

if __name__ == "__main__":
    main()