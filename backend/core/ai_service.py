import os
from django.conf import settings
from openai import OpenAI
import requests
import json


class AIService:
    """AI Service class to handle both OpenAI and Mistral AI providers"""
    
    def __init__(self):
        self.provider = getattr(settings, 'AI_PROVIDER', 'mistral')
        self.openai_client = None
        self.mistral_base_url = getattr(settings, 'MISTRAL_BASE_URL', 'http://localhost:11434')
        
        if self.provider == 'openai':
            openai_api_key = getattr(settings, 'OPENAI_API_KEY')
            if openai_api_key:
                self.openai_client = OpenAI(api_key=openai_api_key)
    
    def generate_response(self, messages, model=None, max_tokens=1000, temperature=0.3):
        """Generate AI response using the configured provider"""
        if self.provider == 'mistral':
            try:
                return self._generate_mistral_response(messages, model, max_tokens, temperature)
            except Exception as e:
                print(f"Mistral failed, trying OpenAI fallback: {e}")
                # Fallback to OpenAI if Mistral fails
                if self.openai_client:
                    return self._generate_openai_response(messages, model, max_tokens, temperature)
                else:
                    raise Exception("Mistral AI is not available and OpenAI is not configured. Please install Ollama or configure OpenAI API key.")
        elif self.provider == 'openai':
            return self._generate_openai_response(messages, model, max_tokens, temperature)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    def _generate_mistral_response(self, messages, model=None, max_tokens=1000, temperature=0.3):
        """Generate response using local Mistral via Ollama with streaming"""
        if not model:
            model = "mistral"  # Default Mistral model
        
        # Convert messages to Ollama format
        prompt = self._convert_messages_to_prompt(messages)
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,  # Enable streaming
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = requests.post(
                f"{self.mistral_base_url}/api/generate",
                json=payload,
                stream=True,  # Enable streaming in requests
                timeout=300  # 5 minutes for streaming
            )
            response.raise_for_status()
            
            # Collect streaming response
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        # Parse JSON from each line
                        data = line.decode('utf-8')
                        if data.startswith('data: '):
                            data = data[6:]  # Remove 'data: ' prefix
                        
                        if data.strip() == '[DONE]':
                            break
                            
                        json_data = json.loads(data)
                        if 'response' in json_data:
                            full_response += json_data['response']
                            
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing streaming response: {e}")
                        continue
            
            return full_response.strip()
            
        except requests.exceptions.Timeout as e:
            print(f"Mistral API timeout: {e}")
            raise Exception("Mistral AI is taking too long to respond. Please try again.")
        except requests.exceptions.RequestException as e:
            print(f"Mistral API error: {e}")
            # Raise exception to trigger fallback
            raise Exception(f"Mistral AI connection failed: {str(e)}")
    
    def _generate_openai_response(self, messages, model=None, max_tokens=1000, temperature=0.3):
        """Generate response using OpenAI with streaming"""
        if not self.openai_client:
            raise ValueError("OpenAI client not configured")
        
        if not model:
            model = "gpt-4"  # Default OpenAI model
        
        try:
            # Use streaming for OpenAI as well
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True  # Enable streaming
            )
            
            # Collect streaming response
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
            
            return full_response
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "I apologize, but I'm having trouble connecting to the AI service. Please try again later."
    
    def _convert_messages_to_prompt(self, messages):
        """Convert OpenAI-style messages to a single prompt for Mistral"""
        prompt = ""
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            if role == 'system':
                prompt += f"System: {content}\n\n"
            elif role == 'user':
                prompt += f"User: {content}\n\n"
            elif role == 'assistant':
                prompt += f"Assistant: {content}\n\n"
        
        prompt += "Assistant: "
        return prompt
    
    def switch_provider(self, provider):
        """Switch between AI providers"""
        if provider not in ['mistral', 'openai']:
            raise ValueError("Provider must be 'mistral' or 'openai'")
        
        self.provider = provider
        return f"Switched to {provider} provider"
    
    def get_current_provider(self):
        """Get the current AI provider"""
        return self.provider
    
    def test_connection(self):
        """Test the connection to the current AI provider"""
        if self.provider == 'mistral':
            try:
                response = requests.get(f"{self.mistral_base_url}/api/tags", timeout=10)
                if response.status_code == 200:
                    # Try to warm up the model with a simple streaming request
                    try:
                        warmup_payload = {
                            "model": "mistral",
                            "prompt": "Hello",
                            "stream": True,
                            "options": {
                                "temperature": 0.1,
                                "num_predict": 10
                            }
                        }
                        warmup_response = requests.post(
                            f"{self.mistral_base_url}/api/generate",
                            json=warmup_payload,
                            stream=True,
                            timeout=30
                        )
                        if warmup_response.status_code == 200:
                            # Collect streaming response
                            for line in warmup_response.iter_lines():
                                if line:
                                    try:
                                        data = line.decode('utf-8')
                                        if data.startswith('data: '):
                                            data = data[6:]
                                        if data.strip() == '[DONE]':
                                            break
                                    except:
                                        continue
                            return {"status": "connected", "provider": "mistral", "models": response.json(), "warmed_up": True}
                        else:
                            return {"status": "connected", "provider": "mistral", "models": response.json(), "warmed_up": False}
                    except:
                        return {"status": "connected", "provider": "mistral", "models": response.json(), "warmed_up": False}
                else:
                    return {"status": "error", "provider": "mistral", "message": "Connection failed"}
            except Exception as e:
                return {"status": "error", "provider": "mistral", "message": str(e)}
        
        elif self.provider == 'openai':
            if not self.openai_client:
                return {"status": "error", "provider": "openai", "message": "OpenAI client not configured"}
            
            try:
                # Simple test call
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                return {"status": "connected", "provider": "openai"}
            except Exception as e:
                return {"status": "error", "provider": "openai", "message": str(e)}
        
        return {"status": "error", "provider": "unknown", "message": "Unknown provider"}


# Global AI service instance
ai_service = AIService() 