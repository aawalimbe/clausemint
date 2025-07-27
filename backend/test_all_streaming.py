#!/usr/bin/env python
"""
Comprehensive streaming test for all AI providers and features
"""

import requests
import json
import time
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core.ai_service import ai_service
from django.conf import settings

def test_mistral_streaming():
    """Test Mistral AI streaming directly"""
    print("🧪 Testing Mistral AI Streaming...")
    
    try:
        payload = {
            "model": "mistral",
            "prompt": "Write a short paragraph about legal documents.",
            "stream": True,
            "options": {
                "temperature": 0.3,
                "num_predict": 200
            }
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            stream=True,
            timeout=120
        )
        
        if response.status_code == 200:
            print("✅ Mistral streaming working:")
            full_response = ""
            chunk_count = 0
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = line.decode('utf-8')
                        if data.startswith('data: '):
                            data = data[6:]
                        
                        if data.strip() == '[DONE]':
                            break
                            
                        json_data = json.loads(data)
                        if 'response' in json_data:
                            chunk = json_data['response']
                            full_response += chunk
                            chunk_count += 1
                            print(f"  Chunk {chunk_count}: {chunk}", end='', flush=True)
                            
                    except json.JSONDecodeError:
                        continue
            
            print(f"\n  Total chunks: {chunk_count}, Length: {len(full_response)}")
            return True
        else:
            print(f"❌ Mistral streaming failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Mistral streaming error: {e}")
        return False

def test_ai_service_streaming():
    """Test AI service streaming wrapper"""
    print("\n🔧 Testing AI Service Streaming Wrapper...")
    
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a short paragraph about legal technology."}
        ]
        
        print("  Generating response...")
        response = ai_service.generate_response(messages, max_tokens=200, temperature=0.3)
        
        if response and len(response) > 0:
            print(f"✅ AI Service streaming working:")
            print(f"  Response length: {len(response)} characters")
            print(f"  Preview: {response[:100]}...")
            return True
        else:
            print("❌ AI Service returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ AI Service streaming error: {e}")
        return False

def test_nda_streaming_endpoint():
    """Test NDA streaming endpoint"""
    print("\n📄 Testing NDA Streaming Endpoint...")
    
    try:
        payload = {
            "party_a": "Test Company A",
            "party_b": "Test Company B",
            "nda_type": "two-way",
            "purpose": "Testing streaming functionality",
            "confidentiality_period": "2 years",
            "jurisdiction": "India"
        }
        
        print("  Sending NDA generation request...")
        response = requests.post(
            "http://localhost:8000/api/nda/generate/streaming/",
            json=payload,
            stream=True,
            timeout=300
        )
        
        if response.status_code == 200:
            print("✅ NDA streaming endpoint working:")
            status_count = 0
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = line.decode('utf-8')
                        if data.startswith('data: '):
                            data = data[6:]
                        
                        json_data = json.loads(data)
                        status_count += 1
                        
                        if json_data.get('status') == 'started':
                            print(f"  Status {status_count}: Started")
                        elif json_data.get('status') == 'completed':
                            print(f"  Status {status_count}: Completed")
                            content = json_data.get('content', '')
                            print(f"  Content length: {len(content)} characters")
                            return True
                        elif json_data.get('status') == 'error':
                            print(f"  Status {status_count}: Error - {json_data.get('error')}")
                            return False
                            
                    except json.JSONDecodeError:
                        continue
            
            print(f"  Total status updates: {status_count}")
            return True
        else:
            print(f"❌ NDA streaming endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ NDA streaming endpoint error: {e}")
        return False

def test_chat_streaming_endpoint():
    """Test chat streaming endpoint"""
    print("\n💬 Testing Chat Streaming Endpoint...")
    
    try:
        # First upload a test document
        test_content = "This is a test legal document for streaming chat functionality."
        
        upload_payload = {
            "title": "Test Document",
            "document_type": "test",
            "content": test_content
        }
        
        print("  Creating test document...")
        upload_response = requests.post(
            "http://localhost:8000/api/upload/",
            data=upload_payload
        )
        
        if upload_response.status_code != 201:
            print("❌ Failed to create test document")
            return False
        
        document_data = upload_response.json()
        document_id = document_data['id']
        
        # Test chat streaming
        chat_payload = {
            "document_id": document_id,
            "message": "What is this document about?"
        }
        
        print("  Sending chat streaming request...")
        chat_response = requests.post(
            "http://localhost:8000/api/chat/streaming/",
            json=chat_payload,
            stream=True,
            timeout=120
        )
        
        if chat_response.status_code == 200:
            print("✅ Chat streaming endpoint working:")
            status_count = 0
            
            for line in chat_response.iter_lines():
                if line:
                    try:
                        data = line.decode('utf-8')
                        if data.startswith('data: '):
                            data = data[6:]
                        
                        json_data = json.loads(data)
                        status_count += 1
                        
                        if json_data.get('status') == 'started':
                            print(f"  Status {status_count}: Started")
                        elif json_data.get('status') == 'completed':
                            print(f"  Status {status_count}: Completed")
                            response = json_data.get('response', '')
                            print(f"  Response length: {len(response)} characters")
                            return True
                        elif json_data.get('status') == 'error':
                            print(f"  Status {status_count}: Error - {json_data.get('error')}")
                            return False
                            
                    except json.JSONDecodeError:
                        continue
            
            return True
        else:
            print(f"❌ Chat streaming endpoint failed: {chat_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chat streaming endpoint error: {e}")
        return False

def main():
    """Run all streaming tests"""
    print("=" * 70)
    print("🚀 COMPREHENSIVE STREAMING TEST SUITE")
    print("=" * 70)
    
    # Check current AI provider
    current_provider = ai_service.get_current_provider()
    print(f"Current AI Provider: {current_provider}")
    print(f"Mistral Base URL: {getattr(settings, 'MISTRAL_BASE_URL', 'Not set')}")
    print()
    
    # Run tests
    tests = [
        ("Mistral Direct Streaming", test_mistral_streaming),
        ("AI Service Streaming", test_ai_service_streaming),
        ("NDA Streaming Endpoint", test_nda_streaming_endpoint),
        ("Chat Streaming Endpoint", test_chat_streaming_endpoint),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All streaming tests passed! Your AI system is fully functional.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print("=" * 70)

if __name__ == "__main__":
    main() 