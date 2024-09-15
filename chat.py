import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def send_message(prompt):
    payload = {
        "model": "llama2",
        "prompt": prompt
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    data = json.loads(decoded_line)
                    if "response" in data:
                        full_response += data["response"]
                except json.JSONDecodeError:
                    continue

        return full_response or "No response from Ollama."
    
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {str(e)}"
