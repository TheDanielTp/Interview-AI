# ollama_helper.py
import requests
import json
import time

class OllamaHelper:
    def __init__(self, model="phi3:mini", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.session = requests.Session()
        self.last_call_time = 0
        self.min_call_interval = 0.5  # Minimum time between calls in seconds

    def call_ollama(self, prompt, max_tokens=150, temperature=0.3):
        # Rate limiting to avoid overwhelming the server
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        if time_since_last_call < self.min_call_interval:
            time.sleep(self.min_call_interval - time_since_last_call)
        
        url = f"{self.base_url}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = self.session.post(url, json=data, timeout=30)
            self.last_call_time = time.time()
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                print(f"Error: Ollama API returned status code {response.status_code}")
                return None
        except requests.exceptions.ConnectionError:
            print("Error: Unable to connect to Ollama. Please ensure it's running on http://localhost:11434")
            return None
        except requests.exceptions.Timeout:
            print("Error: Request to Ollama timed out")
            return None

# Create a global instance
ollama_helper = OllamaHelper()

# For backward compatibility
def call_ollama(prompt, model="phi3:mini"):
    return ollama_helper.call_ollama(prompt)