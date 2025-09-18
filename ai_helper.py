# ollama_helper.py
import requests
import json
import time
import os
from typing import Optional

class DeepSeekAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("API") #TODO: Add a Deepseek API key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-r1"
        
    def call_api(self, prompt: str, system_message: str = None, max_tokens: int = 1000) -> Optional[str]:
        """
        Make a request to the DeepSeek R1 API via OpenRouter
        """
        if not self.api_key:
            raise ValueError("DeepSeek API key is required")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.3,
            "top_p": 0.9,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except KeyError as e:
            print(f"Unexpected response format: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

deepseek_api = DeepSeekAPI("API") #TODO: Add a Deepseek API key

def call_ollama(prompt: str, system_message: str = None) -> Optional[str]:
    return deepseek_api.call_api(prompt, system_message)