import logging
from datetime import datetime
from typing import Dict, Any
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ObservabilityService:
    def __init__(self):
        self.logger = logging.getLogger("MediaAgentSystem")
        self.metrics = {
            "agent_calls": 0,
            "tool_calls": 0,
            "recommendations_generated": 0,
            "items_added": 0,
            "searches_performed": 0
        }
    
    def log_agent_call(self, agent_name: str, input_data: Any, trace_id: str):
        self.logger.info(f"[{trace_id}] Agent: {agent_name} | Input: {str(input_data)[:100]}")
        self.metrics["agent_calls"] += 1
    
    def log_agent_response(self, agent_name: str, response: Any, trace_id: str):
        self.logger.info(f"[{trace_id}] Agent: {agent_name} | Response: {str(response)[:100]}")
    
    def log_tool_call(self, tool_name: str, params: Dict[str, Any], trace_id: str):
        self.logger.info(f"[{trace_id}] Tool: {tool_name} | Params: {params}")
        self.metrics["tool_calls"] += 1
        
        if tool_name == "search_media":
            self.metrics["searches_performed"] += 1
        elif tool_name == "add_to_library":
            self.metrics["items_added"] += 1
        elif tool_name == "get_recommendations":
            self.metrics["recommendations_generated"] += 1
    
    def log_tool_result(self, tool_name: str, result: Any, trace_id: str):
        self.logger.info(f"[{trace_id}] Tool: {tool_name} | Result: {str(result)[:100]}")
    
    def get_metrics(self) -> Dict[str, int]:
        return self.metrics.copy()

observability = ObservabilityService()