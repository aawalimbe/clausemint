#!/usr/bin/env python
"""
Test script to check AI service connectivity
"""

import os
import sys
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core.ai_service import ai_service
from django.conf import settings

def test_ai_connectivity():
    """Test AI service connectivity and provide diagnostics"""
    
    print("🔍 AI Service Connectivity Test")
    print("=" * 50)
    
    # Check current provider
    current_provider = ai_service.get_current_provider()
    print(f"Current AI Provider: {current_provider}")
    
    # Test connection
    print("\n📡 Testing Connection...")
    connection_status = ai_service.test_connection()
    
    print(f"Status: {connection_status['status']}")
    if connection_status['status'] == 'error':
        print(f"Error: {connection_status['message']}")
    
    # Provider-specific checks
    if current_provider == 'mistral':
        print("\n🔧 Mistral AI (Ollama) Diagnostics:")
        print("- Checking if Ollama is running...")
        
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code == 200:
                print("✅ Ollama is running!")
                models = response.json()
                print(f"Available models: {[model['name'] for model in models.get('models', [])]}")
            else:
                print("❌ Ollama is not responding properly")
        except requests.exceptions.ConnectionError:
            print("❌ Ollama is not running or not accessible")
            print("\n💡 To fix this:")
            print("1. Install Ollama: https://ollama.ai/")
            print("2. Run: ollama serve")
            print("3. Pull Mistral model: ollama pull mistral")
        except Exception as e:
            print(f"❌ Error checking Ollama: {e}")
    
    elif current_provider == 'openai':
        print("\n🔧 OpenAI Diagnostics:")
        openai_key = getattr(settings, 'OPENAI_API_KEY', None)
        if openai_key:
            print("✅ OpenAI API key is configured")
        else:
            print("❌ OpenAI API key is not configured")
            print("\n💡 To fix this:")
            print("1. Get an API key from: https://platform.openai.com/")
            print("2. Add OPENAI_API_KEY to your .env file")
    
    # Test AI generation
    print("\n🧪 Testing AI Generation...")
    try:
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, AI is working!'"}
        ]
        
        response = ai_service.generate_response(test_messages, max_tokens=50)
        print(f"✅ AI Response: {response}")
        
    except Exception as e:
        print(f"❌ AI Generation Failed: {e}")
        print("\n💡 Troubleshooting:")
        if current_provider == 'mistral':
            print("- Install and run Ollama")
            print("- Or switch to OpenAI by setting AI_PROVIDER=openai in .env")
        elif current_provider == 'openai':
            print("- Configure OpenAI API key")
            print("- Or switch to Mistral by setting AI_PROVIDER=mistral in .env")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_ai_connectivity() 