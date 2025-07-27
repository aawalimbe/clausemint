#!/usr/bin/env python
"""
Warmup script for Mistral AI model
This helps reduce the first request timeout issue
"""

import requests
import time
import json

def warmup_mistral():
    """Warm up the Mistral model with a simple streaming request"""
    print("🔥 Warming up Mistral AI model with streaming...")
    
    try:
        # Simple warmup request with streaming
        warmup_payload = {
            "model": "mistral",
            "prompt": "Hello, please respond with 'Model is ready'",
            "stream": True,
            "options": {
                "temperature": 0.1,
                "num_predict": 20
            }
        }
        
        print("Sending streaming warmup request...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=warmup_payload,
            stream=True,
            timeout=120
        )
        
        if response.status_code == 200:
            # Collect streaming response
            full_response = ""
            print("Receiving streaming response...")
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
                            print(f"Received: {chunk}", end='', flush=True)
                            
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing streaming response: {e}")
                        continue
            
            print(f"\n✅ Model warmed up successfully!")
            print(f"Full Response: {full_response}")
            return True
        else:
            print(f"❌ Warmup failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Warmup timed out - this is normal for the first request")
        return False
    except Exception as e:
        print(f"❌ Warmup error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Mistral AI Model Warmup")
    print("=" * 50)
    
    success = warmup_mistral()
    
    if success:
        print("\n🎉 Model is ready for NDA generation!")
        print("You can now try generating an NDA in the web interface.")
    else:
        print("\n⚠️  Model warmup had issues, but you can still try NDA generation.")
        print("The first request might take longer than usual.")
    
    print("=" * 50) 