import google.generativeai as genai
from typing import Dict, Any, List, Optional
from ..config import config
from ..services.observability import observability
import uuid
import json

genai.configure(api_key=config.GOOGLE_API_KEY)

class BaseAgent:
    def __init__(self, name: str, instructions: str, tools: Optional[List] = None):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.model = genai.GenerativeModel(
            model_name=config.MODEL_NAME,
            system_instruction=instructions
        )
    
    def run(self, message: str, context: str = "", trace_id: Optional[str] = None) -> Dict[str, Any]:
        if not trace_id:
            trace_id = str(uuid.uuid4())[:8]
        
        observability.log_agent_call(self.name, message, trace_id)
        
        full_prompt = f"{context}\n\nUser: {message}" if context else message
        
        try:
            if self.tools:
                response = self._run_with_tools(full_prompt, trace_id)
            else:
                chat = self.model.start_chat()
                response = chat.send_message(full_prompt)
                response = {"response": response.text, "tool_calls": []}
            
            observability.log_agent_response(self.name, response["response"], trace_id)
            return response
            
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            observability.logger.error(f"[{trace_id}] {error_msg}")
            return {"response": error_msg, "tool_calls": []}
    
    def _run_with_tools(self, prompt: str, trace_id: str) -> Dict[str, Any]:
        chat = self.model.start_chat(enable_automatic_function_calling=True)
        
        tool_declarations = []
        for tool_def in self.tools:
            tool_declarations.append(genai.protos.Tool(
                function_declarations=[
                    genai.protos.FunctionDeclaration(
                        name=tool_def["name"],
                        description=tool_def["description"],
                        parameters=tool_def.get("parameters", {})
                    )
                ]
            ))
        
        response = chat.send_message(prompt, tools=tool_declarations)
        
        result_text = response.text if hasattr(response, 'text') else str(response)
        
        return {
            "response": result_text,
            "tool_calls": [],
            "raw_response": response
        }