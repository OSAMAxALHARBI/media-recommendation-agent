from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

from ..agents.orchestrator import OrchestratorAgent
from ..agents.discovery_agent import DiscoveryAgent
from ..agents.library_agent import LibraryAgent
from ..agents.recommender_agent import RecommenderAgent
from ..tools.search_tools import SearchTools
from ..tools.library_tools import LibraryTools
from ..tools.recommendation_tools import RecommendationTools
from ..services.session_service import SessionService
from ..services.memory_service import MemoryService
from ..services.observability import observability

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

app = FastAPI(title="Media Recommendation Agent System", version="1.0.0")

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        result = orchestrator.process(session_id, request.message)
        return ChatResponse(
            response=result["response"],
            session_id=result["session_id"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "metrics": observability.get_metrics()}

@app.get("/library/{session_id}")
async def get_library(session_id: str):
    items = library_tools.list_library(session_id)
    return {"session_id": session_id, "items": items}

def cli_main():
    print("Media Recommendation Agent System")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input or user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            result = orchestrator.process(session_id, user_input)
            print(f"\nAssistant: {result['response']}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if "--cli" in sys.argv:
        cli_main()
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
