"""LLM provider adapters.

Each adapter wraps a provider's API behind the common `BaseAdapter.generate()`
interface so the evaluation loop is provider-agnostic.
"""

from .mock_adapter import MockAdapter
from .openai_adapter import OpenAIAdapter
from .anthropic_adapter import AnthropicAdapter
from .google_adapter import GoogleAdapter

ADAPTERS = {
    "mock": MockAdapter,
    "openai": OpenAIAdapter,
    "anthropic": AnthropicAdapter,
    "google": GoogleAdapter,
}
