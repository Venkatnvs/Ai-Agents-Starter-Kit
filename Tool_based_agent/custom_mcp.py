from google.generativeai.types import GenerationConfig

class CustomMCP:
    def __init__(self, model, tools: list):
        self.model = model
        self.tools = {tool.name: tool for tool in tools}
        self.tool_schemas = [{
            "function_declarations": [{
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": tool.get_schema()["parameters"]["properties"],
                    "required": tool.get_schema()["parameters"].get("required", [])
                }
            }]
        } for tool in tools]

    def _execute_function_call(self, function_call) -> dict:
        function_name = function_call.name
        args = function_call.args
        if function_name not in self.tools:
            return {"status": "error", "message": f"Unknown function '{function_name}'"}
        tool = self.tools[function_name]
        try:
            return tool.execute(params=dict(args))
        except Exception as e:
            return {"status": "error", "message": f"Failed to execute tool: {str(e)}"}

    def chat(self, user_input: str) -> str:
        try:
            conversation = [{"role": "user", "parts": [{"text": user_input}]}]
            response = self.model.generate_content(
                conversation,
                generation_config=GenerationConfig(temperature=0.7),
                tools=self.tool_schemas
            )
            if response.candidates and response.candidates[0].content.parts:
                parts = response.candidates[0].content.parts
                function_responses = []
                
                for part in parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        function_response = self._execute_function_call(part.function_call)
                        function_responses.append({
                            "name": part.function_call.name,
                            "response": function_response
                        })
                if function_responses:
                    conversation.append(response.candidates[0].content)
                    conversation.append({
                        "role": "function",
                        "parts": [{"function_response": resp} for resp in function_responses]
                    })
                    
                    response = self.model.generate_content(
                        conversation,
                        generation_config=GenerationConfig(temperature=0.7),
                        tools=self.tool_schemas
                    )
            final_text = "".join(
                part.text for part in response.candidates[0].content.parts if hasattr(part, 'text')
            )
            return final_text.strip() if final_text else "I couldn't process your request."
        except Exception as e:
            return f"Sorry, an error occurred: {e}"
