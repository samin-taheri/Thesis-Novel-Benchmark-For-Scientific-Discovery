#!/bin/bash
# API Keys Setup Script
# Copy this file to setup_keys.sh and add your actual API keys

# OpenAI API Key
export OPENAI_API_KEY="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"

# Anthropic API Key  
export ANTHROPIC_API_KEY="your-anthropic-api-key-here"

# Google API Key
export GOOGLE_API_KEY="AIzaSyAqBRpo8pfuXwDVPZa0534VSeEoZbmR3FA"

# Optional: Add to your shell profile for persistence
# echo 'export OPENAI_API_KEY="your-key"' >> ~/.zshrc
# echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.zshrc  
# echo 'export GOOGLE_API_KEY="your-key"' >> ~/.zshrc

echo "API keys set! Run 'source setup_keys.sh' to activate them."
