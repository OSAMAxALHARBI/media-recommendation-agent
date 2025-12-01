from ..agents.orchestrator import OrchestratorAgent
from ..services.session_service import SessionService
from ..services.memory_service import MemoryService
from ..services.observability import observability
import uuid

class AgentEvaluator:
    def __init__(self, orchestrator: OrchestratorAgent):
        self.orchestrator = orchestrator
        self.session_service = orchestrator.session_service
        self.memory_service = orchestrator.memory_service
    
    def run_evaluation(self):
        print("=" * 80)
        print("AGENT SYSTEM EVALUATION")
        print("=" * 80)
        
        results = []
        results.append(self.test_discovery())
        results.append(self.test_library_management())
        results.append(self.test_recommendations())
        results.append(self.test_multi_turn())
        
        passed = sum(1 for r in results if r["passed"])
        print(f"\n{'=' * 80}")
        print(f"RESULTS: {passed}/{len(results)} tests passed")
        print(f"Metrics: {observability.get_metrics()}")
        print(f"{'=' * 80}")
        
        return results
    
    def test_discovery(self) -> dict:
        print("\n[TEST 1] Discovery Agent - Search Functionality")
        session_id = str(uuid.uuid4())
        
        response = self.orchestrator.process(session_id, "search for attack on titan anime")
        
        passed = "found" in response["response"].lower() or "attack" in response["response"].lower()
        
        print(f"  Input: 'search for attack on titan anime'")
        print(f"  Output: {response['response'][:150]}...")
        print(f"  Status: {'✓ PASS' if passed else '✗ FAIL'}")
        
        return {"test": "discovery", "passed": passed}
    
    def test_library_management(self) -> dict:
        print("\n[TEST 2] Library Agent - Add and List Items")
        session_id = str(uuid.uuid4())
        
        from ..models import MediaItem
        item = MediaItem(
            id="test_anime_1",
            source="anilist",
            type="anime",
            title="Test Anime",
            overview="Test description",
            score=8.5
        )
        
        self.memory_service.add_media_item(session_id, item)
        
        response = self.orchestrator.process(session_id, "show my library")
        
        passed = "test anime" in response["response"].lower() and "library" in response["response"].lower()
        
        print(f"  Input: Added 1 item, then 'show my library'")
        print(f"  Output: {response['response'][:150]}...")
        print(f"  Status: {'✓ PASS' if passed else '✗ FAIL'}")
        
        return {"test": "library", "passed": passed}
    
    def test_recommendations(self) -> dict:
        print("\n[TEST 3] Recommender Agent - Generate Recommendations")
        session_id = str(uuid.uuid4())
        
        from ..models import MediaItem
        items = [
            MediaItem(id="a1", source="anilist", type="anime", title="Anime 1", 
                     overview="", score=9.0, status="planned", genres=["Action"]),
            MediaItem(id="m1", source="tmdb", type="movie", title="Movie 1", 
                     overview="", score=8.5, status="planned", genres=["Drama"])
        ]
        
        for item in items:
            self.memory_service.add_media_item(session_id, item)
        
        response = self.orchestrator.process(session_id, "recommend something to watch")
        
        passed = "recommendation" in response["response"].lower() or "anime" in response["response"].lower() or "movie" in response["response"].lower()
        
        print(f"  Input: Added 2 items, then 'recommend something to watch'")
        print(f"  Output: {response['response'][:150]}...")
        print(f"  Status: {'✓ PASS' if passed else '✗ FAIL'}")
        
        return {"test": "recommendations", "passed": passed}
    
    def test_multi_turn(self) -> dict:
        print("\n[TEST 4] Session Persistence - Multi-turn Conversation")
        session_id = str(uuid.uuid4())
        
        response1 = self.orchestrator.process(session_id, "Hello")
        response2 = self.orchestrator.process(session_id, "What can you help me with?")
        
        session = self.session_service.get_session(session_id)
        passed = len(session.conversation_history) >= 4
        
        print(f"  Input: Two-turn conversation")
        print(f"  Conversation length: {len(session.conversation_history)} messages")
        print(f"  Status: {'✓ PASS' if passed else '✗ FAIL'}")
        
        return {"test": "multi_turn", "passed": passed}