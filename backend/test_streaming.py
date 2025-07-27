#!/usr/bin/env python
"""
Test script for streaming functionality
"""

import requests
import json
import time

def test_streaming():
    """Test streaming with a simple request"""
    print("🧪 Testing Mistral AI Streaming...")
    
    try:
        # Test payload
        payload = {
            "model": "mistral",
            "prompt": "Write a short paragraph about legal documents.",
            "stream": True,
            "options": {
                "temperature": 0.3,
                "num_predict": 200
            }
        }
        
        print("Sending streaming request...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            stream=True,
            timeout=120
        )
        
        if response.status_code == 200:
            print("✅ Streaming response received:")
            print("-" * 50)
            
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
                            print(f"Chunk {chunk_count}: {chunk}", end='', flush=True)
                            
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing chunk: {e}")
                        continue
            
            print(f"\n\n✅ Streaming completed successfully!")
            print(f"Total chunks received: {chunk_count}")
            print(f"Full response length: {len(full_response)} characters")
            print(f"Response: {full_response}")
            return True
            
        else:
            print(f"❌ Streaming failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Streaming timed out")
        return False
    except Exception as e:
        print(f"❌ Streaming error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Mistral AI Streaming Test")
    print("=" * 60)
    
    success = test_streaming()
    
    if success:
        print("\n🎉 Streaming is working correctly!")
        print("You can now use streaming for NDA generation.")
    else:
        print("\n⚠️  Streaming test failed.")
        print("Check if Ollama is running and Mistral model is available.")
    
    print("=" * 60) 