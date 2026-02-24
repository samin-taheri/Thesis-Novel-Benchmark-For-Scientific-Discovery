#!/bin/bash
# API Keys Setup Script
# Copy this file to setup_keys.sh and add your actual API keys

# OpenAI API Key
export OPENAI_API_KEY="YOUR_OPENAI_KEY_HERE"

# Anthropic API Key
export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_KEY_HERE"

# Google API Key
export GOOGLE_API_KEY="YOUR_GOOGLE_KEY_HERE"

# Optional: Add to your shell profile for persistence
# echo 'export OPENAI_API_KEY="your-key"' >> ~/.zshrc
# echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.zshrc
# echo 'export GOOGLE_API_KEY="your-key"' >> ~/.zshrc

echo "API keys set! Run 'source setup_keys.sh' to activate them."
