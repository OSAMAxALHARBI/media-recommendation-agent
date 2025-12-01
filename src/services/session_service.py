from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class Session:
    session_id: str
    user_id: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_active: str = field(default_factory=lambda: datetime.now().isoformat())
    conversation_history: list = field(default_factory=list)
    workflow_state: Dict[str, Any] = field(default_factory=dict)

class SessionService:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
    
    def create_session(self, session_id: str, user_id: str = "default_user") -> Session:
        session = Session(session_id=session_id, user_id=user_id)
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, message: Dict[str, Any]):
        if session_id in self.sessions:
            self.sessions[session_id].conversation_history.append(message)
            self.sessions[session_id].last_active = datetime.now().isoformat()
    
    def save_workflow_state(self, session_id: str, state: Dict[str, Any]):
        if session_id in self.sessions:
            self.sessions[session_id].workflow_state = state
    
    def get_workflow_state(self, session_id: str) -> Dict[str, Any]:
        session = self.sessions.get(session_id)
        return session.workflow_state if session else {}