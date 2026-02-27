"""Google Gemini adapter for the benchmark pipeline.

Uses the google-generativeai SDK to call Gemini models.
Includes automatic retry with exponential back-off for free-tier
rate limits (HTTP 429).
"""

import os
import time

import google.generativeai as genai

from typing import Dict, Any
from .base import BaseAdapter

# Retry settings for free-tier rate limits
_MAX_RETRIES = 5
_INITIAL_WAIT = 15  # seconds


class GoogleAdapter(BaseAdapter):
    """Adapter that wraps Google Generative AI (Gemini) models."""

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
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
        )

        # Retry loop to handle free-tier 429 rate limits
        last_err: Exception | None = None
        for attempt in range(_MAX_RETRIES):
            try:
                response = self.model_instance.generate_content(
                    prompt,
                    generation_config=generation_config,
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

                # Estimate token counts from word counts
                prompt_tokens = len(prompt.split())
                completion_tokens = len(content.split())

                return {
                    "content": prediction,
                    "rationale": rationale,
                    "usage": {
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": prompt_tokens + completion_tokens,
                    },
                }
            except Exception as e:
                last_err = e
                err_str = str(e)
                if "429" in err_str or "quota" in err_str.lower():
                    wait = _INITIAL_WAIT * (2 ** attempt)
                    print(f"  [rate-limit] attempt {attempt + 1}/{_MAX_RETRIES}, waiting {wait}s …")
                    time.sleep(wait)
                    continue
                # Non-retryable error — break immediately
                break

        # All retries exhausted or non-retryable error
        return {
            "content": f"Error: {str(last_err)}",
            "rationale": "Failed to generate response due to API error.",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }
