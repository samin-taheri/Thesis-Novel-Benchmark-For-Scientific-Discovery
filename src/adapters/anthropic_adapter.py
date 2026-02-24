from .base import BaseAdapter
from typing import Dict, Any
import os
import anthropic

class AnthropicAdapter(BaseAdapter):
    def __init__(self, model: str, temperature: float, top_p: float, max_tokens: int, tools=None):
        super().__init__(model, temperature, top_p, max_tokens, tools)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is required.\n"
                "To fix this:\n"
                "1. Get an API key from https://console.anthropic.com/\n"
                "2. Set it, e.g.: export ANTHROPIC_API_KEY='YOUR_ANTHROPIC_KEY_HERE'\n"
                "3. Or use the mock adapter by changing 'provider: anthropic' to 'provider: mock' in your YAML"
            )
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate(self, prompt: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text if response.content else ""
            
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
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            }
        except Exception as e:
            # Fallback for errors
            return {
                "content": f"Error: {str(e)}",
                "rationale": "Failed to generate response due to API error.",
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            }
