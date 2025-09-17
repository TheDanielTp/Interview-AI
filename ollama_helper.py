import requests
import json

def call_ollama(prompt, model="phi3:mini"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            print(f"Error: Ollama API returned status code {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to Ollama. Please ensure it's running on http://localhost:11434")
        return None