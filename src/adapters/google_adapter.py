from .base import BaseAdapter
from typing import Dict, Any
import os
import google.generativeai as genai

class GoogleAdapter(BaseAdapter):
    def __init__(self, model: str, temperature: float, top_p: float, max_tokens: int, tools=None):
        super().__init__(model, temperature, top_p, max_tokens, tools)
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is required.\n"
                "To fix this:\n"
                "1. Get an API key from https://ai.google.dev/\n"
                "2. Set it, e.g.: export GOOGLE_API_KEY='YOUR_GOOGLE_KEY_HERE'\n"
                "3. Or use mock adapter by changing 'provider: google' to 'provider: mock' in your YAML"
            )
        genai.configure(api_key=api_key)
        self.model_instance = genai.GenerativeModel(model)
    
    def generate(self, prompt: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        try:
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p
            )
            
            response = self.model_instance.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            content = response.text if response.text else ""
            
            # Extract rationale (everything after "Rationale:" if present)
            parts = content.split("Rationale:", 1)
            if len(parts) == 2:
                prediction = parts[0].strip()
                rationale = parts[1].strip()
            else:
                prediction = content.strip()
                rationale = "Generated scientific hypothesis using language model reasoning."
            
            # Google API doesn't provide detailed token counts in the same way
            # Estimate tokens as rough word count
            prompt_tokens = len(prompt.split())
            completion_tokens = len(content.split())
            
            return {
                "content": prediction,
                "rationale": rationale,
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens
                }
            }
        except Exception as e:
            # Fallback for errors
            return {
                "content": f"Error: {str(e)}",
                "rationale": "Failed to generate response due to API error.",
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            }
