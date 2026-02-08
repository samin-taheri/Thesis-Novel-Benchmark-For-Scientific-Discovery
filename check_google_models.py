#!/usr/bin/env python3
"""
Check available Google Gemini models
"""

import os
import google.generativeai as genai

def check_google_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        return
    
    try:
        genai.configure(api_key=api_key)
        print("🔍 Checking available Google models...")
        
        models = genai.list_models()
        available_models = []
        
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
                print(f"✅ {model.name}")
        
        if available_models:
            print(f"\n🎯 Try these models in your YAML:")
            for model in available_models[:3]:  # Show first 3
                print(f"  model: {model.replace('models/', '')}")
        else:
            print("❌ No models found. Check your API key.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Possible issues:")
        print("  - API key is invalid")
        print("  - Network connectivity issues")
        print("  - Google API quotas")

if __name__ == "__main__":
    check_google_models()
