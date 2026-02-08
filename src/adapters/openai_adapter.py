from .base import BaseAdapter
from typing import Dict, Any
import os
import openai

class OpenAIAdapter(BaseAdapter):
    def __init__(self, model: str, temperature: float, top_p: float, max_tokens: int, tools=None):
        super().__init__(model, temperature, top_p, max_tokens, tools)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required.\n"
                "To fix this:\n"
                "1. Get an API key from https://platform.openai.com/api-keys\n"
                "2. Set it: export OPENAI_API_KEY='sk-your-key-here'\n"
                "3. Or use mock adapter by changing 'provider: openai' to 'provider: mock' in your YAML"
            )
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate(self, prompt: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens
            )
            
            content = response.choices[0].message.content or ""
            
            # Extract rationale (everything after "Rationale:" if present)
            parts = content.split("Rationale:", 1)
            if len(parts) == 2:
                prediction = parts[0].strip()
                rationale = parts[1].strip()
            else:
                prediction = content.strip()
                rationale = "Generated scientific hypothesis using language model reasoning."
            
            return {
                "content": prediction,
                "rationale": rationale,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            # Fallback for errors
            return {
                "content": f"Error: {str(e)}",
                "rationale": "Failed to generate response due to API error.",
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            }
